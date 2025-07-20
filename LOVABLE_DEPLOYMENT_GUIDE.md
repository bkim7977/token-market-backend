# 🚀 LOVABLE DEPLOYMENT GUIDE - Backend & Frontend Integration

## 🎯 THE PROBLEM
Your Lovable frontend is hosted online at:
`https://b08e3d6b-734d-4dda-ba2e-871103b4a845.lovableproject.com`

But it's trying to connect to:
`http://localhost:8000` (only accessible on your local machine)

## ✅ SOLUTION: Deploy Your Backend

### Option 1: Railway (Recommended - Free & Easy)

1. **Prepare for deployment**:
   ```bash
   # Your project is already configured with:
   # - requirements.txt ✅
   # - Dockerfile ✅ 
   # - start.py with serve command ✅
   ```

2. **Deploy to Railway**:
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub
   - Click "Deploy from GitHub repo"
   - Connect your token_market_backend repository
   - Railway will auto-detect your Python app

3. **Environment Variables in Railway**:
   ```
   SUPABASE_URL=https://rrhdrkmomngxcjsatcpy.supabase.co
   SUPABASE_KEY=your-anon-key-here
   JWT_SECRET_KEY=your-secret-key-here
   ENVIRONMENT=production
   ```

4. **Get your Railway URL**:
   - After deployment, Railway gives you a URL like:
   - `https://your-app-name.railway.app`

### Option 2: Render (Also Free)

1. **Deploy to Render**:
   - Go to [render.com](https://render.com)
   - Connect GitHub and select your repo
   - Choose "Web Service"
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python start.py serve`

### Option 3: Heroku

1. **Create Heroku app**:
   ```bash
   # Install Heroku CLI first
   heroku create your-token-market-backend
   git push heroku main
   ```

## 🔧 UPDATE YOUR LOVABLE FRONTEND

Once your backend is deployed, update your Lovable component:

```typescript
// Replace localhost with your deployed URL
const API_BASE_URL = 'https://your-backend-url.railway.app';
// or
const API_BASE_URL = 'https://your-app-name.onrender.com';
```

## 🛠️ QUICK RAILWAY DEPLOYMENT

Let me create the exact files you need:

### 1. Railway Configuration (railway.toml)
```toml
[build]
builder = "nixpacks"

[deploy]
healthcheckPath = "/health"
healthcheckTimeout = 100
restartPolicyType = "always"
```

### 2. Production Requirements
Your existing `requirements.txt` is perfect:
```
fastapi==0.104.1
uvicorn==0.24.0
python-jose==3.3.0
passlib==2.0.0
bcrypt==4.1.2
python-multipart==0.0.6
supabase==2.0.2
```

### 3. Dockerfile (already exists)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "start.py", "serve"]
```

## 🌐 ENVIRONMENT VARIABLES FOR PRODUCTION

### In Railway Dashboard:
```
SUPABASE_URL=https://rrhdrkmomngxcjsatcpy.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJyaGRya21vbW5neGNqc2F0Y3B5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzU0MDQwODUsImV4cCI6MjA1MDk4MDA4NX0.yLnx5vQyZ49vwLlT1mKS_DGx1-MfLCXVZ4lJtWMIPlA
JWT_SECRET_KEY=your-super-secret-jwt-key-make-it-long-and-random
ENVIRONMENT=production
PORT=8000
```

### CORS Configuration
Your backend already allows all origins (`["*"]`) which works for development. For production, you might want to restrict this to your Lovable domain:

```python
# In main.py, update CORS to:
origins = [
    "https://b08e3d6b-734d-4dda-ba2e-871103b4a845.lovableproject.com",
    "https://localhost:3000",  # for local development
    "https://127.0.0.1:3000",
]
```

## 📱 STEP-BY-STEP DEPLOYMENT

### Step 1: Deploy Backend
1. Push your code to GitHub (if not already)
2. Go to Railway.app → "Deploy from GitHub"
3. Select your repository
4. Add environment variables
5. Deploy automatically starts

### Step 2: Update Lovable Frontend
1. Get your Railway URL (e.g., `https://token-market-backend.railway.app`)
2. In your Lovable project, update the API_BASE_URL

### Step 3: Test Integration
1. Open your Lovable app
2. Try registration/login
3. Check that marketplace loads
4. Verify user balance shows

## 🎯 ALTERNATIVE: Local Development with ngrok

If you want to test quickly without full deployment:

1. **Install ngrok**: `brew install ngrok` (Mac) or download from ngrok.com
2. **Run your backend locally**: `python start.py serve`
3. **Expose with ngrok**: `ngrok http 8000`
4. **Get public URL**: ngrok gives you something like `https://abc123.ngrok.io`
5. **Update Lovable**: Use the ngrok URL as your API_BASE_URL

## 🔧 UPDATED LOVABLE COMPONENT

Here's the updated API_BASE_URL line for your component:

```typescript
// Production URL (update with your actual deployed URL)
const API_BASE_URL = process.env.NODE_ENV === 'development' 
  ? 'http://localhost:8000' 
  : 'https://your-backend-url.railway.app';
```

## ✅ DEPLOYMENT CHECKLIST

- [ ] Backend deployed to Railway/Render/Heroku
- [ ] Environment variables configured
- [ ] CORS settings allow your Lovable domain
- [ ] Health check endpoint working (/health)
- [ ] Lovable frontend updated with new API URL
- [ ] Test authentication flow
- [ ] Test marketplace data loading
- [ ] Verify user balance display

Your backend is **production-ready** - it just needs to be hosted online so Lovable can reach it! 🚀
