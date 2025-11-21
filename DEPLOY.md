# 🚀 Quick Deploy to Vercel - Step by Step

## ⚡ 3-Minute Deployment

### 1️⃣ Open Vercel Dashboard
**Go to:** https://vercel.com/dashboard

### 2️⃣ Import Project (if not already linked)
- Click **"Add New..."** → **"Project"**
- Find: `nelcostaa/openai_chatbot` or `GeorgeJacksonAI/recollectlife`
- Click **"Import"**

### 3️⃣ Add Environment Variable (CRITICAL)
⚠️ **Your current API key is leaked and won't work!**

1. Click **"Environment Variables"**
2. Add new variable:
   - Name: `GEMINI_API_KEY`
   - Value: Get new key from https://aistudio.google.com/app/apikey
   - Select: All environments (Production, Preview, Development)

### 4️⃣ Deploy
Click **"Deploy"** button

Wait 1-2 minutes for build to complete.

### 5️⃣ Test Your Deployment
Once deployed, test:
- Visit the URL (e.g., `https://openai-chatbot-xxx.vercel.app`)
- Type "yes" → Click "Enviar"
- Should advance to Route Selection

---

## ✅ What's Already Done

- ✅ Code pushed to GitHub (both repos)
- ✅ All 45 tests passing
- ✅ Frontend builds successfully  
- ✅ `vercel.json` configured
- ✅ Python dependencies ready
- ✅ `.env` not in git (secure)

---

## 🔧 Build Settings (Auto-detected)

Vercel reads from `vercel.json`:
- **Build Command:** `cd frontend && npm install && npm run build`
- **Output Directory:** `frontend/dist`
- **Install Command:** `pip install -r requirements.txt`

No changes needed!

---

## 📱 After Deployment

Your app structure:
```
https://your-app.vercel.app/
├── /                    → React frontend
├── /api/health          → Python serverless
├── /api/model-status    → Python serverless
└── /api/chat            → Python serverless (with Gemini AI)
```

---

## 🆘 Quick Troubleshooting

**"API calls failing"**
→ Add `GEMINI_API_KEY` in Environment Variables

**"Build failed"**
→ Check Vercel build logs for specific error

**"Frontend works, API doesn't"**
→ Check Functions tab for errors

---

## 📚 Full Documentation

See `docs/VERCEL_DEPLOYMENT_GUIDE.md` for complete instructions.

