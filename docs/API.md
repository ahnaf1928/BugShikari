# 🔌 API Specification & Integration Reference — KarBaar (কারবার)

> **Document Version:** 2.0.0  
> **Target Domain:** CommerceSphere AI | **Challenge:** DemandIQ  
> **Team:** BugShikari  

---

## 1. Internal Serverless API: `karbaar-ai`

The `karbaar-ai` serverless function acts as an air-gapped security proxy between the client browser and Google's Gemini API.

### 1.1 Endpoint Overview
- **Path:** `POST /.netlify/functions/karbaar-ai`
- **Content-Type:** `application/json`
- **Authentication:** Injected server-side via `process.env.GEMINI_API_KEY` (Never exposed to client)
- **Rate Limit:** 20 requests per minute per IP address

---

### 1.2 Request Specification

#### Request Headers
```http
POST /.netlify/functions/karbaar-ai HTTP/1.1
Host: karbaar.netlify.app
Content-Type: application/json
Accept: application/json
```

#### Request Payload Schema
```json
{
  "prompt": "কাউসার ভাইকে ২ বস্তা মিনিকেট চাল বাকি দিলাম আর ৫০ টাকা দোকান খরচ হলো",
  "systemInstruction": "You are KarBaar AI, a professional Bengali retail business assistant...",
  "context": {
    "storeName": "রহমান স্টোর",
    "todaySales": 7845,
    "inventorySample": [
      { "name": "মিনিকেট চাল (৫০ কেজি)", "stock": 12, "sellPrice": 3650 },
      { "name": "তীর সয়াবিন তেল (৫ লিটার)", "stock": 4, "sellPrice": 910 }
    ]
  }
}
```

| Field | Type | Required | Description |
| :--- | :--- | :---: | :--- |
| `prompt` | `string` | **Yes** | Transcribed voice query or user typed input (1 to 2,000 characters). |
| `systemInstruction` | `string` | No | Persona and formatting instructions for structured extraction. |
| `context` | `object` | No | Current retail ledger metrics (inventory sample, sales, cash drawer). |

---

### 1.3 Response Specification

#### Success Response (`HTTP 200 OK`)
```json
{
  "text": "কাউসার ভাইয়ের নামে ২ বস্তা মিনিকেট চাল (৭,৩০০৳) বাকি যোগ করা হয়েছে এবং ৫০৳ দোকান খরচ রেকর্ড করা হয়েছে।",
  "actions": [
    {
      "type": "baki",
      "customer": "কাউসার ভাই",
      "item": "মিনিকেট চাল (৫০ কেজি)",
      "qty": 2,
      "unitPrice": 3650,
      "totalAmount": 7300
    },
    {
      "type": "expense",
      "category": "দোকান খরচ",
      "amount": 50
    }
  ],
  "modelUsed": "gemini-3.5-flash-lite",
  "timestamp": "2026-11-20T03:45:00.000Z"
}
```

#### Error Responses

| HTTP Status | Error Code | Reason & Client Handling |
| :---: | :--- | :--- |
| `400 Bad Request` | `INVALID_PAYLOAD` | Missing `prompt` or malformed JSON. Fallback to local tokenizer. |
| `413 Payload Too Large` | `PAYLOAD_OVERSIZE` | Body exceeds 50,000 bytes. Request rejected for DDoS mitigation. |
| `429 Too Many Requests` | `RATE_LIMITED` | Exceeded 20 req/min. Header `Retry-After: 60` returned. |
| `500 Server Error` | `MISSING_API_KEY` | Server-side `GEMINI_API_KEY` environment variable not configured. |
| `502 Bad Gateway` | `UPSTREAM_TIMEOUT` | Google API unreachable. Client triggers local edge rule engine. |

---

## 2. External Integration Specifications

### 2.1 Google Gemini AI Cluster Integration
- **Upstream Host:** `https://generativelanguage.googleapis.com/v1beta/models/`
- **Primary Model:** `gemini-3.5-flash-lite`
- **Failover Model:** `gemini-3.5-flash-lite`
- **Parameters:**
  - `temperature`: `0.2` (Strict determinism for entity extraction)
  - `topP`: `0.95`
  - `maxOutputTokens`: `1024`

### 2.2 WhatsApp Click-to-Chat API
Used for automated, polite credit collection messages:
- **Base URL:** `https://wa.me/{phone_number}`
- **Query Parameter:** `?text={url_encoded_bengali_message}`
- **Example Template:**
  ```text
  আসসালামু আলাইকুম কাউসার ভাই, রহমান স্টোর থেকে জানাচ্ছি। আপনার পূর্বের বকেয়া হিসাব ৩,৫০০ টাকা। সুবিধা মতো সময়ে পরিশোধের অনুরোধ রইল। ধন্যবাদ!
  ```

### 2.3 Browser Web Speech API (`bn-BD`)
- **Engine:** Chromium / DirectWrite native speech recognizer
- **Configuration:**
  ```javascript
  const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
  recognition.lang = 'bn-BD';
  recognition.continuous = false;
  recognition.interimResults = false;
  ```
