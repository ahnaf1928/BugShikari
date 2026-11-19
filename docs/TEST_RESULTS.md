# KarBaar AI — Automated Test Results Log (Production Verification)

**Execution Engine:** Portable Standalone Node.js v20.18.0  
**Test Suite:** 24 Financial Integrity, Accounting, Concurrency & Security Tests  
**Result:** **24/24 Tests PASSED (100% Empirical Pass Rate)**  
**Verification Date:** 2026-11-20  

---

## 📊 Summary of Test Execution

| Category | Tests | Status | Details |
| :--- | :--- | :--- | :--- |
| **A. Core Accounting & Inventory** | T01 – T08 | **8/8 PASS** | WAC restock, cash/credit sales, debt settlement, separated OpEx, unknown profit transparency |
| **B. Concurrency, Batches & Rollbacks** | T09 – T12 | **4/4 PASS** | Sequential stock projection, multi-action consistency, **mid-batch runtime failure rollback (Saga pattern)**, **persistent idempotency registry** |
| **C. Undo, History & Reversals** | T13 – T15 | **3/3 PASS** | Refresh-surviving undo journal, customer balance merge protection, debt collection reversals |
| **D. Input Validation & Clarification** | T16 – T20 | **5/5 PASS** | Numeric guards, **gram-to-kg conversion & incompatible unit rejection**, entity clarification, offline fallback |
| **E. Persistence, Reconciliation & Invariants** | T21 – T24 | **4/4 PASS** | 7 localStorage partitions, cash drawer reconciliation, historical cost undo, error burst resilience |

---

## 🔬 Detailed Test-by-Test Verification Log

### [T01] Cash sale updates inventory and revenue — ✅ **PASS**
- **Expected:** Stock 4 -> 2, Sales = 370, Profit = 30
- **Actual:** `Stock: 2, Sales: 370, Profit: 30`
- **Evidence / Assertion:** _Transaction logged: তীর সয়াবিন তেল বিক্রি, Qty: 2, id: tx_1795128680328_7ke8dk_

### [T02] Purchase updates inventory and weighted-average cost — ✅ **PASS**
- **Expected:** Stock 7 -> 17, WAC updated to 140 BDT, Profit unchanged
- **Actual:** `Stock: 17, WAC: 140, Profit: 30`
- **Evidence / Assertion:** _Purchase recorded as asset restock. prevAvgCost: 130, newAvgCost: 140_

### [T03] Credit sale updates inventory, revenue, and dues — ✅ **PASS**
- **Expected:** Stock 10 -> 8, Sales += 140, Rahim due = 140, Profit += 20
- **Actual:** `Stock: 8, Sales: 510, Rahim due: 140, Profit: 50`
- **Evidence / Assertion:** _Credit sale ledger entry created with isCredit: true, bakiId: b_1795128680334_321_

### [T04] Partial credit payment reduces dues without increasing sales — ✅ **PASS**
- **Expected:** Rahim due 140 -> 40, Settled: false, Collected = 100, Sales strictly unchanged
- **Actual:** `Rahim due: 40, Settled: false, Collected: 100, Sales: 510 (Before: 510)`
- **Evidence / Assertion:** _Zero double-counting: Revenue recognized at credit sale, not collection_

### [T05] Full payment settles dues — ✅ **PASS**
- **Expected:** Due 500 -> 0, Settled = true
- **Actual:** `Due: 0, Settled: true`
- **Evidence / Assertion:** _bakiList marked settled with timestamped payment log_

### [T06] Discounted sale calculates correct profit — ✅ **PASS**
- **Expected:** Profit increase = 5 BDT (175 sold - 170 cost)
- **Actual:** `Profit increase: 5 BDT (Total profit: 55)`
- **Evidence / Assertion:** _Historical cost basis 170 BDT deducted from discounted revenue 175 BDT_

### [T07] Unknown cost produces unknown profit — ✅ **PASS**
- **Expected:** tx.profitUnknown = true, tx.calculatedProfit = null, stats.profit unchanged (No fake 15%)
- **Actual:** `profitUnknown: true, calculatedProfit: null, Profit delta: 0`
- **Evidence / Assertion:** _System reports unknown profit as unavailable rather than fabricating a number_

### [T08] Operating expenses separated from purchase costs — ✅ **PASS**
- **Expected:** Operating expenses reduce profit by 450, separated from purchase costs (1470)
- **Actual:** `Expenses: 450, Purchases: 1470, Profit: -395`
- **Evidence / Assertion:** _Cash reconciliation separates period operating expense from asset restock_

### [T09] Cumulative batch stock shortage is rejected — ✅ **PASS**
- **Expected:** Batch rejected due to cumulative shortage. Stock unchanged at 1.
- **Actual:** `Validation ok: false, Error: "তেল-এর পর্যাপ্ত স্টক নেই। ব্যাচের মোট চাহিদা ১ বোতল, কিন্তু অবশিষ্ট প্রজেক্টেড স্টক মাত্র ০ বোতল।", Stock: 1`
- **Evidence / Assertion:** _validateBatchActions projected cumulative stock sequentially across batch_

### [T10] Multi-action batch succeeds consistently — ✅ **PASS**
- **Expected:** Both actions committed atomically. Sugar stock 17 -> 15, Sales += 280
- **Actual:** `Saved: 2, Sugar stock: 15, Sales: 1465`
- **Evidence / Assertion:** _Batch pre-validation succeeded and both transactions committed consistently_

### [T11] Mid-batch failure does not silently corrupt records — ✅ **PASS**
- **Expected:** Action 1 executed and rolled back after Action 2 mid-execution failure. State 100% restored (rolledBack: true).
- **Actual:** `res.ok: false, rolledBack: true, Sugar stock: 15 (Before: 15), Sales: 1465 (Before: 1465)`
- **Evidence / Assertion:** _Mid-batch runtime failure triggered compensating transaction rollback (Saga pattern); zero partial mutation remained._

### [T12] Duplicate request is not applied twice — ✅ **PASS**
- **Expected:** 1st call: ok true; 2nd call: in-memory latch blocked; 3rd call: persistent registry blocked duplicate. Sales delta +140 exactly.
- **Actual:** `1st: true, 2nd: already_executed, 3rd duplicate: true, Sales delta: 140`
- **Evidence / Assertion:** _Persistent idempotency store in localStorage blocks resubmissions across card instances and page refreshes_

### [T13] Undo survives page refresh — ✅ **PASS**
- **Expected:** Undo succeeds post-refresh: Stock reverted to 14, Sales reverted to 1605
- **Actual:** `Undo ok: true, Stock: 14, Sales: 1605`
- **Evidence / Assertion:** _undoStack restored from LS.undo and transaction reverted successfully_

### [T14] Merged customer credit undo preserves earlier balances — ✅ **PASS**
- **Expected:** Due merged to 3000, reverted to 2000. Customer record preserved.
- **Actual:** `Before undo: 3000, After undo: 2000, Customer exists: true`
- **Evidence / Assertion:** _baki_add undo decremented only the added amount without deleting merged record_

### [T15] Payment reversal restores the correct balance — ✅ **PASS**
- **Expected:** Due 140 -> 40 on payment -> 140 on undo. Sales revenue constant throughout.
- **Actual:** `Due after pay: 40, Due after undo: 140, Sales: 1745 (Expected: 1745)`
- **Evidence / Assertion:** _baki_collect undo restored customer balance and decremented collectedBaki without touching sales_

### [T16] Negative, zero, NaN, and infinite amounts are rejected — ✅ **PASS**
- **Expected:** All 6 invalid transactions rejected with ok: false.
- **Actual:** `tZero: false, tNeg: false, tNaN: false, tInf: false, tZeroQty: false, tNegQty: false`
- **Evidence / Assertion:** _commitTransaction strictly enforces positive finite numeric amounts and quantities_

### [T17] Invalid unit conversion & unit mismatch rejected — ✅ **PASS**
- **Expected:** 500g converts to 0.5kg; Rice/oil unit mismatches rejected with Bengali guidance; negative qty sanitized.
- **Actual:** `Conversion: true (qty: 0.5, amt: 70), Rice mismatch: true, Oil mismatch: true, Sanitize: true`
- **Evidence / Assertion:** _Unit engine performs gram-to-kg conversion and rejects physical unit incompatibilities with explicit Bengali guidance_

### [T18] Missing or ambiguous customer triggers clarification — ✅ **PASS**
- **Expected:** Missing customer triggers clear Bengali clarification prompt.
- **Actual:** `Result: "কার নামে বাকি লিখব? নামসহ আবার বলুন।"`
- **Evidence / Assertion:** _resolveAction requires explicit customer name for all credit transactions_

### [T19] Missing or ambiguous product triggers clarification — ✅ **PASS**
- **Expected:** Unrecognized product triggers product clarification prompt.
- **Actual:** `Result: "কোন পণ্য বুঝতে পারিনি।"`
- **Evidence / Assertion:** _resolveAction matches against catalog and refuses ambiguous items_

### [T20] AI network failure handled transparently with local fallback — ✅ **PASS**
- **Expected:** Returns local answer gracefully with offline badge.
- **Actual:** `Source: "Karbaar AI · হিসাব সহকারী (লোকাল ইঞ্জিন)", Preview: "রহমান ভাই, আমি স্টক, কেনার পরামর্শ, লাভ, বাকি আদায..."`
- **Evidence / Assertion:** _localAnswer provides 100% offline uptime when cloud network is unreachable_

### [T21] Local data persists after refresh — ✅ **PASS**
- **Expected:** All 6 storage partitions saved and 100% reconstructed without data loss.
- **Actual:** `Keys present: true, Sales: 1745, Tx: 12, Baki: 4, Undo: 12`
- **Evidence / Assertion:** _Keys in storage: karbaar_stats, karbaar_transactions, karbaar_baki, karbaar_inventory, karbaar_saleslog, karbaar_undo, karbaar_idempotency_

### [T22] Cash reconciliation matches underlying transactions — ✅ **PASS**
- **Expected:** Drawer cash exactly equals totalCashIn (2065) - totalCashOut (1970) = 95
- **Actual:** `Drawer cash: 95, Expected: 95`
- **Evidence / Assertion:** _Cash-in (Sales + Collected) minus Cash-out (Purchases + Expenses) matches ledger_

### [T23] Historical cost changes handled correctly — ✅ **PASS**
- **Expected:** WAC updated to 71.11, then reverted to 60 on undo. Stock 18 -> 8.
- **Actual:** `WAC after restock: 71.11, WAC after undo: 60, Stock after undo: 8`
- **Evidence / Assertion:** _commitTransaction tracked prevAvgCost and undoLastAction restored historical cost basis_

### [T24] All business invariants remain valid after consecutive errors — ✅ **PASS**
- **Expected:** State completely unchanged after consecutive illegal actions.
- **Actual:** `Tx count: 12 (Before: 12), Sales: 1745 (Before: 1745)`
- **Evidence / Assertion:** _Zero ghost records or ledger corruption after error bursts_

---

## 🎯 Key Architectural Findings Confirmed by Test Suite

1. **True Mid-Batch Runtime Rollback (T11):**  
   Action 1 executes and commits to ledger and stock. When Action 2 encounters a runtime execution failure, the compensating transaction handler (`undoLastAction()`) systematically rolls back Action 1. The inventory stock, revenue, and undo journal return 100% to baseline (`rolledBack: true`).
2. **Persistent Idempotency Registry (T12):**  
   Idempotency is enforced not only via in-memory button latches but persistently in `localStorage` (`karbaar_idempotency`). Re-submitting the same batch key across page reloads or network retries is immediately rejected (`duplicate: true`).
3. **True Unit Conversion & Physical Compatibility (T17):**  
   Weight units convert accurately (500 gram sugar $\rightarrow$ 0.5 kg at 70 BDT). Physical unit mismatches (selling rice in liters, or oil bottles in kg) are rejected with clear Bengali guidance instructing the shopkeeper on the correct unit.
4. **Weighted-Average Cost (WAC) Accounting (T02, T23):**  
   Restocks calculate exact WAC; inventory and cost baselines cleanly revert when purchase transactions are undone.
5. **Separation of Cash-in from Revenue (T04, T15):**  
   Collecting customer debt increases cash without inflating revenue (zero double-counting).
