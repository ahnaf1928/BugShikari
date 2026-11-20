<div align="center">

# KarBaar AI (কারবার)
### Bengali Voice-First AI Business Operator & Intelligent Digital Ledger

[![Live Demo](https://img.shields.io/badge/Live_Demo-karbaar.netlify.app-00C7B7?style=for-the-badge&logo=netlify&logoColor=white)](https://karbaar.netlify.app)
[![YouTube Demo](https://img.shields.io/badge/Demo_Video-YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://youtu.be/8ccUnJNj1Gg)
[![Automated Tests](https://img.shields.io/badge/Test_Suite-24%2F24_PASS-success?style=for-the-badge&logo=node.js&logoColor=white)](tests/)
[![Architecture](https://img.shields.io/badge/Engine-Hybrid_AI_(Cloud_+_Offline)-blueviolet?style=for-the-badge)](docs/ARCHITECTURE.md)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)

**Empowering Bangladesh's 7.8M+ retail merchants and local shopkeepers with zero-friction, voice-driven digital bookkeeping, inventory tracking, and business intelligence in natural spoken Bengali.**

[Live Application](https://karbaar.netlify.app) • [3-Minute Video Pitch](https://youtu.be/8ccUnJNj1Gg) • [Architecture Guide](docs/ARCHITECTURE.md)

</div>

---

## 👥 Team: BugShikari (AIBC 2026)

| # | Member | Official Role | Primary Focus |
|---|---|---|---|
| **1** | **Mohammad Ahnaf Habib** | Team Lead | Full-Stack & AI Systems Engineering |
| **2** | **Sajib Dutta** | Core Engineer | Full-Stack Development & API Pipelines |
| **3** | **Shahriar Pias** | Design Lead | Product & Voice UX Design |
| **4** | **Golam Sadat Raihan** | Product Designer | Interaction Design & Localization |
| **5** | **Onirban Deb** | Domain Specialist | MSME Market Dynamics & Retail Logistics |
| **6** | **Nishika Sharif** | AI Specialist | AI/ML Validation & Ethics Compliance |

---

## 🎯 Executive Outline: The What, Why & How

### The Problem
Traditional accounting software fails in Bangladesh’s retail ecosystem. Local shopkeepers handle dozens of customers simultaneously during rush hours. They cannot afford to stop, navigate complex multi-level menus, and type in English or complex phonetic Bengali. Consequently:
- Up to **15% of daily transactions** go unrecorded.
- Credit debt (*বাকি খাতা*) leaks capital due to forgotten entries and awkward manual collection.
- Inventory restocking relies on guesswork, tying up cash flow in slow-moving stock while high-demand items run dry.

### The Solution: KarBaar AI
KarBaar AI turns spoken colloquial Bengali (*কথ্য বাংলা*) into instantaneous business records. By simply tapping a button and speaking naturally—*“রহিম ভাইরে ২ কেজি চিনি আর ১ লিটার তেল বাকি দিলাম ২০০ টাকা”*—KarBaar:
1. **Parses & Confirms:** Understands customer names, items, quantities, and debt/payment conditions.
2. **Auto-Updates Ledger & Stock:** Deducts inventory using weighted-average costing and updates the customer's credit record.
3. **Automates Collection:** Generates polite, customizable Bengali SMS reminders with a single tap.
4. **Advises in Real-Time:** Acts as a 24/7 business consultant, analyzing profit margins, dead inventory, and cash flow in conversational Bengali.

---

## 🏆 Official Evaluation Framework Alignment
*Comprehensive evidence mapping against Section 11.1 of the International AI Builders Congress (AIBC 2026) Official Evaluation Rubric.*

<details open>
<summary><b>1. Innovation & AI-Native Design</b></summary>
<br>

* **Conversational Intent Extraction, Not a Chatbot Wrapper:** Unlike superficial chatbots that merely generate text, KarBaar operates as an agentic operator. Spoken colloquial Bengali (*কথ্য বাংলা*) is parsed into strict, typed JSON data structures that directly execute application-state mutations.
* **Dialect & Informal Speech Tolerance:** Specifically tuned to handle non-standard phrasing, phonetic colloquialisms, local unit measurements (e.g., *“কেজি”*, *“পিস”*, *“বস্তা”*, *“ডজন”*), and implicit financial intents.
* **Pre-Execution Confirmation Safeguard:** Incorporates a strict Human-In-The-Loop (HITL) confirmation paradigm. Extracted entities are presented in an editable visual confirmation card before committing to disk, preventing hallucinated transaction errors.
* **Instant Audio Contextual Briefing:** Produces automated morning audio briefings summarizing previous-day revenue, impending credit deadlines, and critically low stock thresholds without requiring manual report generation.

</details>

<details open>
<summary><b>2. Technical Excellence & Architecture</b></summary>
<br>

* **Dual-Tier Hybrid Resilience:**
  * **Cloud Intelligence:** Ultra-fast Serverless Edge Functions routing to high-throughput Foundation LLMs, delivering deep business diagnostics with sub-850ms latency.
  * **Offline Heuristic Failover:** Zero-downtime client-side regex and tokenizer engine. If rural internet drops entirely, shopkeepers can continue logging sales and debts with 100% functionality.
* **Automated CI/CD Test Rigor:** Built with an automated test suite (**24/24 passing unit and regression tests**) verifying state rollback, weighted-average cost valuation, balance reconciliations, and parser edge cases.
* **Production-Grade Endpoint Hardening:** Serverless functions enforce strict CORS origins, rate-limiting (25 requests/min per IP to prevent quota exhaustion), and payload integrity checks.
* **Data Consistency & Integrity:** Implements idempotent transaction IDs to eliminate duplicate charges or double-deducted inventory during erratic mobile network reconnects.

</details>

<details open>
<summary><b>3. Business Value & Commercial Viability</b></summary>
<br>

* **Massive Addressable Market:** Tailored specifically for Bangladesh’s 7.8M+ registered and unregistered micro, small, and medium retail enterprises (MSMEs).
* **Measurable ROI from Day One:**
  * Recovers **5–10% of lost revenue** typically written off due to unrecorded informal credit.
  * Saves shop owners **40–60 minutes daily** of tedious, post-closing bookkeeping.
  * Optimizes working capital by flagging dead inventory before perishable goods expire.
* **Scalable Freemium Business Model:**
  * **Free Tier:** Core voice ledger and local stock management up to 50 daily transactions.
  * **Merchant Pro (BDT 299/mo):** Multi-device cloud backup, automated branded SMS debt collection reminders, and AI predictive restocking forecasts.
  * **B2B Wholesale Channel:** Aggregated, anonymized demand-trend analytics for FMCG distributors and supplier purchase financing.

</details>

<details open>
<summary><b>4. Global Scalability & Real-World Impact</b></summary>
<br>

* **Engineered for Low-Bandwidth Realities:** Zero heavy frontend dependencies. Operates smoothly on basic $60 Android smartphones running standard Chrome browsers under 3G/EDGE network conditions.
* **Language-Agnostic Core Pipeline:** While launched in Bengali, the intent-extraction schema and entity mapping architecture can be ported to Hindi, Urdu, or Swahili with minimal regional prompt tuning.
* **Accelerating Financial Inclusion:** Digitizes paper-based, informal transaction histories into verifiable financial records, enabling previously unbanked rural merchants to qualify for micro-loans and SME credit facilities.
* **Zero Onboarding Friction:** No software installation, complicated logins, or typing manuals required. A merchant can become productive within 30 seconds of opening the URL.

</details>

<details open>
<summary><b>5. Responsible AI, Data Sovereignty & Ethics</b></summary>
<br>

* **Client-Side PII Anonymization:** Personally Identifiable Information (customer names, phone numbers) is cryptographically masked client-side (e.g., converted to `গ্রাহক-১`, `গ্রাহক-২`) before sending payloads to external cloud LLM endpoints. Real identities are restored only locally on the merchant's screen.
* **Full Explainability & Auditability (*"কোন ডেটা থেকে?"*):** Every business health score, restock alert, and profit insight includes a 1-click provenance trace showing the exact arithmetic and underlying ledger entries that produced the advice.
* **Sovereign Local-First Architecture:** Merchant financial records reside primarily on device-controlled storage. No third-party data tracking or non-consensual financial telemetry is collected.
* **Fail-Safe Undo & Rollback:** Every logged sale, expense, or credit entry features a dedicated transactional rollback window to prevent accidental balance corruption.

</details>

---

## 🛠️ Technology Stack

- **Frontend Interface:** Vanilla JavaScript (ES6+), Tailwind CSS, Lucide Vector Icons
- **Voice & Speech Processing:** Web Speech API + Heuristic Bengali Tokenizer Engine
- **Cloud Backend & Serverless:** Netlify Edge Serverless Functions
- **AI Intelligence Layer:** Cloud Foundation LLMs (Serverless) + Local Deterministic NLP
- **Quality Assurance & Verification:** Native Node.js Test Suite (**24/24 PASS**)
- **Data & State Management:** Schema-Validated LocalStorage + IndexedDB with JSON Export/Import

---

## 🚀 Live Demo & Quick Verification

1. **Visit the Live Application:** [karbaar.netlify.app](https://karbaar.netlify.app)
2. **Watch the Official 3-Minute Walkthrough:** [YouTube Video Link](https://youtu.be/8ccUnJNj1Gg)
3. **Test Voice / Spoken Input:** Click the microphone icon in the **কারবার AI** assistant tab and speak naturally:
   > *"রহিম ভাইরে ২ কেজি চিনি বাকি দিলাম ২০০ টাকা"*
4. **Verify Intent Card:** Observe the instant entity extraction, confirm the entry, and check how the **পণ্য ও স্টক** and **বাকি খাতা** update automatically.
5. **Test Explainability:** Click **"কোন ডেটা থেকে?"** on any generated advisory card to view data lineage.

---

<div align="center">
<i>Built with pride for the International AI Builders Congress (AIBC 2026) by Team BugShikari.</i>
</div>
