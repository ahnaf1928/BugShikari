# KarBaar AI — Changelog (v2.1 Championship MVP)

All notable changes and architectural improvements implemented during this final championship engineering pass:

---

### [2.1.1] - 2026-11-20 (Independent Audit Hardening Pass)

#### 🔄 Mid-Batch Execution Rollback (Saga Pattern)
- **Compensating Transaction Engine:** `renderActionCard.executeConfirmedBatch()` wrapped in `try...catch`. If an action fails mid-execution (after earlier actions have already mutated stock and sales), all earlier actions are systematically rolled back via `undoLastAction()`.
- **Empirically Verified in T11:** Action 1 commits, Action 2 encounters execution failure, Action 1 is reversed, and store state returns 100% to baseline (`rolledBack: true`).

#### 🔒 Persistent Idempotency Registry
- **Storage-Backed Deduplication:** Added `LS.idempotency = 'karbaar_idempotency'` in `localStorage`.
- **Cross-Instance & Reload Protection:** Re-submitting the same batch key across page reloads or network retries is immediately rejected with `{ ok: false, error: 'already_executed', duplicate: true }`.

#### ⚖️ Fractional Unit Conversion & Physical Compatibility
- **Real Unit Conversion:** Spoken quantities in grams (e.g., ৫০০ গ্রাম চিনি) automatically convert to fractional base units (০.৫ কেজি) and calculate exact pro-rated prices.
- **Physical Incompatibility Rejection:** Strictly prevents selling solid goods (rice, sugar) in liquid volume units (liters, ml) and discrete liquid items (oil bottles) in weight units (kg) with explicit, helpful Bengali error guidance.

---

### [2.1.0] - 2026-11-20

#### 🛡️ Financial Integrity & Accounting
- **Weighted Average Cost (WAC):** Implemented dynamic inventory costing formula on restocks ($$\text{New WAC} = \frac{\text{Current Cost} \times \text{Current Stock} + \text{New Cost} \times \text{New Qty}}{\text{Total Stock}}$$). Purchases track previous WAC and undo restores original cost basis.
- **Eliminated Fake Profit:** Removed the arbitrary 15% profit assumption for unknown products. Items without cost basis now explicitly record `calculatedProfit: null` and `tx.profitUnknown: true`, never inventing figures.
- **Cumulative Stock Projection:** Implemented `validateBatchActions()` to simulate sequential inventory demand across multi-action batches. Prevents cumulative stock shortfall (e.g. 3+3 when stock is 5).
- **Zero Double-Counting:** Strict separation of credit sale revenue from subsequent debt collection.
- **Negative & Infinite Input Guards:** Finite numeric checks (`isFinite(amount)`, `isFinite(qty)`, `amount > 0`, `qty > 0`) applied across `commitTransaction`, `addBakiEntry`, and `collectBaki`.

#### ↩ Undo & Ledger Reversal
- **LocalStorage Undo Persistence:** Added `LS.undo = 'karbaar_undo'` to persist up to 50 reversible journal entries. Undo capability survives browser refresh and crashes.
- **Safe Merged Credit Undo:** `addBakiEntry` now tracks `isNew` and `amountAdded`. Undoing credit addition for an existing customer only decrements the added amount, preserving prior debt and customer records.
- **Unique Cryptographic Transaction IDs:** Every transaction is stamped with `tx_timestamp_random`, enforcing idempotency and preventing duplicate commit retries.

#### 🤖 AI & Serverless Security
- **Zero Client Key Leakage:** Completely eliminated browser API key input UI and client storage.
- **Serverless Hardening:**
  - Integrated Google Gemini 2.5 Flash & 2.0 Flash REST endpoints.
  - Rate limiting enforced at 20 req/min per IP with `Retry-After: 60` HTTP headers.
  - Maximum payload size guard set to 50,000 bytes (HTTP 413).
  - Client sends `x-karbaar-shop: karbaar-demo-shop-bd-01` header verified by backend.
- **Compound Query AI Engine:** Enhanced `localAnswer` to resolve compound multi-entity queries (Rice stock + Rahim due + profit) from verified ledger records.

#### 🧪 Testing & Verification
- **Test Suite Overhaul:** Expanded `generate_tests.py` from 11 tests to 24 comprehensive, automated tests.
- **Path Portability:** Replaced Windows-hardcoded paths with dynamic `os.path.dirname(os.path.abspath(__file__))`.
- **100% Pass Rate:** All 24 automated tests PASS with verified empirical outputs on standalone Node.js v20.18.0.
