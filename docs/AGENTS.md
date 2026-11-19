# KarBaar — AGENTS.md
## Autonomous Coding Agent Directives & Production Maintenance Rules

**Project:** KarBaar (কারবার) — Bengali AI Business Operator & Digital Ledger  
**Standard:** AIBC 2026 Developer Guidelines & Vibe-Coding Standards  
**Authority:** Governing document for all automated coding agents and contributors

---

## 1. Golden Principles
1. **Never Break Financial Consistency:** Ledger debits, credits, cash-in-drawer formulas, and inventory balances must remain strictly deterministic. Never round off decimals without explicit rounding rules.
2. **First Do No Harm (Inspect Before Edit):** Always examine existing state management, DOM event listeners, and LocalStorage keys before modifying code.
3. **No Unapproved External Dependencies:** Keep the application zero-build, ultra-fast, and completely self-contained. Do not introduce massive npm bundles or frameworks that break single-file Netlify deployment.
4. **Authentic Bengali First:** All merchant UI text, error dialogues, receipt formats, and voice prompts must use grammatically natural, respectful Bangladeshi Bengali (ব্যবহারকারীকে আপনি/ভাই সম্বোধন).

---

## 2. Code Quality & Standards
* **Vanilla JavaScript & ES6+:** Modern, clean, well-commented modular JS functions.
* **Tailwind CSS Utility Classes:** Maintain the dark-first Dribbble aesthetic (`#0b0f19` dark canvas, `#7c3aed` brand purple, emerald status indicators).
* **DOM Event Binding:** Use explicit descriptive function names (`toggleNotificationModal`, `openTransactionModal`, `exportDataJSON`).
* **Safe LocalStorage Access:** Always wrap storage access in `try...catch` blocks to handle private browsing mode restrictions gracefully.

---

## 3. Security & Anti-Exfiltration Boundaries
* **Serverless API Key Isolation:** Client-side scripts must never store production master Gemini API keys in plain text. Always route through Netlify Serverless Functions (`/.netlify/functions/karbaar-ai`) with server-side environment variables (`GEMINI_API_KEY`).
* **Input Sanitization:** Sanitize all user inputs using `escapeHtml()` before rendering to innerHTML to prevent XSS.
* **Zero PII Leakage:** Customer phone numbers and balances must never be transmitted to third-party telemetry or ad-trackers.

---

## 4. Test Discipline & Verification
* **Pre-Commit Verification:** Run `node -c` on all function files and execute the 11/11 financial audit suite before deploying to Netlify or pushing to GitHub.
* **Zero Syntax Errors:** Ensure all JSON files, redirects, and manifest files parse with exit code 0.
