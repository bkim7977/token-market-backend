# 🚂 RAILWAY DEPLOYMENT CHECKLIST

## Step-by-Step Railway URL Process:

### ✅ Pre-Deployment:
- [x] Repository on GitHub: https://github.com/bkim7977/token-market-backend
- [x] All files committed and pushed
- [x] Railway.toml configuration file ready
- [x] Health check endpoint (/health) implemented

### 🚀 Deployment Steps:
1. [ ] Go to https://railway.app
2. [ ] Sign in with GitHub account  
3. [ ] Click "Deploy from GitHub repo"
4. [ ] Select `bkim7977/token-market-backend`
5. [ ] Railway auto-detects Python app
6. [ ] Add environment variables:
   ```
   SUPABASE_URL=https://rrhdrkmomngxcjsatcpy.supabase.co
   SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJyaGRya21vbW5neGNqc2F0Y3B5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzU0MDQwODUsImV4cCI6MjA1MDk4MDA4NX0.yLnx5vQyZ49vwLlT1mKS_DGx1-MfLCXVZ4lJtWMIPlA
   JWT_SECRET_KEY=token-market-super-secret-jwt-key-2025-production-ready
   ENVIRONMENT=production
   PORT=8000
   ```
7. [ ] Click "Deploy" 
8. [ ] Wait for build to complete (2-5 minutes)

### 📊 Finding Your URL:
1. [ ] Railway dashboard → Your project
2. [ ] Look for "Domains" or "Settings" tab
3. [ ] Copy the generated URL (e.g., https://your-app.railway.app)
4. [ ] Test the URL: visit `your-url/health`

### 🧪 Testing Your Deployment:
1. [ ] Visit `your-railway-url/health` - should return JSON
2. [ ] Visit `your-railway-url/collectibles` - should return array
3. [ ] Visit `your-railway-url/` - should return API info

### 💖 Update Lovable:
1. [ ] Copy your Railway URL
2. [ ] Update TokenMarketLovable.tsx:
   ```typescript
   const API_BASE_URL = 'https://your-actual-railway-url.railway.app';
   ```
3. [ ] Test login/register in your Lovable app
4. [ ] Verify collectibles load correctly

### 🐛 Troubleshooting:
- **URL not working?** Check Railway logs in dashboard
- **Build failing?** Verify requirements.txt has all dependencies
- **Environment errors?** Double-check environment variables
- **CORS issues?** Your backend already allows all origins (*)

## 🎯 Expected Railway URL Examples:
- `https://token-market-backend-production-1a2b3c.railway.app`
- `https://web-production-def456.railway.app`
- `https://lovable-backend.up.railway.app`

## ⚡ Quick Test Command:
Once you have your Railway URL, run:
```bash
python test_railway_url.py
```
And enter your URL to verify everything is working!
