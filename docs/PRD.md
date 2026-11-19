# 📋 Product Requirements Document (PRD) — KarBaar (কারবার)

> **Document Version:** 2.0.0 (Production Candidate)  
> **Target Domain:** CommerceSphere AI | **Challenge:** DemandIQ  
> **Team:** BugShikari  
> **Target Audience:** Micro, Small & Medium Enterprise (CMSME) Retailers in Bangladesh  

---

## 1. Executive Summary & Problem Definition

### 1.1 The CMSME Retail Crisis in Bangladesh
Bangladesh has approximately **7.8 million Cottage, Micro, Small, and Medium Enterprises (CMSMEs)**, with neighborhood grocery stores (*Mudi Dokan*) forming the backbone of informal retail commerce. Despite powering over $18 billion in annual trade, more than **80% of these shopkeepers still rely on physical paper ledgers (*Laal Baki Khata*)** and mental arithmetic.

### 1.2 Core Pain Points
1. **Cash Flow Blindness:** Shopkeepers cannot tell their true net profit at the end of the day because credit sales, cash sales, supplier restocking costs, and personal pocket withdrawals are jumbled together.
2. **Dead Capital in Unrecovered Credit (*Baki*):** 15% to 22% of working capital is perpetually locked up in uncollected customer credit. Asking for overdue payments verbally feels socially awkward (*Lojja*), causing delays until accounts turn bad.
3. **Unplanned Stockouts & Food Waste:** Lack of seasonal demand forecasting causes popular items (e.g., soybean oil, lentils, sugar) to run out unexpectedly while slow-moving items gather dust and expire.
4. **Digital Literacy & Interface Barrier:** Existing accounting software and POS apps require typing, navigating complex dropdowns, and filling forms—tasks impossible for a busy shopkeeper attending customers with flour-dusted hands.

### 1.3 Value Proposition
**KarBaar is Bangladesh’s first Voice-First Bengali AI Business Operator.** It transforms natural spoken Bengali into structured, double-entry financial transactions, automates credit collection via WhatsApp, and provides AI-driven seasonal demand forecasting—all through an ultra-fast, zero-build Progressive Web App (PWA).

---

## 2. User Personas & Core Journeys

### 2.1 Persona: Rahman Bhai (The Neighborhood Grocer)
- **Age:** 42 | **Location:** Chawkbazar, Old Dhaka
- **Business:** Traditional grocery store with ~350 distinct SKUs
- **Tech Literacy:** Uses Android smartphone for YouTube and WhatsApp; hates typing Bengali on a virtual keyboard.
- **Goal:** Know exact daily net profit, keep inventory stocked before Ramadan, and collect customer dues without confrontation.

### 2.2 Core User Journey (Voice-to-Transaction)
1. **Spoken Intent:** Rahman Bhai taps the floating microphone and speaks naturally: *"কাউসার ভাইকে ২ বস্তা মিনিকেট চাল বাকি দিলাম আর ৫০ টাকা দোকান খরচ হলো।"*
2. **Instant Parsing:** KarBaar’s speech recognition and semantic parser extract two concurrent actions:
   - Action A: Credit Sale (`item: "মিনিকেট চাল"`, `qty: 2`, `customer: "কাউসার ভাই"`, `type: "baki"`)
   - Action B: Expense (`amount: 50`, `category: "দোকান খরচ"`, `type: "expense"`)
3. **Human-in-the-Loop Confirmation:** A tactile confirmation card appears showing exact stock deduction, ledger debit, and net cash impact.
4. **One-Tap Commit:** Rahman Bhai taps "নিশ্চিত করুন" (or speaks *"হ্যাঁ"*).
5. **Real-Time Ledger Update:** Stock drops from 12 to 10 sacks, Baki increases by 7,300৳, cash drawer subtracts 50৳, and stats sync instantly.

---

## 3. Product Features & Functional Requirements

| Module | Feature | Functional Description | Priority |
| :--- | :--- | :--- | :---: |
| **F01: Voice Operator** | Bengali Speech Recognition | Continuous listening via Web Speech API (`bn-BD`) with fuzzy phonetic fallback tokenizer. | P0 (Must Have) |
| **F02: Voice Operator** | Multi-Action Parsing | Decomposes compound spoken sentences into discrete sales, baki, purchase, and expense intents. | P0 (Must Have) |
| **F03: Financial Core** | Real-Time Cash Reconciliation | Dynamic calculation: `Drawer Cash = (Cash In - Cash Out)`, distinguishing cash revenue from credit accruals. | P0 (Must Have) |
| **F04: Digital Baki** | Customer Credit Ledger | Tracks individual customer debt, repayment dates, transaction history, and partial debt collections. | P0 (Must Have) |
| **F05: Digital Baki** | WhatsApp Automated Dunning | Generates polite, culturally respectful Bengali reminder templates and opens WhatsApp Web/App in 1 click. | P0 (Must Have) |
| **F06: DemandIQ** | Seasonal Stock Predictor | Analyzes upcoming festivals (Ramadan, Eid-ul-Fitr, Winter) to forecast SKU surges and prevent stockouts. | P0 (Must Have) |
| **F07: Safety & UX** | Single-Click Undo (LIFO) | Immediate rollback of mistakenly committed sales, restoring inventory counts and ledger numbers. | P0 (Must Have) |
| **F08: Security** | Zero Client Key Leakage | Backend Serverless AI Proxy hides Gemini API credentials completely from client-side network inspectors. | P0 (Must Have) |
| **F09: Offline Engine** | Hybrid Edge Resilience | Fallback local rule-based intelligence when internet is offline or API quota is throttled. | P1 (Must Have) |
| **F10: Data Sovereignty** | Local JSON Backup/Restore | One-click encrypted JSON export and import for 100% merchant data portability. | P1 (Should Have) |

---

## 4. Non-Functional Requirements (NFR)

1. **Performance & Latency:**
   - Client initial load time $< 1.2\text{s}$ on 3G mobile networks.
   - Voice parsing and confirmation card render time $< 450\text{ms}$.
   - Zero-build client bundle size $< 300\text{KB}$ uncompressed.
2. **Reliability & Availability:**
   - 100% uptime through static Edge CDN distribution (Netlify).
   - Graceful offline degradation for all core bookkeeping functions.
3. **Security & Rate Limiting:**
   - Strict serverless rate limiting: maximum 20 requests per minute per IP address.
   - Payload guard: maximum 50,000 bytes per request (prevents buffer overflow/DDoS).
   - Strict HTTP headers: `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`.
4. **Accessibility & Localization:**
   - High-contrast visual tokens designed for outdoor glare and dim indoor incandescent bulbs.
   - Primary language: 100% authentic Bengali typography (Nirmala UI / Tiro Bangla).

---

## 5. Scope & Success Metrics (Hackathon Evaluation Criteria)

- **MVP Scope:** Full Voice-to-Sale flow, Digital Baki ledger with WhatsApp reminder, DemandIQ stock forecast, 11/11 verified financial audit tests, and responsive dark/light UI.
- **Success Criteria:**
  - Zero hallucination on financial numbers (100% test pass rate).
  - Client API key exposure: **0%**.
  - Preliminary pitch compliance: exactly 3-minute video presentation adhering to AIBC guidelines.
