// Karbaar AI — secure server proxy for the Gemini API (Netlify Function).
// The API key lives ONLY in the GEMINI_API_KEY environment variable; it never reaches the browser.
//
// Env vars:
//   GEMINI_API_KEY   (required)
//   GEMINI_MODELS    (optional, comma list, tried in order)
//   ALLOWED_ORIGIN   (optional, e.g. https://karbaar.netlify.app — blocks other sites from using your quota)

// Strictly modern, supported models (retired 1.5 family removed to avoid 404 latency)
const DEFAULT_MODELS = [
  'gemini-2.5-flash',
  'gemini-2.0-flash',
  'gemini-2.5-flash-lite',
  'gemini-flash-latest',
  'gemini-flash-lite-latest'
];
const API = 'https://generativelanguage.googleapis.com/v1beta/models';
const MAX_CONTENTS = 12, MAX_TEXT = 3000, MAX_SYSTEM = 9000, BUDGET_MS = 8500, MAX_PAYLOAD_BYTES = 50000;

// --- Sliding-window IP rate limiting (protects free quota from abuse)
const hits = new Map();
function limited(ip) {
  const now = Date.now(), win = 60000, max = 20; // 20 requests per minute per IP
  const arr = (hits.get(ip) || []).filter(t => now - t < win);
  arr.push(now); hits.set(ip, arr);
  if (hits.size > 500) for (const [k, v] of hits) if (!v.some(t => now - t < win)) hits.delete(k);
  return arr.length > max;
}

// --- discovered model list (ListModels), cached per warm instance
let discovered = null, discoveredAt = 0;
async function discoverModels(key, deadline) {
  if (discovered && Date.now() - discoveredAt < 6 * 3600000) return discovered;
  try {
    const ctl = new AbortController();
    const t = setTimeout(() => ctl.abort(), Math.max(1000, Math.min(3000, deadline - Date.now())));
    const r = await fetch('https://generativelanguage.googleapis.com/v1beta/models?pageSize=200', { headers: { 'x-goog-api-key': key }, signal: ctl.signal });
    clearTimeout(t);
    if (!r.ok) return [];
    const j = await r.json();
    const list = (j.models || [])
      .filter(m => (m.supportedGenerationMethods || []).includes('generateContent'))
      .map(m => String(m.name || '').replace(/^models\//, ''))
      .filter(n => /^gemini-[\d.]+-flash(-lite)?$|^gemini-flash(-lite)?-latest$/.test(n))
      .sort((a, b) => (/lite/.test(a) ? 1 : 0) - (/lite/.test(b) ? 1 : 0) || b.localeCompare(a));
    discovered = list; discoveredAt = Date.now();
    return list;
  } catch (e) { return []; }
}

const json = (code, obj, extra) => ({
  statusCode: code,
  headers: {
    'Content-Type': 'application/json; charset=utf-8',
    'Cache-Control': 'no-store',
    'X-Content-Type-Options': 'nosniff',
    ...(extra || {})
  },
  body: JSON.stringify(obj)
});
const clip = (s, n) => String(s == null ? '' : s).slice(0, n);

function cleanContents(raw) {
  if (!Array.isArray(raw)) return null;
  const out = [];
  for (const c of raw.slice(-MAX_CONTENTS)) {
    const role = c && c.role === 'model' ? 'model' : 'user';
    const text = c && Array.isArray(c.parts) ? c.parts.map(p => clip(p && p.text, MAX_TEXT)).join('') : '';
    if (text.trim()) out.push({ role, parts: [{ text }] });
  }
  while (out.length && out[0].role !== 'user') out.shift();
  return out.length && out[out.length - 1].role === 'user' ? out : null;
}

function buildGenConfig(model, body, tokens) {
  const g = { temperature: 0.4, maxOutputTokens: tokens };
  const asJson = body.responseFormat === 'json';
  if (asJson) {
    g.responseMimeType = 'application/json';
    g.temperature = 0.1;
    if (body.responseSchema && typeof body.responseSchema === 'object') g.responseSchema = body.responseSchema;
  }
  // 2.5-flash "thinks" by default; set budget to 0 to save latency and token quota
  if (/2\.5-flash/.test(model)) g.thinkingConfig = { thinkingBudget: 0 };
  return g;
}

exports.handler = async (event) => {
  const allowed = process.env.ALLOWED_ORIGIN || '*';

  // Handle preflight OPTIONS
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 204,
      headers: {
        'Access-Control-Allow-Origin': allowed,
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, x-karbaar-shop, X-Karbaar-Shop',
        'Access-Control-Max-Age': '86400'
      }
    };
  }

  const key = process.env.GEMINI_API_KEY;
  if (event.httpMethod === 'GET') return json(200, { ok: true, configured: Boolean(key) }, { 'Access-Control-Allow-Origin': allowed });
  if (event.httpMethod !== 'POST') return json(405, { error: 'Method not allowed' });

  // DEMO-TIER ABUSE PROTECTION:
  // Verifies client shop token to prevent casual unauthorized bot scraping of the serverless Gemini quota.
  // ARCHITECTURAL NOTE: For multi-tenant commercial production, replace this single-tenant demo token
  // with cryptographically signed user sessions (JWT / Supabase Auth / OAuth2).
  const shopToken = (event.headers && (event.headers['x-karbaar-shop'] || event.headers['X-Karbaar-Shop'])) || '';
  const EXPECTED_SHOP = process.env.KARBAAR_SHOP_ID || 'karbaar-demo-shop-bd-01';
  if (shopToken !== EXPECTED_SHOP) {
    return json(401, { error: 'Unauthorized: Missing or invalid shop credentials' });
  }

  // Payload size check
  const rawBody = event.body || '';
  if (rawBody.length > MAX_PAYLOAD_BYTES) return json(413, { error: 'Payload too large' });

  // Origin check as complementary browser restriction
  const origin = (event.headers && (event.headers.origin || event.headers.Origin)) || '';
  if (process.env.ALLOWED_ORIGIN && origin && origin !== process.env.ALLOWED_ORIGIN) {
    return json(403, { error: 'Origin not allowed' });
  }
  if (!key) return json(503, { error: 'GEMINI_API_KEY is not configured on the server' });

  // Rate limit
  const ip = (event.headers && (event.headers['x-nf-client-connection-ip'] || event.headers['x-forwarded-for'])) || 'anon';
  if (limited(String(ip).split(',')[0].trim())) {
    return json(429, { error: 'অনেক বেশি অনুরোধ — এক মিনিট পরে আবার চেষ্টা করুন।', upstreamStatus: 429 }, { 'Retry-After': '60' });
  }

  let body;
  try { body = JSON.parse(rawBody); } catch (e) { return json(400, { error: 'Invalid JSON' }); }
  const contents = cleanContents(body.contents);
  if (!contents) return json(400, { error: 'Invalid contents' });
  const system = clip(body.system, MAX_SYSTEM);

  const deadline = Date.now() + BUDGET_MS;
  let models = (process.env.GEMINI_MODELS || '').split(',').map(s => s.trim()).filter(Boolean);
  if (!models.length) models = DEFAULT_MODELS.slice();

  let upstreamStatus = 0, upstreamError = '', retryAfter = 0, triedDiscovery = false;

  for (let mi = 0; mi < models.length; mi++) {
    const model = models[mi];
    let notFound = false;
    for (const tokens of [body.responseFormat === 'json' ? 1024 : 2048, 4096]) {
      const left = deadline - Date.now();
      if (left < 1200) break;
      const ctl = new AbortController();
      const timer = setTimeout(() => ctl.abort(), left);
      try {
        const res = await fetch(`${API}/${encodeURIComponent(model)}:generateContent`, {
          method: 'POST', signal: ctl.signal,
          headers: { 'Content-Type': 'application/json', 'x-goog-api-key': key },
          body: JSON.stringify({
            ...(system ? { systemInstruction: { parts: [{ text: system }] } } : {}),
            contents, generationConfig: buildGenConfig(model, body, tokens)
          })
        });
        clearTimeout(timer);
        if (!res.ok) {
          upstreamStatus = res.status;
          let msg = '';
          try { const e = await res.json(); msg = clip(e && e.error && e.error.message, 300); } catch (e) {}
          upstreamError = msg;
          const ra = Number(res.headers.get('retry-after')) || 0; if (ra) retryAfter = ra;
          if (res.status === 404) notFound = true;
          if (res.status === 503 && tokens === 2048 && deadline - Date.now() > 3000) continue; // transient overload: one quick retry
          break;
        }
        const data = await res.json();
        const cand = data.candidates && data.candidates[0];
        const parts = (cand && cand.content && cand.content.parts) || [];
        const text = parts.filter(p => p && p.text && !p.thought).map(p => p.text).join('');
        if (text.trim()) {
          if (cand.finishReason === 'MAX_TOKENS' && tokens === 2048) continue; // retry once with a bigger budget
          return json(200, { text, model, finishReason: cand.finishReason || 'STOP' });
        }
        upstreamStatus = 200; upstreamError = 'empty response' + (cand && cand.finishReason ? ' (' + cand.finishReason + ')' : '');
        break;
      } catch (e) {
        clearTimeout(timer);
        upstreamStatus = 504; upstreamError = e && e.name === 'AbortError' ? 'timeout' : clip(e && e.message, 120);
        break;
      }
    }
    // every configured model 404'd (retired/renamed): ask Google which models this key can really use
    if (notFound && mi === models.length - 1 && !triedDiscovery && deadline - Date.now() > 2500) {
      triedDiscovery = true;
      const found = (await discoverModels(key, deadline)).filter(m => !models.includes(m));
      if (found.length) models.push(...found.slice(0, 3));
    }
    // a bad/blocked key will not be fixed by another model: stop early. (Quota is per-model, so 429 moves on to the next model.)
    if (upstreamStatus === 401 || upstreamStatus === 403 || (upstreamStatus === 400 && /api key|API_KEY|permission/i.test(upstreamError))) break;
  }

  return json(502, { error: 'AI service unavailable', upstreamStatus, upstreamError, retryAfter }, retryAfter ? { 'Retry-After': String(retryAfter) } : {});
};
