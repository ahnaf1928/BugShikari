// Karbaar AI — High-Performance Secure Serverless Proxy for Google Gemini API
// Netlify Function: /.netlify/functions/karbaar-ai
// Environment Variables:
//   GEMINI_API_KEY   (Required in Netlify Site Configuration)
//   GEMINI_MODELS    (Optional comma-separated list of models)

// Battle-tested, rock-solid Gemini models in priority order:
// gemini-1.5-flash responds in ~1.2s with zero thinking overhead and high rate limits.
const DEFAULT_MODELS = [
  'gemini-1.5-flash',
  'gemini-2.0-flash',
  'gemini-1.5-flash-8b',
  'gemini-flash-latest'
];

const API_BASE = 'https://generativelanguage.googleapis.com/v1beta/models';
const MAX_CONTENTS = 12;
const MAX_TEXT = 3000;
const MAX_SYSTEM = 9000;
const BUDGET_MS = 24000; // 24 seconds total execution budget (Netlify Lambda allows up to 26s)
const MAX_PAYLOAD_BYTES = 50000;

// Rate limiter per IP (25 requests per minute)
const hits = new Map();
function isRateLimited(ip) {
  const now = Date.now();
  const win = 60000;
  const max = 25;
  const arr = (hits.get(ip) || []).filter(t => now - t < win);
  arr.push(now);
  hits.set(ip, arr);
  if (hits.size > 500) {
    for (const [k, v] of hits) {
      if (!v.some(t => now - t < win)) hits.delete(k);
    }
  }
  return arr.length > max;
}

const jsonResponse = (code, obj, extraHeaders = {}) => ({
  statusCode: code,
  headers: {
    'Content-Type': 'application/json; charset=utf-8',
    'Cache-Control': 'no-store, no-cache, must-revalidate',
    'X-Content-Type-Options': 'nosniff',
    ...extraHeaders
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

function buildGenConfig(body) {
  const isJson = body.responseFormat === 'json';
  const config = {
    temperature: isJson ? 0.1 : 0.4,
    maxOutputTokens: isJson ? 1024 : 2048
  };
  if (isJson) {
    config.responseMimeType = 'application/json';
    if (body.responseSchema && typeof body.responseSchema === 'object') {
      config.responseSchema = body.responseSchema;
    }
  }
  return config;
}

exports.handler = async (event) => {
  const allowedOrigin = process.env.ALLOWED_ORIGIN || '*';

  // Handle CORS Preflight OPTIONS
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 204,
      headers: {
        'Access-Control-Allow-Origin': allowedOrigin,
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, x-karbaar-shop, X-Karbaar-Shop',
        'Access-Control-Max-Age': '86400'
      }
    };
  }

  const key = (process.env.GEMINI_API_KEY || '').trim();

  // GET health probe
  if (event.httpMethod === 'GET') {
    return jsonResponse(200, {
      ok: true,
      configured: Boolean(key),
      keyLength: key ? key.length : 0
    }, { 'Access-Control-Allow-Origin': allowedOrigin });
  }

  if (event.httpMethod !== 'POST') {
    return jsonResponse(405, { error: 'Method not allowed' });
  }

  // Shop Token Validation
  const shopToken = (event.headers && (event.headers['x-karbaar-shop'] || event.headers['X-Karbaar-Shop'])) || '';
  const EXPECTED_SHOP = process.env.KARBAAR_SHOP_ID || 'karbaar-demo-shop-bd-01';
  if (shopToken !== EXPECTED_SHOP) {
    return jsonResponse(401, { error: 'Unauthorized: Missing or invalid shop credentials' });
  }

  // Payload Size Validation
  const rawBody = event.body || '';
  if (rawBody.length > MAX_PAYLOAD_BYTES) {
    return jsonResponse(413, { error: 'Payload too large' });
  }

  if (!key) {
    return jsonResponse(503, { error: 'GEMINI_API_KEY is not configured in Netlify Environment Variables.' });
  }

  // Rate Limiting
  const ip = (event.headers && (event.headers['x-nf-client-connection-ip'] || event.headers['x-forwarded-for'])) || 'anon';
  if (isRateLimited(String(ip).split(',')[0].trim())) {
    return jsonResponse(429, {
      error: 'অনেক বেশি অনুরোধ — এক মিনিট পরে আবার চেষ্টা করুন।',
      upstreamStatus: 429
    }, { 'Retry-After': '60' });
  }

  let body;
  try {
    body = JSON.parse(rawBody);
  } catch (e) {
    return jsonResponse(400, { error: 'Invalid JSON body' });
  }

  const contents = cleanContents(body.contents);
  if (!contents) {
    return jsonResponse(400, { error: 'Invalid or empty contents' });
  }

  const system = clip(body.system, MAX_SYSTEM);
  const deadline = Date.now() + BUDGET_MS;

  let models = (process.env.GEMINI_MODELS || '').split(',').map(s => s.trim()).filter(Boolean);
  if (!models.length) {
    models = DEFAULT_MODELS.slice();
  }

  const attempts = [];
  let lastStatus = 0;
  let lastError = '';
  let retryAfter = 0;

  for (const model of models) {
    const remainingTime = deadline - Date.now();
    if (remainingTime < 2000) break;

    const controller = new AbortController();
    const timeoutHandle = setTimeout(() => controller.abort(), Math.min(12000, remainingTime));
    const startTime = Date.now();

    try {
      const payload = {
        contents,
        generationConfig: buildGenConfig(body)
      };
      if (system) {
        payload.systemInstruction = { parts: [{ text: system }] };
      }

      const response = await fetch(`${API_BASE}/${encodeURIComponent(model)}:generateContent`, {
        method: 'POST',
        signal: controller.signal,
        headers: {
          'Content-Type': 'application/json',
          'x-goog-api-key': key
        },
        body: JSON.stringify(payload)
      });

      clearTimeout(timeoutHandle);
      const durationMs = Date.now() - startTime;

      if (!response.ok) {
        lastStatus = response.status;
        let errMsg = '';
        try {
          const errJson = await response.json();
          errMsg = (errJson && errJson.error && errJson.error.message) || response.statusText;
        } catch (_) {
          errMsg = response.statusText;
        }
        lastError = clip(errMsg, 300);
        const ra = Number(response.headers.get('retry-after')) || 0;
        if (ra) retryAfter = ra;

        attempts.push({ model, status: response.status, durationMs, error: lastError });

        // If API key is fundamentally bad (400 bad key, 403 forbidden), stop immediately
        if (response.status === 400 && /API_KEY|key not valid|credential/i.test(lastError)) {
          break;
        }
        if (response.status === 403 || response.status === 401) {
          break;
        }
        continue;
      }

      const data = await response.json();
      const cand = data.candidates && data.candidates[0];
      const parts = (cand && cand.content && cand.content.parts) || [];
      const text = parts.filter(p => p && p.text && !p.thought).map(p => p.text).join('');

      if (text.trim()) {
        return jsonResponse(200, {
          text,
          model,
          finishReason: cand.finishReason || 'STOP',
          durationMs
        }, { 'Access-Control-Allow-Origin': allowedOrigin });
      }

      attempts.push({ model, status: 200, durationMs, error: 'empty response text' });
    } catch (err) {
      clearTimeout(timeoutHandle);
      const durationMs = Date.now() - startTime;
      const isTimeout = err && err.name === 'AbortError';
      lastStatus = isTimeout ? 504 : 500;
      lastError = isTimeout ? 'timeout' : clip(err && err.message, 120);
      attempts.push({ model, status: lastStatus, durationMs, error: lastError });
    }
  }

  return jsonResponse(502, {
    error: 'AI service unavailable',
    upstreamStatus: lastStatus || 504,
    upstreamError: lastError || 'timeout',
    attempts,
    retryAfter
  }, {
    'Access-Control-Allow-Origin': allowedOrigin,
    ...(retryAfter ? { 'Retry-After': String(retryAfter) } : {})
  });
};
