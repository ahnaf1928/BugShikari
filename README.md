# 🛒 Karbaar AI (কারবার) — Bengali AI Business Operator & Digital Ledger

[![Netlify Live](https://img.shields.io/badge/Live-karbaar.netlify.app-00C7B7?style=for-the-badge&logo=netlify)](https://karbaar.netlify.app)
[![AI Engine](https://img.shields.io/badge/AI-Google_Gemini_3.5_Flash_Lite-4285F4?style=for-the-badge&logo=google)](https://ai.google.dev/)
[![Stack](https://img.shields.io/badge/Architecture-PWA_SPA_Serverless-7c3aed?style=for-the-badge)](#)
[![Tests](https://img.shields.io/badge/Financial_Integrity_Tests-24%2F24_PASS-success?style=for-the-badge)](#)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](#)

> **"কারবার শুধু একটি দোকান ম্যানেজমেন্ট ড্যাশবোর্ড নয়; এটি বাংলাদেশের ক্ষুদ্র ও মাঝারি ব্যবসায়ীদের জন্য একটি ভয়েস-ফার্স্ট বাংলা AI বিজনেস অপারেটর — যা মুখের স্বাভাবিক কথাকে নির্ভুল ব্যবসায়িক লেনদেনে রূপান্তর করে।"**

---


---

## 📚 অফিশিয়াল ডকুমেন্টেশন স্যুট (Official Documentation Suite)

হ্যাকাথন রুলবুক ও এন্টারপ্রাইজ স্ট্যান্ডার্ড অনুযায়ী প্রজেক্টের প্রতিটি ডোমেইনের জন্য স্বয়ংসম্পূর্ণ স্পেসিফিকেশন ডকুমেন্ট অন্তর্ভুক্ত করা হয়েছে:

| ডকুমেন্ট | ফাইলের অবস্থান | বিষয়বস্তু ও বিবরণ |
|---|---|---|
| **PRD** | [`docs/PRD.md`](docs/PRD.md) | প্রোডাক্ট রিকোয়ারমেন্টস, ব্যবহারকারীর সমস্যা, জার্নি ও এমভিপি স্কোপ |
| **ARCHITECTURE** | [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | ক্লায়েন্ট-সার্ভারলেস সিকিউরিটি মডেল, জিরো-কী-লিকেজ আর্কিটেকচার ও ডাটা ফ্লো |
| **DATABASE** | [`docs/DATABASE.md`](docs/DATABASE.md) | লোকাল-ফার্স্ট ডাটা মডেল, ইনভেন্টরি-লেজার স্কিমা ও ফিনান্সিয়াল রিকনসিলিয়েশন সূত্র |
| **API** | [`docs/API.md`](docs/API.md) | জেমিনি ২.৫ ফ্ল্যাশ সার্ভারলেস এন্ডপয়েন্ট ও হোয়াটসঅ্যাপ নোটিফিকেশন স্পেক্স |
| **DESIGN** | [`docs/DESIGN.md`](docs/DESIGN.md) | ডার্ক-ফার্স্ট ড্রিবল ডিজাইন সিস্টেম, কালার টোকেন, টাইপোগ্রাফি ও ইউএক্স কম্পোনেন্টস |
| **AGENTS** | [`docs/AGENTS.md`](docs/AGENTS.md) | অটোনোমাস কোডিং এজেন্ট রুলস, কোড কোয়ালিটি ও ফিনান্সিয়াল অডিট গাইডলাইন্স |
| **AUDIT** | [`docs/AUDIT.md`](docs/AUDIT.md) | ২৪/২৪ ফিনান্সিয়াল ইনটেগ্রিটি টেস্ট ম্যাট্রিক্স ও অটোমেটেড টেস্ট রিপোর্ট |

## 🌟 কেন কারবার (KarBaar) অন্যান্যদের চেয়ে আলাদা?

বাংলাদেশের বেশিরভাগ মুদি ও ক্ষুদ্র দোকানদার সারাদিন ব্যস্ত থাকেন, ফোনে জটিল ফর্ম পূরণ করে বা কিবোর্ডে টাইপ করে ডেটা এন্ট্রি করার সময় বা মানসিকতা তাদের থাকে না। বাজারে হিসাবের অ্যাপ অনেক থাকলেও **AI-চালিত ভয়েস-ফার্স্ট স্বয়ংক্রিয় হিসাব রাখার সমাধান দেশে এই প্রথম**।

- 🗣️ **ভয়েস-টু-সেল (Voice-to-Sale):** "কাউসার ভাইকে ২ বস্তা চাল বাকি দিলাম" বললেই সিস্টেম স্বয়ংক্রিয়ভাবে চালের স্টক কমায় এবং কাউসার ভাইয়ের নামে বাকি খাতায় যোগ করে।
- 🤝 **দ্বিধাহীন নিরাপত্তা (Human-in-the-Loop):** AI কখনো আন্দাজে ডেটাবেজ পরিবর্তন করে না। প্রতিটি কণ্ঠস্বর কমান্ডের পর স্পষ্ট কনফার্মেশন কার্ড তৈরি হয় এবং দোকানির স্পষ্ট সম্মতিতে লেনদেন লেজারে যুক্ত হয়।
- ⏪ **এক ক্লিকে পূর্বাবস্থায় ফেরা (Single-Click Undo):** ভুল এন্ট্রি হলে মুহূর্তেই স্টক, নগদ ক্যাশ এবং বাকি পূর্বের অবস্থায় ফিরিয়ে আনা যায়।
- 🛡️ **জিরো ক্লায়েন্ট কী লিকেজ (Zero Client Key Leakage):** ব্রাউজারে কোনো API Key উন্মুক্ত থাকে না। সমস্ত AI কল কঠোরভাবে সার্ভারলেস সিকিউর প্রক্সির মাধ্যমে পরিচালিত হয়।
- 📴 **হাইব্রিড অফলাইন রেজিলিয়েন্স:** ইন্টারনেট বা এপিআই না থাকলেও লোকাল রুল-ইঞ্জিনের মাধ্যমে ১০০% হিসাব ও লেনদেন সচল থাকে।

---

## 🏗️ আর্কিটেকচার ও টেকনিক্যাল স্ট্যাক

```
   ┌─────────────────────────────────────────────────────────────┐
   │                   KarBaar Client (PWA)                     │
   │  - Pure ECMAScript 2024 / Zero-Build Vanilla Architecture   │
   │  - Tailwind CSS + Brand Violet (#7c3aed) + Dark Mode       │
   │  - Web Speech API (bn-BD) with Fuzzy Phonetic Matching     │
   │  - Complete In-Memory & LocalStorage Dual Persistence       │
   └──────────────────────────────┬──────────────────────────────┘
                                  │ POST /.netlify/functions/karbaar-ai
                                  │ (Strict Rate Limiting & Payload Guards)
                                  ▼
   ┌─────────────────────────────────────────────────────────────┐
   │             Netlify Serverless Security Proxy               │
   │  - Node.js Runtime                                          │
   │  - Google Gemini 3.5 Flash Lite / 2.0 Flash REST Integration     │
   │  - Rate Limit: 20 req/min/IP (HTTP 429 Retry-After: 60)    │
   │  - Payload Guard: Max 50,000 bytes (HTTP 413)               │
   │  - Server-Side GEMINI_API_KEY (Never exposed to browser)    │
   └─────────────────────────────────────────────────────────────┘
```

---

## 🧪 আর্থিক নির্ভুলতা ও সম্পূর্ণ টেস্ট স্যুট (Financial Integrity Audit — 24/24 PASS)

আমরা কোডের প্রতিটি লেনদেন, ক্যাশ রিকনসিলিয়েশন, ডাবল-কাউন্টিং রোধ, ইনভেন্টরি কস্ট বেসিস এবং ডায়নামিক রোলব্যাক ২৪টি কঠোর স্বয়ংক্রিয় টেস্ট কেসের মাধ্যমে নোড-ভিত্তিক টেস্ট হার্নেসে শতভাগ যাচাই করেছি:

| ID | টেস্ট কেস (Test Scenario) | প্রত্যাশিত আচরণ (Expected) | ফলাফল (Actual) | স্ট্যাটাস |
|---|---|---|---|:---:|
| **T01** | Cash sale updates inventory and revenue | Stock 4 -> 2, Sales = 370, Profit = 30 | Stock: 2, Sales: 370, Profit: 30 | **PASS** |
| **T02** | Purchase updates inventory and weighted-average cost | Stock 7 -> 17, WAC updated to 140 BDT, Profit unchanged | Stock: 17, WAC: 140, Profit: 30 | **PASS** |
| **T03** | Credit sale updates inventory, revenue, and dues | Stock 10 -> 8, Sales += 140, Rahim due = 140, Profit += 20 | Stock: 8, Sales: 510, Rahim due: 140, Profit: 50 | **PASS** |
| **T04** | Partial credit payment reduces dues without increasing sales | Rahim due 140 -> 40, Settled: false, Collected = 100, Sales strictly unchanged | Rahim due: 40, Settled: false, Collected: 100, Sales: 510 (Before: 510) | **PASS** |
| **T05** | Full payment settles dues | Due 500 -> 0, Settled = true | Due: 0, Settled: true | **PASS** |
| **T06** | Discounted sale calculates correct profit | Profit increase = 5 BDT (175 sold - 170 cost) | Profit increase: 5 BDT (Total profit: 55) | **PASS** |
| **T07** | Unknown cost produces unknown profit | tx.profitUnknown = true, tx.calculatedProfit = null, stats.profit unchanged (No fake 15%) | profitUnknown: true, calculatedProfit: null, Profit delta: 0 | **PASS** |
| **T08** | Operating expenses separated from purchase costs | Operating expenses reduce profit by 450, separated from purchase costs (1470) | Expenses: 450, Purchases: 1470, Profit: -395 | **PASS** |
| **T09** | Cumulative batch stock shortage is rejected | Batch rejected due to cumulative shortage. Stock unchanged at 1. | Validation ok: false, Error: "তেল-এর পর্যাপ্ত স্টক নেই। ব্যাচের মোট চাহিদা ১ বোতল, কিন্তু অবশিষ্ট প্রজেক্টেড স্টক মাত্র ০ বোতল।", Stock: 1 | **PASS** |
| **T10** | Multi-action batch succeeds consistently | Both actions committed atomically. Sugar stock 17 -> 15, Sales += 280 | Saved: 2, Sugar stock: 15, Sales: 1465 | **PASS** |
| **T11** | Mid-batch failure does not silently corrupt records | Action 1 executed and rolled back after Action 2 mid-execution failure. State 100% restored (rolledBack: true). | res.ok: false, rolledBack: true, Sugar stock: 15 (Before: 15), Sales: 1465 (Before: 1465) | **PASS** |
| **T12** | Duplicate request is not applied twice | 1st call: ok true; 2nd call: in-memory latch blocked; 3rd call: persistent registry blocked duplicate. Sales delta +140 exactly. | 1st: true, 2nd: already_executed, 3rd duplicate: true, Sales delta: 140 | **PASS** |
| **T13** | Undo survives page refresh | Undo succeeds post-refresh: Stock reverted to 14, Sales reverted to 1605 | Undo ok: true, Stock: 14, Sales: 1605 | **PASS** |
| **T14** | Merged customer credit undo preserves earlier balances | Due merged to 3000, reverted to 2000. Customer record preserved. | Before undo: 3000, After undo: 2000, Customer exists: true | **PASS** |
| **T15** | Payment reversal restores the correct balance | Due 140 -> 40 on payment -> 140 on undo. Sales revenue constant throughout. | Due after pay: 40, Due after undo: 140, Sales: 1745 (Expected: 1745) | **PASS** |
| **T16** | Negative, zero, NaN, and infinite amounts are rejected | All 6 invalid transactions rejected with ok: false. | tZero: false, tNeg: false, tNaN: false, tInf: false, tZeroQty: false, tNegQty: false | **PASS** |
| **T17** | Invalid unit conversion & unit mismatch rejected | 500g converts to 0.5kg; Rice/oil unit mismatches rejected with Bengali guidance; negative qty sanitized. | Conversion: true (qty: 0.5, amt: 70), Rice mismatch: true, Oil mismatch: true, Sanitize: true | **PASS** |
| **T18** | Missing or ambiguous customer triggers clarification | Missing customer triggers clear Bengali clarification prompt. | Result: "কার নামে বাকি লিখব? নামসহ আবার বলুন।" | **PASS** |
| **T19** | Missing or ambiguous product triggers clarification | Unrecognized product triggers product clarification prompt. | Result: "কোন পণ্য বুঝতে পারিনি।" | **PASS** |
| **T20** | AI network failure handled transparently with local fallback | Returns local answer gracefully with offline badge. | Source: "Karbaar AI · হিসাব সহকারী (লোকাল ইঞ্জিন)", Preview: "রহমান ভাই, আমি স্টক, কেনার পরামর্শ, লাভ, বাকি আদায..." | **PASS** |
| **T21** | Local data persists after refresh | All 6 storage partitions saved and 100% reconstructed without data loss. | Keys present: true, Sales: 1745, Tx: 12, Baki: 4, Undo: 12 | **PASS** |
| **T22** | Cash reconciliation matches underlying transactions | Drawer cash exactly equals totalCashIn (2065) - totalCashOut (1970) = 95 | Drawer cash: 95, Expected: 95 | **PASS** |
| **T23** | Historical cost changes handled correctly | WAC updated to 71.11, then reverted to 60 on undo. Stock 18 -> 8. | WAC after restock: 71.11, WAC after undo: 60, Stock after undo: 8 | **PASS** |
| **T24** | All business invariants remain valid after consecutive errors | State completely unchanged after consecutive illegal actions. | Tx count: 12 (Before: 12), Sales: 1745 (Before: 1745) | **PASS** |

## 🚀 ডিপ্লয়মেন্ট গাইড (Deployment Guide)

### ১. গিট রেপোজিটরি পুশ (Git Push)

প্রজেক্টটি Git-এ আপলোড করার জন্য `karbaar-deploy` ফোল্ডারের ভেতরে গিয়ে টার্মিনালে নিচের কমান্ডগুলো চালান:

```bash
git init
git add .
git commit -m "feat: KarBaar AI Bengali Voice-First Shop Management Engine (Production Ready)"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo-name>.git
git push -u origin main
```

### ২. নেটলিফাই ডিপ্লয় ও এনভায়রনমেন্ট ভেরিয়েবল সেটআপ (Netlify Deploy)

১. [Netlify Dashboard](https://app.netlify.com)-এ যান।
2. **"Add new site"** $\rightarrow$ **"Import an existing project"** নির্বাচন করে আপনার GitHub রেপো সিলেক্ট করুন।
3. Build Settings-এ:
   - **Base directory:** খালি রাখুন (বা `./`)
   - **Publish directory:** `.`
   - **Functions directory:** `netlify/functions`
4. **Site configuration** $\rightarrow$ **Environment variables**-এ গিয়ে নিচের কী-টি যোগ করুন:
   - `GEMINI_API_KEY` = `আপনার_গুগল_জেমিনি_এপিআই_কী`
5. **Deploy Site**-এ ক্লিক করুন। ৩-৫ সেকেন্ডের মধ্যে সাইট লাইভ হয়ে যাবে!

---

## 🔒 সিকিউরিটি ও কমপ্লায়েন্স

- **কোনো ব্রাউজার কী ইনপুট নেই:** সাধারণ ব্যবহারকারী বা অডিটর ব্রাউজারের ইনস্পেক্ট এলিমেন্টে কখনোই API Key দেখতে পাবেন না।
- **রেট লিমিটিং:** প্রতিটি আইপি-র জন্য প্রতি মিনিটে সর্বোচ্চ ২০টি রিকোয়েস্ট বরাদ্দ, যাতে সার্ভার ওভারলোড বা ডিডিওএস না হয়।
- **পে-লোড প্রটেকশন:** সর্বোচ্চ ৫০ কেবি সাইজের বেশি রিকোয়েস্ট সার্ভারলেস ফাংশন তৎক্ষণাৎ ড্রপ করে (HTTP 413)।
- **নিরাপত্তা হেডার:** `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Permissions-Policy: microphone=(self)` সক্ষম।

---

## 👥 টিম ও কৃতজ্ঞতা

- **Project:** KarBaar (কারবার)
- **Competition:** CommerceSphere AI / DemandIQ Hackathon
- **Target Audience:** বাংলাদেশের সকল মুদি, পাইকারি ও ক্ষুদ্র দোকানদার।
