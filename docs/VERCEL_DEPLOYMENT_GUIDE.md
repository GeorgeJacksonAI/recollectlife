# Vercel Deployment Guide

## ✅ Pre-Deployment Checklist (COMPLETED)

- ✅ Frontend builds successfully (`npm run build`)
- ✅ All 37 backend tests passing
- ✅ All 8 frontend tests passing
- ✅ `vercel.json` configured correctly
- ✅ Python dependencies in `requirements.txt`
- ✅ `.env` is gitignored (not pushed to GitHub)
- ✅ Code pushed to GitHub: `nelcostaa/openai_chatbot` and `GeorgeJacksonAI/recollectlife`

---

## 🚀 Deploy via Vercel Dashboard

### Step 1: Access Vercel Dashboard

1. Go to **https://vercel.com/dashboard**
2. Sign in with your account (you're already logged in via CLI as "George Jackson's projects")

### Step 2: Import Your GitHub Repository

**Option A: If project already exists in Vercel**
1. Find "openai-chatbot" in your projects list
2. Click on it to open the project
3. Go to the **"Deployments"** tab
4. Click **"Redeploy"** on the latest deployment
5. Skip to **Step 3: Configure Environment Variables**

**Option B: If this is a fresh deployment**
1. Click **"Add New..."** → **"Project"**
2. Find your repository:
   - **nelcostaa/openai_chatbot** OR
   - **GeorgeJacksonAI/recollectlife**
3. Click **"Import"**

### Step 3: Configure Build Settings

Vercel should auto-detect settings from `vercel.json`, but verify:

**Framework Preset:** `Other` or `None`

**Build & Development Settings:**
- **Build Command:** `cd frontend && npm install && npm run build`
- **Output Directory:** `frontend/dist`
- **Install Command:** `pip install -r requirements.txt`

**Root Directory:** `.` (leave as root)

### Step 4: Configure Environment Variables (CRITICAL)

⚠️ **Your current API key is leaked and disabled. You MUST add a new one.**

1. In the project settings, go to **"Environment Variables"**
2. Click **"Add Variable"**
3. Add:
   - **Name:** `GEMINI_API_KEY`
   - **Value:** `[YOUR_NEW_API_KEY_HERE]`
   - **Environments:** Select all (Production, Preview, Development)
4. Get a new key from: **https://aistudio.google.com/app/apikey**

### Step 5: Deploy

1. Click **"Deploy"**
2. Vercel will:
   - ✅ Install Python dependencies (`pip install -r requirements.txt`)
   - ✅ Install frontend dependencies (`npm install`)
   - ✅ Build frontend (`vite build`)
   - ✅ Create serverless functions from `api/*.py`
   - ✅ Deploy to production

### Step 6: Verify Deployment

Once deployment completes (usually 1-2 minutes):

1. Vercel will show you the deployment URL (e.g., `https://openai-chatbot-xxx.vercel.app`)
2. Click **"Visit"** to open the deployed app
3. Test the following:

**Frontend:**
- Page loads with "Life Story Game" title
- Initial greeting message appears
- Input field and "Enviar" button visible

**API Endpoints:**
```bash
# Replace YOUR_DOMAIN with your Vercel URL
curl https://YOUR_DOMAIN.vercel.app/api/health

# Should return:
# {"status":"ok","service":"Life Story Game AI Interviewer","timestamp":"..."}
```

**Full Interaction:**
1. Type "yes" in the input
2. Click "Enviar"
3. Should advance to Route Selection phase
4. Select a storytelling route
5. Chat should work with AI responses

---

## 🔧 Troubleshooting

### Issue: "API key error" or "403 Forbidden"
**Solution:** Add a valid `GEMINI_API_KEY` in Vercel environment variables (Step 4 above)

### Issue: "Module not found" or Python errors
**Solution:** Ensure `requirements.txt` is at project root and contains:
```
google-generativeai==0.3.2
python-dotenv==1.0.0
```

### Issue: Frontend shows but API calls fail
**Solution:** 
1. Check Vercel Function Logs (Dashboard → Project → Functions)
2. Verify environment variable is set correctly
3. Check that `api/*.py` files are deployed (visible in Deployment → Source)

### Issue: Build fails
**Solution:**
1. Check build logs in Vercel dashboard
2. Verify `frontend/package.json` has all dependencies
3. Test build locally: `cd frontend && npm run build`

---

## 📊 Monitoring Your Deployment

After deployment, monitor:

1. **Functions Tab:** See API invocations, errors, execution time
2. **Analytics Tab:** Page views, performance metrics
3. **Logs Tab:** Real-time logs from serverless functions
4. **Usage Tab:** API calls, bandwidth, build minutes

---

## 🔄 Future Deployments

Every time you push to `main` branch:

1. Vercel automatically detects the push
2. Triggers a new deployment
3. Runs tests and builds
4. Deploys to production (if successful)

You can also:
- Deploy specific branches as previews
- Rollback to previous deployments
- Set up staging environments

---

## 🎯 What Happens in Production

Your architecture on Vercel:

```
User Browser
    ↓
Vercel Edge Network (CDN)
    ↓
├── / (Frontend)
│   └── Static React app from frontend/dist/
│
└── /api/* (Serverless Functions)
    ├── /api/health → api/health.py → handler()
    ├── /api/model-status → api/model_status.py → handler()
    └── /api/chat → api/chat.py → handler()
                      ↓
                  Google Gemini API
```

**Key Differences from Local Dev:**
- ❌ No `dev_server.py` (that's local only)
- ❌ No Vite proxy (not needed in production)
- ✅ Vercel's router handles `/api/*` → Python functions
- ✅ CDN serves frontend assets globally
- ✅ Serverless functions auto-scale

---

## 🔐 Security Notes

- ✅ `.env` is gitignored (never pushed to GitHub)
- ✅ API key stored securely in Vercel environment
- ✅ CORS properly configured in API handlers
- ✅ No secrets in client-side code

**Remember:** Never commit `.env` files or API keys to Git!

---

## ✨ Your Deployment is Ready!

Current state:
- ✅ Code pushed to both GitHub repos
- ✅ All tests passing (45/45)
- ✅ Frontend production build working
- ✅ `vercel.json` properly configured
- ⏳ Waiting for you to deploy via dashboard

**Next action:** Follow Step 1-6 above to deploy! 🚀

