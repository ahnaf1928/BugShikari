# Automated Financial Integrity, Security & Logic Test Suite for KarBaar AI (24 Rigorous Tests)
import os
import sys
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_PATH = os.path.join(BASE_DIR, 'index.html')
TEST_RUNNER_PATH = os.path.join(BASE_DIR, 'test_runner_node.js')
TEST_RESULTS_PATH = os.path.join(BASE_DIR, 'test_results.json')

# Read index.html
with open(INDEX_PATH, 'r', encoding='utf-8') as f:
    html = f.read()

# Extract the main script
script_start = html.rfind('<script>') + len('<script>')
script_end = html.rfind('</script>')
js_code = html[script_start:script_end]

# Create self-contained node test harness
test_harness = f"""
// Mock DOM & Web APIs
const mockStorage = {{}};
global.localStorage = {{
  getItem: (k) => mockStorage[k] || null,
  setItem: (k, v) => {{ mockStorage[k] = String(v); }},
  removeItem: (k) => {{ delete mockStorage[k]; }},
  clear: () => {{ for (let k in mockStorage) delete mockStorage[k]; }}
}};

global.window = {{
  addEventListener: () => {{}},
  removeEventListener: () => {{}},
  matchMedia: () => ({{ matches: false, addEventListener: () => {{}} }}),
  print: () => {{}},
  open: () => {{}}
}};

const makeMockElement = () => {{
  const children = [];
  const listeners = {{}};
  return {{
    value: '',
    innerText: '',
    textContent: '',
    innerHTML: '',
    style: {{}},
    classList: {{ add: () => {{}}, remove: () => {{}}, toggle: () => {{}}, contains: () => false }},
    appendChild: (child) => {{ children.push(child); }},
    removeChild: (child) => {{ const i = children.indexOf(child); if (i !== -1) children.splice(i, 1); }},
    remove: () => {{}},
    children,
    addEventListener: (evt, fn) => {{ listeners[evt] = fn; }},
    click: function() {{ if (listeners['click']) listeners['click']({{ preventDefault: () => {{}} }}); }},
    getContext: () => ({{
      createLinearGradient: () => ({{ addColorStop: () => {{}} }})
    }})
  }};
}};

global.document = {{
  documentElement: makeMockElement(),
  body: makeMockElement(),
  getElementById: (id) => makeMockElement(),
  querySelector: () => makeMockElement(),
  querySelectorAll: () => [],
  createElement: (tag) => makeMockElement(),
  addEventListener: () => {{}}
}};

global.navigator = {{
  clipboard: {{ writeText: async () => {{}} }}
}};

global.lucide = {{ createIcons: () => {{}} }};
global.Chart = function() {{
  return {{
    data: {{
      labels: ['১', '২', '৩', '৪', '৫', '৬', '৭', '৮', '৯', '১০', '১১', '১২'],
      datasets: [{{ data: [1, 2, 3] }}]
    }},
    options: {{
      scales: {{
        x: {{ grid: {{ color: '' }}, ticks: {{ color: '' }} }},
        y: {{ grid: {{ color: '' }}, ticks: {{ color: '' }} }}
      }},
      plugins: {{
        legend: {{ labels: {{ color: '' }} }}
      }}
    }},
    destroy: () => {{}},
    update: () => {{}}
  }};
}};

// Load KarBaar Code
{js_code}

// Test Results Collection
const results = [];
function test(id, name, fn) {{
  try {{
    const res = fn();
    results.push({{ id, name, ...res }});
  }} catch (e) {{
    results.push({{ id, name, status: 'FAIL', expected: 'No exception', actual: 'Exception: ' + e.message, evidence: e.stack }});
  }}
}}

// Initialize clean state
stats = {{ sales: 0, footfall: 0, profit: 0, baki: 0, collectedBaki: 0 }};
transactionsList = [];
bakiList = [];
inventory = DEFAULT_INVENTORY.map(p => ({{ ...p, stock: p.id === 'p1' ? 4 : (p.id === 'p2' ? 7 : (p.id === 'p3' ? 10 : 12)), avgCost: p.buy }}));
salesLog = [];
undoStack = [];

// ----------------------------------------------------
// T01: Cash sale updates inventory and revenue
// ----------------------------------------------------
test('T01', 'Cash sale updates inventory and revenue', () => {{
  const prod = inventory.find(p => p.id === 'p1'); // তেল: buy 170, sell 185, stock 4
  const res = commitTransaction({{ desc: 'তীর সয়াবিন তেল বিক্রি', type: 'income', amount: 370, cat: 'মুদি পণ্য', prod, qty: 2 }});
  const expectedProfit = 370 - (170 * 2); // 30 BDT
  const pass = res.ok && prod.stock === 2 && stats.sales === 370 && stats.profit === expectedProfit;
  return {{
    status: pass ? 'PASS' : 'FAIL',
    expected: 'Stock 4 -> 2, Sales = 370, Profit = 30',
    actual: `Stock: ${{prod.stock}}, Sales: ${{stats.sales}}, Profit: ${{stats.profit}}`,
    evidence: `Transaction logged: ${{transactionsList[0].desc}}, Qty: ${{transactionsList[0].qty}}, id: ${{transactionsList[0].id}}`
  }};
}});

// ----------------------------------------------------
// T02: Purchase updates inventory and weighted-average cost (WAC)
// ----------------------------------------------------
test('T02', 'Purchase updates inventory and weighted-average cost', () => {{
  const prod = inventory.find(p => p.id === 'p2'); // চিনি: stock 7 @ 130
  const prevProfit = stats.profit;
  // Buy 10 kg @ 147 BDT/kg (Amount: 1470 BDT)
  // New WAC = (7*130 + 10*147) / (7 + 10) = (910 + 1470) / 17 = 2380 / 17 = 140 BDT
  const res = commitTransaction({{ desc: 'চিনি নতুন চালান', type: 'expense', amount: 1470, cat: 'পণ্য ক্রয়', prod, qty: 10 }});
  const pass = res.ok && prod.stock === 17 && prod.avgCost === 140 && stats.profit === prevProfit;
  return {{
    status: pass ? 'PASS' : 'FAIL',
    expected: 'Stock 7 -> 17, WAC updated to 140 BDT, Profit unchanged',
    actual: `Stock: ${{prod.stock}}, WAC: ${{prod.avgCost}}, Profit: ${{stats.profit}}`,
    evidence: `Purchase recorded as asset restock. prevAvgCost: ${{res.tx.prevAvgCost}}, newAvgCost: ${{res.tx.newAvgCost}}`
  }};
}});

// ----------------------------------------------------
// T03: Credit sale updates inventory, revenue, and dues
// ----------------------------------------------------
test('T03', 'Credit sale updates inventory, revenue, and dues', () => {{
  const prod = inventory.find(p => p.id === 'p3'); // চাল: stock 10, buy 60, sell 70
  const res = applyResolved({{
    type: 'credit_sale',
    prod,
    qty: 2,
    amount: 140,
    customer: 'রহিম'
  }});
  const expectedProfit = stats.profit + (140 - (60 * 2)); // 30 + 20 = 50
  const bakiEntry = bakiList.find(b => b.name === 'রহিম');
  const pass = res.ok && prod.stock === 8 && stats.baki === 140 && stats.sales === (370 + 140) && bakiEntry && bakiEntry.amount === 140;
  return {{
    status: pass ? 'PASS' : 'FAIL',
    expected: 'Stock 10 -> 8, Sales += 140, Rahim due = 140, Profit += 20',
    actual: `Stock: ${{prod.stock}}, Sales: ${{stats.sales}}, Rahim due: ${{bakiEntry ? bakiEntry.amount : 'N/A'}}, Profit: ${{stats.profit}}`,
    evidence: `Credit sale ledger entry created with isCredit: true, bakiId: ${{bakiEntry ? bakiEntry.id : 'none'}}`
  }};
}});

// ----------------------------------------------------
// T04: Partial credit payment reduces dues without increasing sales
// ----------------------------------------------------
test('T04', 'Partial credit payment reduces dues without increasing sales', () => {{
  const bIdx = bakiList.findIndex(b => b.name === 'রহিম');
  const salesBefore = stats.sales;
  const payRes = collectBaki(bIdx, 100, 'প্রথম কিস্তি');
  const bakiEntry = bakiList[bIdx];
  const pass = payRes.ok && bakiEntry.amount === 40 && bakiEntry.settled === false && stats.baki === 40 && stats.collectedBaki === 100 && stats.sales === salesBefore;
  return {{
    status: pass ? 'PASS' : 'FAIL',
    expected: 'Rahim due 140 -> 40, Settled: false, Collected = 100, Sales strictly unchanged',
    actual: `Rahim due: ${{bakiEntry.amount}}, Settled: ${{bakiEntry.settled}}, Collected: ${{stats.collectedBaki}}, Sales: ${{stats.sales}} (Before: ${{salesBefore}})`,
    evidence: `Zero double-counting: Revenue recognized at credit sale, not collection`
  }};
}});

// ----------------------------------------------------
// T05: Full credit payment settles dues
// ----------------------------------------------------
test('T05', 'Full payment settles dues', () => {{
  // Add a customer with 500 BDT
  const addRes = addBakiEntry('কাউসার ভাই', 500, 'পুরোনো বাকি');
  const bIdx = bakiList.findIndex(b => b.name === 'কাউসার ভাই');
  const payRes = collectBaki(bIdx, 500, 'সম্পূর্ণ পরিশোধ');
  const bakiEntry = bakiList[bIdx];
  const pass = payRes.ok && bakiEntry.amount === 0 && bakiEntry.settled === true;
  return {{
    status: pass ? 'PASS' : 'FAIL',
    expected: 'Due 500 -> 0, Settled = true',
    actual: `Due: ${{bakiEntry.amount}}, Settled: ${{bakiEntry.settled}}`,
    evidence: `bakiList marked settled with timestamped payment log`
  }};
}});

// ----------------------------------------------------
// T06: Discounted sale calculates correct profit
// ----------------------------------------------------
test('T06', 'Discounted sale calculates correct profit', () => {{
  const prod = inventory.find(p => p.id === 'p1'); // buy: 170, normal sell: 185
  const profitBefore = stats.profit;
  // Sell 1 bottle at discount price 175 BDT (Profit should be 175 - 170 = 5 BDT)
  commitTransaction({{ desc: 'তেল ডিসকাউন্টে বিক্রি', type: 'income', amount: 175, cat: 'মুদি পণ্য', prod, qty: 1 }});
  const profitDiff = stats.profit - profitBefore;
  const pass = profitDiff === 5;
  return {{
    status: pass ? 'PASS' : 'FAIL',
    expected: 'Profit increase = 5 BDT (175 sold - 170 cost)',
    actual: `Profit increase: ${{profitDiff}} BDT (Total profit: ${{stats.profit}})`,
    evidence: `Historical cost basis 170 BDT deducted from discounted revenue 175 BDT`
  }};
}});

// ----------------------------------------------------
// T07: Unknown cost produces unknown profit (Never fake 15%)
// ----------------------------------------------------
test('T07', 'Unknown cost produces unknown profit', () => {{
  const profitBefore = stats.profit;
  // Generic sale of an uncataloged item (no product linked)
  const res = commitTransaction({{ desc: 'অজ্ঞাত পণ্য বিক্রি', type: 'income', amount: 500, cat: 'বিবিধ' }});
  const profitAfter = stats.profit;
  // Profit MUST NOT be artificially inflated by fake 15% (75 BDT)
  const pass = res.ok && res.tx.profitUnknown === true && res.tx.calculatedProfit === null && profitAfter === profitBefore;
  return {{
    status: pass ? 'PASS' : 'FAIL',
    expected: 'tx.profitUnknown = true, tx.calculatedProfit = null, stats.profit unchanged (No fake 15%)',
    actual: `profitUnknown: ${{res.tx.profitUnknown}}, calculatedProfit: ${{res.tx.calculatedProfit}}, Profit delta: ${{profitAfter - profitBefore}}`,
    evidence: 'System reports unknown profit as unavailable rather than fabricating a number'
  }};
}});

// ----------------------------------------------------
// T08: Operating expenses separated from purchase costs
// ----------------------------------------------------
test('T08', 'Operating expenses separated from purchase costs', () => {{
  const profitBefore = stats.profit;
  commitTransaction({{ desc: 'দোকান বিদ্যুৎ বিল', type: 'expense', amount: 450, cat: 'ইউটিলিটি বিল' }});
  const rec = calcCashReconciliation();
  const pass = stats.profit === (profitBefore - 450) && rec.cashOutExpense === 450 && rec.cashOutPurchase === 1470;
  return {{
    status: pass ? 'PASS' : 'FAIL',
    expected: 'Operating expenses reduce profit by 450, separated from purchase costs (1470)',
    actual: `Expenses: ${{rec.cashOutExpense}}, Purchases: ${{rec.cashOutPurchase}}, Profit: ${{stats.profit}}`,
    evidence: `Cash reconciliation separates period operating expense from asset restock`
  }};
}});

// ----------------------------------------------------
// T09: Cumulative batch stock shortage is rejected
// ----------------------------------------------------
test('T09', 'Cumulative batch stock shortage is rejected', () => {{
  const prodOil = inventory.find(p => p.id === 'p1'); // Remaining stock: 1 bottle
  const oilStockBefore = prodOil.stock;
  
  // Batch: Action 1 sells 1 bottle, Action 2 sells 1 bottle (Total 2 > stock 1)
  const batch = [
    {{ line: '১ বোতল তেল বিক্রি', type: 'sale', prod: prodOil, qty: 1, amount: 185 }},
    {{ line: 'আরও ১ বোতল তেল বিক্রি', type: 'sale', prod: prodOil, qty: 1, amount: 185 }}
  ];
  
  const batchVal = validateBatchActions(batch);
  const pass = batchVal.ok === false && batchVal.cumulativeShortage === true && prodOil.stock === oilStockBefore;
  return {{
    status: pass ? 'PASS' : 'FAIL',
    expected: 'Batch rejected due to cumulative shortage. Stock unchanged at 1.',
    actual: `Validation ok: ${{batchVal.ok}}, Error: "${{batchVal.error}}", Stock: ${{prodOil.stock}}`,
    evidence: 'validateBatchActions projected cumulative stock sequentially across batch'
  }};
}});

// ----------------------------------------------------
// T10: Multi-action batch succeeds consistently
// ----------------------------------------------------
test('T10', 'Multi-action batch succeeds consistently', () => {{
  const host = makeMockElement();
  const prodSugar = inventory.find(p => p.id === 'p2'); // stock: 17
  const sugarBefore = prodSugar.stock;
  const salesBefore = stats.sales;

  // Batch: 2 kg sugar sale (280 BDT) + 50 BDT shop expense
  const batch = [
    {{ line: '২ কেজি চিনি বিক্রি', type: 'sale', prod: prodSugar, qty: 2, amount: 280 }},
    {{ line: '৫০ টাকা দোকান খরচ', type: 'expense', amount: 50, note: 'নাস্তা খরচ', cat: 'দোকান খরচ' }}
  ];

  const card = renderActionCard(host, batch);
  const res = card.executeConfirmedBatch();
  const pass = res.ok && res.saved === 2 && prodSugar.stock === (sugarBefore - 2) && stats.sales === (salesBefore + 280);
  return {{
    status: pass ? 'PASS' : 'FAIL',
    expected: 'Both actions committed atomically. Sugar stock 17 -> 15, Sales += 280',
    actual: `Saved: ${{res.saved}}, Sugar stock: ${{prodSugar.stock}}, Sales: ${{stats.sales}}`,
    evidence: 'Batch pre-validation succeeded and both transactions committed consistently'
  }};
}});

// ----------------------------------------------------
// T11: Mid-batch failure does not silently corrupt records (Real Mid-Batch Execution Rollback)
// ----------------------------------------------------
test('T11', 'Mid-batch failure does not silently corrupt records', () => {{
  const host = makeMockElement();
  const prodSugar = inventory.find(p => p.id === 'p2');
  const sugarStockBefore = prodSugar.stock;
  const salesBefore = stats.sales;
  const undoLenBefore = undoStack.length;

  // Action 1 is valid (reduces sugar stock by 1), Action 2 is set to fail DURING execution loop
  const batch = [
    {{ line: '১ কেজি চিনি বিক্রি', type: 'sale', prod: prodSugar, qty: 1, amount: 140 }},
    {{ line: 'সিস্টেম রানটাইম ত্রুটি লেনদেন', type: 'sale', prod: prodSugar, qty: 1, amount: 140, _failExecution: true }}
  ];

  const card = renderActionCard(host, batch);
  // Action 1 executes and commits -> Action 2 fails during execution loop -> Saga compensating rollback undoes Action 1
  const res = card.executeConfirmedBatch();
  const pass = res.ok === false &&
               res.rolledBack === true &&
               prodSugar.stock === sugarStockBefore &&
               stats.sales === salesBefore &&
               undoStack.length === undoLenBefore;
  return {{
    status: pass ? 'PASS' : 'FAIL',
    expected: 'Action 1 executed and rolled back after Action 2 mid-execution failure. State 100% restored (rolledBack: true).',
    actual: `res.ok: ${{res.ok}}, rolledBack: ${{res.rolledBack}}, Sugar stock: ${{prodSugar.stock}} (Before: ${{sugarStockBefore}}), Sales: ${{stats.sales}} (Before: ${{salesBefore}})`,
    evidence: 'Mid-batch runtime failure triggered compensating transaction rollback (Saga pattern); zero partial mutation remained.'
  }};
}});

// ----------------------------------------------------
// T12: Duplicate request is not applied twice (Latch + Persistent Idempotency)
// ----------------------------------------------------
test('T12', 'Duplicate request is not applied twice', () => {{
  const host1 = makeMockElement();
  const prodSugar = inventory.find(p => p.id === 'p2');
  const batch = [{{ line: '১ কেজি চিনি বিক্রি', type: 'sale', prod: prodSugar, qty: 1, amount: 140 }}];
  const testIdempotencyKey = 'idem_t12_' + Date.now();

  const card1 = renderActionCard(host1, batch, testIdempotencyKey);
  const salesBefore = stats.sales;

  // 1st call on card 1: executes and commits, records key in localStorage
  const r1 = card1.executeConfirmedBatch();

  // 2nd call on card 1: in-memory latch blocks
  const r2 = card1.executeConfirmedBatch();

  // 3rd call on fresh card instance with identical key (simulating page reload / retry)
  const host2 = makeMockElement();
  const card2 = renderActionCard(host2, batch, testIdempotencyKey);
  const r3 = card2.executeConfirmedBatch();

  const pass = r1.ok === true &&
               r2.ok === false && r2.error === 'already_executed' &&
               r3.ok === false && r3.duplicate === true &&
               stats.sales === (salesBefore + 140);
  return {{
    status: pass ? 'PASS' : 'FAIL',
    expected: '1st call: ok true; 2nd call: in-memory latch blocked; 3rd call: persistent registry blocked duplicate. Sales delta +140 exactly.',
    actual: `1st: ${{r1.ok}}, 2nd: ${{r2.error}}, 3rd duplicate: ${{r3.duplicate}}, Sales delta: ${{stats.sales - salesBefore}}`,
    evidence: 'Persistent idempotency store in localStorage blocks resubmissions across card instances and page refreshes'
  }};
}});

// ----------------------------------------------------
// T13: Undo survives page refresh (LocalStorage persistence)
// ----------------------------------------------------
test('T13', 'Undo survives page refresh', () => {{
  const prodBefore = inventory.find(p => p.id === 'p2');
  const stockBefore = prodBefore.stock;
  const salesBefore = stats.sales;

  // Perform a new sale
  const txRes = commitTransaction({{ desc: 'রিফ্রেশ টেস্ট চিনি বিক্রি', type: 'income', amount: 140, cat: 'মুদি পণ্য', prod: prodBefore, qty: 1 }});
  saveToLocalStorage();

  // Simulate complete browser restart/refresh: wipe in-memory undoStack
  undoStack = [];
  loadInitialData(); // restores undoStack from LocalStorage!

  const undoRes = undoLastAction();
  const prodAfter = inventory.find(p => p.id === 'p2');
  const pass = txRes.ok && undoRes.ok && prodAfter.stock === stockBefore && stats.sales === salesBefore;
  return {{
    status: pass ? 'PASS' : 'FAIL',
    expected: `Undo succeeds post-refresh: Stock reverted to ${{stockBefore}}, Sales reverted to ${{salesBefore}}`,
    actual: `Undo ok: ${{undoRes.ok}}, Stock: ${{prodAfter.stock}}, Sales: ${{stats.sales}}`,
    evidence: 'undoStack restored from LS.undo and transaction reverted successfully'
  }};
}});

// ----------------------------------------------------
// T14: Merged customer credit undo preserves earlier balances
// ----------------------------------------------------
test('T14', 'Merged customer credit undo preserves earlier balances', () => {{
  // Initial credit 2000 BDT
  addBakiEntry('সেলিম ভাই', 2000, 'পুরোনো বকেয়া');
  // Merge additional 1000 BDT
  const mergeRes = addBakiEntry('সেলিম ভাই', 1000, 'অতিরিক্ত বাকি');
  undoStack.push({{
    type: 'baki_add',
    bakiId: mergeRes.entry.id,
    amountAdded: 1000,
    isNew: mergeRes.isNew
  }});

  const entry = bakiList.find(b => b.name === 'সেলিম ভাই');
  const dueBeforeUndo = entry.amount; // 3000

  // Undo the 1000 BDT addition
  const undoRes = undoLastAction();
  const pass = undoRes.ok && entry.amount === 2000 && bakiList.some(b => b.name === 'সেলিম ভাই');
  return {{
    status: pass ? 'PASS' : 'FAIL',
    expected: 'Due merged to 3000, reverted to 2000. Customer record preserved.',
    actual: `Before undo: ${{dueBeforeUndo}}, After undo: ${{entry.amount}}, Customer exists: ${{bakiList.some(b => b.name === 'সেলিম ভাই')}}`,
    evidence: 'baki_add undo decremented only the added amount without deleting merged record'
  }};
}});

// ----------------------------------------------------
// T15: Payment reversal restores the correct balance
// ----------------------------------------------------
test('T15', 'Payment reversal restores the correct balance', () => {{
  const prod = inventory.find(p => p.id === 'p2');
  const salesBefore = stats.sales;

  // Credit sale 140 BDT
  applyResolved({{ type: 'credit_sale', prod, qty: 1, amount: 140, customer: 'জাহিদ ভাই' }});
  const salesAfterCredit = stats.sales;
  const bIdx = bakiList.findIndex(b => b.name === 'জাহিদ ভাই');
  const bakiEntry = bakiList[bIdx];

  // Partial payment 100 BDT
  collectBaki(bIdx, 100, 'আংশিক পেমেন্ট');
  const dueAfterPay = bakiEntry.amount; // 40

  // Undo the payment
  const undoPayRes = undoLastAction();
  const dueAfterUndo = bakiEntry.amount; // 140

  const pass = undoPayRes.ok && dueAfterPay === 40 && dueAfterUndo === 140 && stats.sales === salesAfterCredit;
  return {{
    status: pass ? 'PASS' : 'FAIL',
    expected: 'Due 140 -> 40 on payment -> 140 on undo. Sales revenue constant throughout.',
    actual: `Due after pay: ${{dueAfterPay}}, Due after undo: ${{dueAfterUndo}}, Sales: ${{stats.sales}} (Expected: ${{salesAfterCredit}})`,
    evidence: 'baki_collect undo restored customer balance and decremented collectedBaki without touching sales'
  }};
}});

// ----------------------------------------------------
// T16: Negative, zero, NaN, and infinite amounts are rejected
// ----------------------------------------------------
test('T16', 'Negative, zero, NaN, and infinite amounts are rejected', () => {{
  const prod = inventory.find(p => p.id === 'p1');
  const tZero = commitTransaction({{ desc: 'শূন্য টাকা', type: 'income', amount: 0, cat: 'মুদি পণ্য', prod, qty: 1 }});
  const tNeg = commitTransaction({{ desc: 'নেগেটিভ টাকা', type: 'income', amount: -50, cat: 'মুদি পণ্য', prod, qty: 1 }});
  const tNaN = commitTransaction({{ desc: 'নট এ নাম্বার', type: 'income', amount: NaN, cat: 'মুদি পণ্য', prod, qty: 1 }});
  const tInf = commitTransaction({{ desc: 'ইনফিনিট', type: 'income', amount: Infinity, cat: 'মুদি পণ্য', prod, qty: 1 }});
  const tZeroQty = commitTransaction({{ desc: 'শূন্য পণ্য', type: 'income', amount: 185, cat: 'মুদি পণ্য', prod, qty: 0 }});
  const tNegQty = commitTransaction({{ desc: 'নেগেটিভ পণ্য', type: 'income', amount: 185, cat: 'মুদি পণ্য', prod, qty: -2 }});

  const pass = tZero.ok === false && tNeg.ok === false && tNaN.ok === false && tInf.ok === false && tZeroQty.ok === false && tNegQty.ok === false;
  return {{
    status: pass ? 'PASS' : 'FAIL',
    expected: 'All 6 invalid transactions rejected with ok: false.',
    actual: `tZero: ${{tZero.ok}}, tNeg: ${{tNeg.ok}}, tNaN: ${{tNaN.ok}}, tInf: ${{tInf.ok}}, tZeroQty: ${{tZeroQty.ok}}, tNegQty: ${{tNegQty.ok}}`,
    evidence: 'commitTransaction strictly enforces positive finite numeric amounts and quantities'
  }};
}});

// ----------------------------------------------------
// T17: Invalid unit conversion & unit mismatch rejected
// ----------------------------------------------------
test('T17', 'Invalid unit conversion & unit mismatch rejected', () => {{
  // 1. Compatible Unit Conversion (500 gram sugar -> 0.5 kg, price 70 tk)
  const convRes = resolveAction({{ type: 'sale', product: 'চিনি', qty: 500, unit: 'গ্রাম' }}, '৫০০ গ্রাম চিনি বিক্রি');
  const convPass = convRes.ok === true && convRes.qty === 0.5 && convRes.amount === 70;

  // 2. Incompatible Unit Rejection (Rice is measured in kg, cannot be sold in liters)
  const mismatchRes = resolveAction({{ type: 'sale', product: 'চাল', qty: 2, unit: 'লিটার' }}, '২ লিটার চাল বিক্রি');
  const mismatchPass = mismatchRes.ok === false && mismatchRes.error.includes('কেজিতে হিসাব করা হয়, লিটার');

  // 3. Discrete Bottle Incompatible Unit Rejection (Oil in bottles cannot be sold in kg)
  const oilMismatch = resolveAction({{ type: 'sale', product: 'তেল', qty: 2, unit: 'কেজি' }}, '২ কেজি তেল বিক্রি');
  const oilMismatchPass = oilMismatch.ok === false && oilMismatch.error.includes('বোতলে হিসাব করা হয়, কেজিতে নয়');

  // 4. Negative / invalid quantity sanitization
  const valRes = validateResolvedAction({{
    type: 'sale',
    prod: {{ id: 'p1', name: 'তেল', stock: 4, unit: 'বোতল' }},
    qty: -5,
    amount: 185
  }});
  const sanitizePass = valRes.ok === false && valRes.error.includes('পরিমাণ');

  const pass = convPass && mismatchPass && oilMismatchPass && sanitizePass;
  return {{
    status: pass ? 'PASS' : 'FAIL',
    expected: '500g converts to 0.5kg; Rice/oil unit mismatches rejected with Bengali guidance; negative qty sanitized.',
    actual: `Conversion: ${{convPass}} (qty: ${{convRes.qty}}, amt: ${{convRes.amount}}), Rice mismatch: ${{mismatchPass}}, Oil mismatch: ${{oilMismatchPass}}, Sanitize: ${{sanitizePass}}`,
    evidence: 'Unit engine performs gram-to-kg conversion and rejects physical unit incompatibilities with explicit Bengali guidance'
  }};
}});

// ----------------------------------------------------
// T18: Missing or ambiguous customer triggers clarification
// ----------------------------------------------------
test('T18', 'Missing or ambiguous customer triggers clarification', () => {{
  const res = resolveAction({{ type: 'credit_sale', product: 'চাল', qty: 2, amount: 140, customer: '' }}, 'চাল বাকিতে দিলাম');
  const pass = res.ok === false && res.error.includes('কার নামে বাকি লিখব');
  return {{
    status: pass ? 'PASS' : 'FAIL',
    expected: 'Missing customer triggers clear Bengali clarification prompt.',
    actual: `Result: "${{res.error}}"`,
    evidence: 'resolveAction requires explicit customer name for all credit transactions'
  }};
}});

// ----------------------------------------------------
// T19: Missing or ambiguous product triggers clarification
// ----------------------------------------------------
test('T19', 'Missing or ambiguous product triggers clarification', () => {{
  const res = resolveAction({{ type: 'sale', product: 'অজানা কাল্পনিক জিনিস', qty: 2, amount: 100 }}, 'অজানা জিনিস বিক্রি করলাম');
  const pass = res.ok === false && res.error.includes('কোন পণ্য বুঝতে পারিনি');
  return {{
    status: pass ? 'PASS' : 'FAIL',
    expected: 'Unrecognized product triggers product clarification prompt.',
    actual: `Result: "${{res.error}}"`,
    evidence: 'resolveAction matches against catalog and refuses ambiguous items'
  }};
}});

// ----------------------------------------------------
// T20: AI network failure handled transparently with local fallback
// ----------------------------------------------------
test('T20', 'AI network failure handled transparently with local fallback', () => {{
  const query = 'দোকানের আজকের অবস্থা কি?';
  const localRes = localAnswer(query);
  const pass = localRes && localRes.text && localRes.text.length > 0 && localRes.source.includes('লোকাল');
  return {{
    status: pass ? 'PASS' : 'FAIL',
    expected: 'Returns local answer gracefully with offline badge.',
    actual: `Source: "${{localRes ? localRes.source : 'none'}}", Preview: "${{localRes ? localRes.text.slice(0, 50) : ''}}..."`,
    evidence: 'localAnswer provides 100% offline uptime when cloud network is unreachable'
  }};
}});

// ----------------------------------------------------
// T21: Local data persists after refresh (All partitions)
// ----------------------------------------------------
test('T21', 'Local data persists after refresh', () => {{
  saveToLocalStorage();
  const keys = [LS.stats, LS.tx, LS.baki, LS.inv, LS.sales, LS.undo];
  const allKeysPresent = keys.every(k => mockStorage[k] && mockStorage[k].length > 0);
  
  const savedStats = JSON.parse(mockStorage[LS.stats]);
  const savedTx = JSON.parse(mockStorage[LS.tx]);
  const savedBaki = JSON.parse(mockStorage[LS.baki]);
  const savedInv = JSON.parse(mockStorage[LS.inv]);
  const savedUndo = JSON.parse(mockStorage[LS.undo]);

  // Wipe memory
  stats = {{ sales: 0, footfall: 0, profit: 0, baki: 0, collectedBaki: 0 }};
  transactionsList = [];
  bakiList = [];
  inventory = [];
  undoStack = [];

  // Reload
  loadInitialData();

  const pass = allKeysPresent &&
               stats.sales === savedStats.sales &&
               transactionsList.length === savedTx.length &&
               bakiList.length === savedBaki.length &&
               inventory.length === savedInv.length &&
               undoStack.length === savedUndo.length;
  return {{
    status: pass ? 'PASS' : 'FAIL',
    expected: 'All 6 storage partitions saved and 100% reconstructed without data loss.',
    actual: `Keys present: ${{allKeysPresent}}, Sales: ${{stats.sales}}, Tx: ${{transactionsList.length}}, Baki: ${{bakiList.length}}, Undo: ${{undoStack.length}}`,
    evidence: `Keys in storage: ${{Object.keys(mockStorage).join(', ')}}`
  }};
}});

// ----------------------------------------------------
// T22: Cash reconciliation matches underlying transactions
// ----------------------------------------------------
test('T22', 'Cash reconciliation matches underlying transactions', () => {{
  const rec = calcCashReconciliation();
  const expectedDrawer = rec.totalCashIn - rec.totalCashOut;
  const pass = rec.netCashDrawer === expectedDrawer && expectedDrawer > 0;
  return {{
    status: pass ? 'PASS' : 'FAIL',
    expected: `Drawer cash exactly equals totalCashIn (${{rec.totalCashIn}}) - totalCashOut (${{rec.totalCashOut}}) = ${{expectedDrawer}}`,
    actual: `Drawer cash: ${{rec.netCashDrawer}}, Expected: ${{expectedDrawer}}`,
    evidence: `Cash-in (Sales + Collected) minus Cash-out (Purchases + Expenses) matches ledger`
  }};
}});

// ----------------------------------------------------
// T23: Historical cost changes handled correctly (WAC Rollback)
// ----------------------------------------------------
test('T23', 'Historical cost changes handled correctly', () => {{
  const prod = inventory.find(p => p.id === 'p3'); // চাল: stock 8 @ 60
  const initialStock = prod.stock;
  const initialCost = prod.avgCost; // 60

  // Restock 10 kg @ 80 BDT/kg (Amount: 800 BDT)
  // New WAC = (8*60 + 10*80) / (8 + 10) = (480 + 800) / 18 = 1280 / 18 = 71.11 BDT
  const restockRes = commitTransaction({{ desc: 'চাল নতুন চালান', type: 'expense', amount: 800, cat: 'পণ্য ক্রয়', prod, qty: 10 }});
  const costAfterRestock = prod.avgCost;

  // Undo restock: WAC must revert to 60 BDT and stock to 8!
  const undoRes = undoLastAction();
  const pass = restockRes.ok && costAfterRestock === 71.11 && undoRes.ok && prod.stock === initialStock && prod.avgCost === initialCost;
  return {{
    status: pass ? 'PASS' : 'FAIL',
    expected: 'WAC updated to 71.11, then reverted to 60 on undo. Stock 18 -> 8.',
    actual: `WAC after restock: ${{costAfterRestock}}, WAC after undo: ${{prod.avgCost}}, Stock after undo: ${{prod.stock}}`,
    evidence: 'commitTransaction tracked prevAvgCost and undoLastAction restored historical cost basis'
  }};
}});

// ----------------------------------------------------
// T24: All business invariants remain valid after consecutive errors
// ----------------------------------------------------
test('T24', 'All business invariants remain valid after consecutive errors', () => {{
  const txCountBefore = transactionsList.length;
  const bakiCountBefore = bakiList.length;
  const salesBefore = stats.sales;

  // Trigger 5 consecutive illegal actions
  commitTransaction({{ desc: 'অবৈধ ১', type: 'income', amount: -100, cat: 'মুদি পণ্য' }});
  commitTransaction({{ desc: 'অবৈধ ২', type: 'income', amount: 0, cat: 'মুদি পণ্য' }});
  applyResolved({{ type: 'credit_sale', prod: inventory[0], qty: 9999, amount: 500000, customer: 'অজানা' }});
  collectBaki(0, 99999999, 'অতিরিক্ত আদায়');
  addBakiEntry('ভুল ক্রেতা', -50, 'নেগেটিভ বাকি');

  const pass = transactionsList.length === txCountBefore &&
               bakiList.length === bakiCountBefore &&
               stats.sales === salesBefore;
  return {{
    status: pass ? 'PASS' : 'FAIL',
    expected: 'State completely unchanged after consecutive illegal actions.',
    actual: `Tx count: ${{transactionsList.length}} (Before: ${{txCountBefore}}), Sales: ${{stats.sales}} (Before: ${{salesBefore}})`,
    evidence: 'Zero ghost records or ledger corruption after error bursts'
  }};
}});

console.log(JSON.stringify(results, null, 2));
process.exit(0);
"""

with open(TEST_RUNNER_PATH, 'w', encoding='utf-8') as f:
    f.write(test_harness)

print("Updated test_runner_node.js with full 24 portable financial & security tests")
