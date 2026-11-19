# 🎨 UI/UX Design System & Specification — KarBaar (কারবার)

> **Document Version:** 2.0.0  
> **Target Domain:** CommerceSphere AI | **Challenge:** DemandIQ  
> **Team:** BugShikari  

---

## 1. Design Philosophy & Environmental Constraints

Retail grocery environments in urban and rural Bangladesh present extreme operating conditions:
1. **Lighting Extremes:** Glare from direct afternoon sunlight hitting store counters vs. dim, flickering 40W yellow tungsten bulbs at night.
2. **Physical Context:** Shopkeepers frequently operate with wet, dusty, or oil-stained hands while packing bulk dry goods (rice, lentils, spices).
3. **Cognitive Load:** High stress during peak morning and evening rush hours; no tolerance for multi-step form modals or confirmation dialogues with ambiguous button labels.

### Core Principles
- **Touch Targets $\ge 48\text{px}$:** All interactive buttons and inputs adhere to WCAG AAA minimum hit targets to prevent mis-clicks.
- **Voice as First-Class Citizen:** The microphone button is persistently anchored in the primary visual thumb zone.
- **Color-Coded Status Language:** Green (`#10b981`) always signifies healthy stock / income; Red (`#ef4444`) signals urgent restock / debt; Amber (`#f59e0b`) signals warnings.

---

## 2. Color Tokens & Theme Architecture

KarBaar features a dual **Dark/Light Theme** powered by semantic Tailwind utility tokens.

### 2.1 Color Palette
| Token Name | Hex Code | Semantic Role |
| :--- | :---: | :--- |
| **Brand Violet** | `#7c3aed` | Primary brand accent, active state, voice ripple pulse. |
| **Violet Dark** | `#6d28d9` | Button hover states, header gradient stops. |
| **Emerald Growth** | `#10b981` | Cash income, healthy safe inventory, WhatsApp action. |
| **Rose Alert** | `#ef4444` | Urgent restock alert, customer debt, expense debit. |
| **Amber Warning** | `#f59e0b` | Low stock threshold, overdue reminder flag. |
| **Surface Dark** | `#0f172a` | App dark mode background (Slate-900). |
| **Card Surface Dark** | `#1e293b` | Elevated cards, tables, modals (Slate-800). |
| **Text Primary Dark** | `#f8fafc` | High-contrast body text in dark mode. |
| **Text Secondary Dark**| `#94a3b8` | Subtitles, timestamps, SKU metadata. |

---

## 3. Typography Hierarchy

| Style Role | Font Family | Size | Weight | Line Height |
| :--- | :--- | :---: | :---: | :---: |
| **Display Header** | Plus Jakarta Sans / Tiro Bangla | 28px | 800 (Extrabold) | 1.2 |
| **Section Title** | Plus Jakarta Sans / Tiro Bangla | 20px | 700 (Bold) | 1.3 |
| **Card Metric** | Plus Jakarta Sans (Monospace numerals) | 24px | 700 (Bold) | 1.1 |
| **Body Primary** | Tiro Bangla / Nirmala UI | 15px | 500 (Medium) | 1.5 |
| **Meta / Badge** | Plus Jakarta Sans | 12px | 600 (Semibold) | 1.0 |

---

## 4. Key UI Components

### 4.1 Floating Voice Operator (FAB)
- Centrally docked in the bottom navigation on mobile viewport.
- Animated CSS radial wave ripple during active microphone recording (`@keyframes pulse-ring`).
- Seamless tactile feedback on tap.

### 4.2 Human-in-the-Loop Confirmation Card
- Appears as a sliding bottom sheet on mobile and an overlay modal on desktop.
- Displays:
  - Extracted Product Name & Quantity.
  - Calculated Price & Ledger Destination (Cash vs. Baki).
  - Prominent Green "নিশ্চিত করুন" (Confirm) button and Red "বাতিল" (Cancel) button.

### 4.3 DemandIQ Stock Forecast Card
- Visual gradient card displaying seasonal indicators (e.g., "রমজান স্পেশাল", "শীতকালীন চাহিদা").
- Actionable suggestion chips: "৫ বস্তা চিনি রিস্টক করুন" with 1-click supplier order intent.
