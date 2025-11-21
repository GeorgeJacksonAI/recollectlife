# Vercel Deployment Guide - Life Story Game AI Interviewer

## Pre-Deployment Checklist

- [ ] All backend tests passing (37/37)
- [ ] Python syntax validated for all serverless functions
- [ ] Frontend builds successfully (`npm run build`)
- [ ] `.env.example` documented with all required variables
- [ ] Sensitive data not committed (check git history)
- [ ] `vercel.json` configuration correct

## Environment Variables Required

Add these in Vercel Project Settings → Environment Variables:

| Variable | Value | Environment |
|----------|-------|-------------|
| `GEMINI_API_KEY` | Your Google AI Studio API key | Production, Preview, Development |
| `GEMINI_MODELS` | (Optional) Custom model cascade | All |

**Get API Key:** https://aistudio.google.com/app/apikey

## Deployment Steps

### Option 1: Automatic Deployment (Recommended)

1. **Connect Repository to Vercel**
   - Visit https://vercel.com/new
   - Import your GitHub repository
   - Select the `openai_chatbot` repository

2. **Configure Build Settings**
   ```
   Framework Preset: Other
   Root Directory: ./
   Build Command: cd frontend && npm install && npm run build
   Output Directory: frontend/dist
   Install Command: cd frontend && npm install
   Node.js Version: 18.x (or latest)
   ```

3. **Add Environment Variables**
   - Project Settings → Environment Variables
   - Add `GEMINI_API_KEY`
   - Apply to: Production, Preview, Development

4. **Deploy**
   - Click "Deploy"
   - Wait for build to complete (~2-3 minutes)
   - Visit deployed URL

### Option 2: CLI Deployment

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy to preview
vercel

# Deploy to production
vercel --prod
```

## Post-Deployment Verification

### 1. Health Check
```bash
curl https://your-deployment.vercel.app/api/health
```
Expected: `{"status":"ok",...}`

### 2. Model Status
```bash
curl https://your-deployment.vercel.app/api/model-status
```
Expected: List of available models

### 3. Frontend
- Visit `https://your-deployment.vercel.app`
- Should show chat interface
- Type "yes" → Should advance to route selection
- Select route → Should start interview

### 4. Full Interview Test
- Complete GREETING → ROUTE_SELECTION → QUESTION_1
- Verify AI responses appear
- Check phase indicators update
- Confirm no console errors

## Monitoring & Logs

### View Logs
1. Vercel Dashboard → Your Project → Deployments
2. Click on deployment
3. View "Function Logs" tab

### Common Log Patterns
```
[AI] Attempt 1/6: gemini-2.5-flash
[AI] ✅ Success with gemini-2.5-flash
```

### Error Patterns to Watch
- `❌ All models exhausted rate limits` → Reduce request frequency
- `GEMINI_API_KEY not found` → Check environment variables
- `Messages list cannot be empty` → Frontend payload issue

## Performance Optimization

### Cold Start Mitigation
- Vercel keeps functions warm with traffic
- First request may take 2-5s (cold start)
- Subsequent requests: < 1s

### Token Usage
- Each conversation: ~500-2000 tokens
- Gemini free tier: 1500 requests/day
- Monitor usage in Google AI Studio

### Timeout Configuration
- Current: 30s per function
- If hitting timeout with 6-model fallback, reduce to 3 models
- Edit `vercel.json`: `"maxDuration": 60` (max)

## Rollback Procedure

If deployment breaks:

1. **Instant Rollback**
   ```bash
   # Vercel Dashboard → Deployments → Previous Version → Promote to Production
   ```

2. **Revert Git**
   ```bash
   git revert HEAD
   git push origin main
   ```

3. **Environment Issues**
   - Check Vercel logs first
   - Verify environment variables in dashboard
   - Test with preview deployment before promoting

## Troubleshooting

### Build Fails
```bash
# Locally test build
cd frontend
npm run build

# Check for errors
npm run lint
```

### Function Timeout
- Reduce fallback models in env vars
- Check Gemini API response times
- Consider caching system prompts

### CORS Errors
- Serverless functions include CORS headers
- Check browser console for specific origin
- Verify fetch URL matches deployment domain

### Rate Limit Issues
- Normal during high traffic
- Fallback cascade handles automatically
- If all models exhausted: implement client-side throttling

## Scaling Considerations

### Current Limits
- Vercel Hobby: 100GB bandwidth/month
- Serverless functions: 100GB-hours/month
- Concurrent executions: 100

### Upgrade Triggers
- > 10K requests/month
- > 1K concurrent users
- Custom domain needed
- Team collaboration required

## Security

### Pre-Production Security Audit
- [ ] No API keys in git history
- [ ] Environment variables encrypted by Vercel
- [ ] Input validation in place (50K char limit)
- [ ] CORS restricted to deployment domain
- [ ] Error messages don't leak sensitive info

### Post-Deployment
- Monitor Vercel logs for abuse patterns
- Rotate API keys every 90 days
- Check Google AI Studio quota usage
- Review Vercel function logs weekly

## Custom Domain Setup

1. Vercel Dashboard → Project Settings → Domains
2. Add your domain
3. Configure DNS (A/CNAME records provided)
4. Wait for SSL provisioning (~1 minute)
5. Verify `https://your-domain.com` works

## CI/CD Pipeline

Current setup:
- **Trigger:** Git push to `main`
- **Build:** Automatic on Vercel
- **Tests:** Run locally before push (manual)
- **Deploy:** Automatic to production

### Future Enhancements
- GitHub Actions for pre-deploy tests
- Staging environment (separate Vercel project)
- Automated E2E tests

## Support & Resources

- **Vercel Status:** https://www.vercel-status.com/
- **Gemini API Status:** https://status.cloud.google.com/
- **Community:** https://github.com/vercel/vercel/discussions

---

**Deployment Date:** 2025-11-21  
**Version:** 1.0.0  
**Deployed By:** Autonomous AI Agent
