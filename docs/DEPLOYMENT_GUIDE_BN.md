# KarBaar AI — সহজ বাংলা ডিপ্লয়মেন্ট গাইড (Beginner-Friendly)

এই গাইডটি অনুসরণ করে আপনি কোনো জটিল কোডিং জ্ঞান ছাড়াই ২ মিনিটের মধ্যে KarBaar AI-কে সম্পূর্ণ লাইভ করতে পারবেন।

---

## ১. GitHub-এ কোড আপলোড করার নিয়ম

১. আপনার কম্পিউটারে টার্মিনাল বা PowerShell খুলুন।
২. আনজিপ করা `karbaar-deploy` ফোল্ডারের ভেতরে যান:
   ```bash
   cd karbaar-deploy
   ```
৩. নিচের ৫টি কমান্ড একে একে চালান:
   ```bash
   git init
   git add .
   git commit -m "feat: KarBaar AI Bengali Voice MVP (Production Verified)"
   git branch -M main
   git remote add origin https://github.com/<আপনার-ইউজারনেম>/<আপনার-রেপো-নাম>.git
   git push -u origin main
   ```

---

## ২. Netlify-তে ডিপ্লয় এবং এপিআই কী সেট করার নিয়ম

১. [Netlify Dashboard](https://app.netlify.com/)-এ যান এবং আপনার GitHub একাউন্ট দিয়ে লগইন করুন।
২. **"Add new site"** $\rightarrow$ **"Import an existing project"** চাপুন।
৩. GitHub সিলেক্ট করে আপনার `karbaar` রেপোজিটরিটি নির্বাচন করুন।
৪. **Build settings**-এ নিচের তথ্যগুলো মিলিয়ে নিন:
   - **Base directory:** খালি রাখুন (বা `./`)
   - **Publish directory:** `.` (শুধু একটি ডট)
   - **Functions directory:** `netlify/functions`
৫. **Site configuration** $\rightarrow$ **Environment variables** সেকশনে গিয়ে **"Add a variable"** চাপুন:
   - **Key:** `GEMINI_API_KEY`
   - **Value:** `আপনার_গুগল_জেমিনি_এপিআই_কী`
   - *(ঐচ্ছিক)* **Key:** `KARBAAR_SHOP_ID` | **Value:** `karbaar-demo-shop-bd-01`
৬. **"Deploy site"** বাটনে চাপ দিন। ১ মিনিটের মধ্যেই সাইট লাইভ হয়ে যাবে!

---

## ৩. মোবাইল ফোনে PWA হিসেবে ইনস্টল করার নিয়ম

১. যেকোনো অ্যান্ড্রয়েড ফোনে **Google Chrome** বা **Microsoft Edge** দিয়ে আপনার Netlify সাইটের লিঙ্কে যান (যেমন: `https://karbaar.netlify.app`)।
২. ব্রাউজারের উপরে বা নিচে **"Add KarBaar to Home screen"** অথবা ৩-ডট মেনু থেকে **"Install app"** চাপুন।
৩. আপনার ফোনের হোম স্ক্রিনে KarBaar-এর বেগুনী অ্যাপ আইকন যুক্ত হয়ে যাবে।
৪. অ্যাপটি ওপেন করে প্রথমবার মাইক্রোফোনের অনুমতি (Allow Microphone) দিয়ে কথা বলা শুরু করুন!
