# 📤 Manual Upload Guide

## Quick Steps

### 1. Go to GitHub Repository
Visit: https://github.com/Elnino0009/FundSight

### 2. Upload Files
- Click "uploading an existing file" or drag and drop
- Navigate to the `../FundSight_Clean` directory
- Select ALL files and folders
- Click "Commit changes"

### 3. Verify Upload
Check that these key files are uploaded:
- ✅ `main.py` (backend)
- ✅ `frontend/` directory (frontend)
- ✅ `README.md` (documentation)
- ✅ `requirements.txt` (dependencies)
- ✅ `railway.json` (Railway config)
- ✅ `frontend/vercel.json` (Vercel config)

### 4. What's NOT Uploaded (Good!)
- ❌ `.env` files (contains your API keys)
- ❌ `node_modules/` (large build files)
- ❌ `.next/` (build cache)
- ❌ `__pycache__/` (Python cache)

## After Upload - Deploy

### Backend (Railway)
1. Connect GitHub repo to Railway
2. Set environment variables:
   - `OPENAI_API_KEY` = your actual key
   - `HOST` = 0.0.0.0
   - `PORT` = 8000
   - `DEBUG` = False
3. Deploy
4. Run `python setup.py` to initialize AI

### Frontend (Vercel)
1. Connect GitHub repo to Vercel
2. Set root directory to `frontend`
3. Set environment variable:
   - `NEXT_PUBLIC_API_URL` = your Railway URL
4. Deploy

## Security ✅
- No API keys in the uploaded code
- No sensitive configuration files
- Only safe template files included
- All sensitive data excluded by the preparation script
