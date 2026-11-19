# KarBaar — DATABASE.md
## Data Architecture, Local-First Persistence & Schema Specifications

**Project:** KarBaar (কারবার) — Bengali AI Business Operator & Digital Ledger  
**Track:** CommerceSphere AI / DemandIQ  
**Target Environment:** Local-First Client-Side Persistence with Zero Server Cloud Vulnerability  
**Storage Engine:** HTML5 LocalStorage with Versioned JSON Models & Idempotency Registry

---

## 1. Design Philosophy: Local-First & Sovereign Data
Micro-merchants in Bangladesh (মুদির দোকান) prioritize absolute privacy, zero recurring cloud hosting costs, and 100% uninterrupted offline usability in areas with erratic connectivity.
* **Zero Remote DB Dependency:** Financial records reside strictly in the merchant's private browser memory.
* **Zero Data Exfiltration:** Neither customer phone numbers nor financial ledger balances are uploaded to external databases.
* **Deterministic Migrations:** State versions are tagged (`karbaar_v3_nov2026_prices`) ensuring automated schema evolution without data loss.

---

## 2. Entity Schemas & Models

### 2.1 Store Profile (`karbaar_store_profile`)
```typescript
interface StoreProfile {
  name: string;      // e.g. "রহমান জেনারেল স্টোর"
  owner: string;     // e.g. "রহমান ভাই"
  area: string;      // e.g. "মিরপুর-১০, ঢাকা"
  category: string;  // e.g. "মুদি ও কনফেকশনারি"
  currency: string;  // "BDT" (৳)
}
```

### 2.2 Inventory Item (`karbaar_inventory`)
```typescript
interface InventoryItem {
  id: string;        // Unique identifier (e.g. "p1", "p2")
  name: string;      // Full Bengali product name (e.g. "তীর সয়াবিন তেল (১ লি.)")
  short: string;     // Voice keyword alias (e.g. "তেল")
  unit: string;      // Measurement unit ("বোতল", "কেজি", "বস্তা", "প্যাকেট")
  buy: number;       // Benchmark wholesale buy price (৳)
  avgCost: number;   // Moving average cost basis for FIFO margin tracking (৳)
  sell: number;      // Retail selling price (৳)
  stock: number;     // Physical stock units available
  avgDaily: number;  // Seed baseline daily run-rate
}
```

### 2.3 Financial Transaction (`karbaar_transactions`)
```typescript
interface Transaction {
  id?: string;               // UUID or timestamp
  ts: number;                // Epoch timestamp (ms, Dhaka UTC+6)
  desc: string;              // Bengali narrative note
  cat: string;               // Category ("মুদি পণ্য", "পণ্য ক্রয়", "দোকান খরচ", "ইউটিলিটি বিল")
  type: 'income' | 'expense';// Cashflow direction
  amount: number;            // Financial value in BDT (৳)
  pid?: string;              // Optional linked product ID (triggers auto-stock update)
  qty?: number;              // Physical units moved
  isCredit?: boolean;        // Whether transaction was deferred on baki
  isBakiCollection?: boolean;// Whether transaction represents recovered debt
}
```

### 2.4 Customer Debt / Baki Ledger (`karbaar_baki`)
```typescript
interface BakiEntry {
  id: string;                // e.g. "b1", "b2"
  name: string;              // Customer name with title (e.g. "রফিকুল ইসলাম (শিক্ষক)")
  phone: string;             // WhatsApp-ready 11-digit mobile (e.g. "01712345678")
  desc: string;              // Itemized credit memo (e.g. "চাল, তেল ও চিনি বাকি")
  amount: number;            // Outstanding debt principal (৳)
  settled: boolean;          // Settlement flag (true when fully paid)
  createdAt: number;         // Creation epoch timestamp (ms)
  settledAt?: number;        // Payment resolution timestamp (ms)
}
```

### 2.5 Sales Demand Audit Stream (`karbaar_sales_log`)
Feeds the **DemandIQ Moving-Average Forecasting Engine**:
```typescript
interface SalesLogEntry {
  ts: number;                // Transaction epoch
  pid: string;               // Inventory item reference
  qty: number;               // Units depleted
}
```

### 2.6 Idempotency & Rollback Journal (`karbaar_undo_journal`)
```typescript
interface UndoRecord {
  id: string;                // Transaction ID
  action: 'add_tx' | 'add_baki' | 'collect_baki' | 'stock_update';
  snapshot: any;             // Reversible state payload
  ts: number;
}
```

---

## 3. Financial Integrity & Reconciliation Formulas

1. **Net Daily Sales:**
   $$\text{Daily Sales} = \sum_{\text{type} = \text{income}} \text{amount}$$
2. **True Cash Drawer Balance:**
   $$\text{Cash in Hand} = (\text{Cash Sales} + \text{Baki Collected}) - (\text{Inventory Purchases} + \text{Store Operational Expenses})$$
3. **Inventory Days of Cover:**
   $$\text{Days Remaining} = \frac{\text{Current Stock Units}}{\max(0.1, \text{Moving Average Daily Sales})}$$
4. **Weighted Average Cost Basis on Restock:**
   $$\text{New Average Cost} = \frac{(\text{Prior Stock} \times \text{Prior Cost}) + (\text{New Qty} \times \text{Purchase Price})}{\text{Prior Stock} + \text{New Qty}}$$
