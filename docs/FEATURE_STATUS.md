# KarBaar AI — Feature Implementation Status Matrix

This document defines the exact scope, status, and completion state of the KarBaar application for the CommerceSphere AI / DemandIQ Hackathon.

---

## 1. Core MVP Features (Implemented & 100% Verified)

| Feature | Scope | Status | Notes |
|---|---|:---:|---|
| **Voice-to-Sale** | Bengali voice command to record cash sales | **VERIFIED** | Extracts product, qty, price; reduces inventory; updates sales and profit. |
| **Voice-to-Purchase** | Restock inventory by voice | **VERIFIED** | Increases stock; recalculates Weighted Average Cost (WAC); zero immediate profit penalty. |
| **Voice-to-Credit** | Record credit sale to customer | **VERIFIED** | Reduces stock; logs transaction; adds customer due without double-counting. |
| **Voice-to-Payment** | Collect full/partial credit payment | **VERIFIED** | Decrements customer due; adds cash to drawer; total sales revenue unchanged. |
| **Multi-Action Commands** | Multiple actions in 1 voice sentence | **VERIFIED** | Extracts distinct actions (e.g. sale + expense); presents combined confirmation. |
| **Cumulative Stock Projection** | Batch stock validation | **VERIFIED** | Pre-calculates projected stock sequentially; rejects batch if collective stock short. |
| **Mid-Batch Runtime Rollback** | Saga pattern compensating transaction | **VERIFIED** | Wrapped in `try...catch`; if mid-batch failure occurs, all executed actions are rolled back (`rolledBack: true`). |
| **Human-in-the-Loop Confirmation** | Interactive confirmation card | **VERIFIED** | Shows exact parsed actions; requires explicit "নিশ্চিত করুন" click before write. |
| **Persistent Idempotency Registry** | Storage-backed duplicate guard | **VERIFIED** | Card-level key stored in `localStorage` (`karbaar_idempotency`); blocks duplicate retries across page refresh. |
| **Real Unit Conversion & Rejection** | Fractional units & compatibility | **VERIFIED** | Converts 500g $\rightarrow$ 0.5kg; rejects incompatible units (rice in liters, oil in kg) with clear Bengali messages. |
| **Persistent Undo Engine** | Reversal journal across refresh | **VERIFIED** | `karbaar_undo` in LocalStorage restores undo capability even after page refresh. |
| **Merged Credit Undo** | Safe incremental debt undo | **VERIFIED** | Undoing credit for an existing customer only subtracts added debt; preserves history. |
| **Historical WAC Costing** | Inventory cost basis tracking | **VERIFIED** | Tracks Weighted Average Cost per purchase; restores prior WAC on purchase undo. |
| **Unknown Profit Safety** | Uncataloged item handling | **VERIFIED** | Eliminates invented 15% profit assumption; flags unknown cost as unavailable. |
| **Cash Drawer Reconciliation** | Cash In vs Cash Out reconciliation | **VERIFIED** | Separates sales, collected credit, restock purchases, and operating expenses. |
| **Offline Semantic Rule-Engine** | Hybrid dual-engine fallback | **VERIFIED** | Answers business questions, sales stats, and baki inquiries with 100% offline uptime. |
| **Deterministic Demo Scenario** | Rice 10kg, ৳70 sell, ৳60 cost, Rahim | **VERIFIED** | Seeded catalog matches hackathon demo steps exactly. |
| **Zero Client Key Leakage** | API security proxy | **VERIFIED** | `karbaar-ai` Netlify function holds server-side `GEMINI_API_KEY`; no key in client. |
| **Sliding-Window Rate Limiting** | Endpoint abuse protection | **VERIFIED** | Limits requests to 20 req/min per IP with `Retry-After: 60` HTTP header. |
| **Payload Size Guard** | Buffer overflow protection | **VERIFIED** | Drops payloads larger than 50,000 bytes with HTTP 413. |
| **Mobile-First Responsive UI** | Tailwind CSS mobile layout | **VERIFIED** | Centered prominent mic button, high contrast Bengali typography (`Tiro Bangla`). |

---

## 2. Partially Implemented / Architectural Disclosures

| Feature | Current Implementation | Production Requirement |
|---|---|---|
| **Shop Authorization** | Client passes `x-karbaar-shop` header verified by serverless proxy. | Suitable for single-shop hackathon demo. Multi-tenant commercial release requires JWT / Supabase Auth. |
| **Transactional Consistency** | Client-side compensating transactions (Saga Pattern via `undoLastAction`). | Suitable for offline-first local ledger. High-concurrency cloud multi-user stores require PostgreSQL serializable transactions. |
| **Web Speech Recognition** | Integrated via browser `webkitSpeechRecognition` (bn-BD). | Supported natively in Google Chrome and Microsoft Edge on Android and Desktop. Safari requires text fallback. |
| **Local Storage Persistence** | Full 7-partition LocalStorage sync (`stats`, `tx`, `baki`, `inv`, `sales`, `undo`, `idempotency`). | Excellent for standalone PWA demo. Multi-device cloud sync requires cloud DB backend. |

---

## 3. Deliberately Deferred (Non-MVP Backlog)

To ensure zero half-finished features in the hackathon submission, the following were intentionally deferred:
- Multi-store corporate enterprise dashboard.
- SMS gateway integration (WhatsApp manual greeting is used instead).
- Thermal Bluetooth receipt printer driver.
- Hardware barcode scanner integration.
