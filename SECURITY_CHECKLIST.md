# 🔒 Security Checklist for Manual Upload

## Files to NEVER Upload (Contains Sensitive Data)

### ❌ DO NOT UPLOAD THESE FILES:
- `.env` - Contains your OpenAI API key
- `.env.local` - Contains local configuration
- `frontend/.env.local` - Frontend environment variables
- `frontend/frontend_backup/.env.local` - Backup environment file
- Any file with "backup" in the name
- `__pycache__/` directories
- `node_modules/` directories
- `.git/` directory
- `*.log` files

## Files Safe to Upload ✅

### Backend Files:
- `main.py` - Main FastAPI application
- `config.py` - Configuration management
- `models.py` - Pydantic models
- `setup.py` - AI knowledge base setup
- `requirements.txt` - Python dependencies
- `railway.json` - Railway deployment config
- `Procfile` - Process file for Railway
- `nixpacks.toml` - Railway build config
- `Dockerfile` - Docker configuration
- `env.example` - Environment template (safe)

### Frontend Files:
- `frontend/src/` - All source code
- `frontend/public/` - Static assets
- `frontend/package.json` - Dependencies
- `frontend/vercel.json` - Vercel config
- `frontend/env.example` - Environment template (safe)
- `frontend/tsconfig.json` - TypeScript config
- `frontend/next.config.ts` - Next.js config

### Documentation:
- `README.md` - Project documentation
- `DEPLOYMENT.md` - Deployment guide
- `SECURITY_CHECKLIST.md` - This file

### Data Files (Optional):
- `documents/` - PDF fund documents (if not too large)
- `metadata/` - JSON metadata files
- `Returns/` - Excel returns data

## Step-by-Step Upload Process

### 1. Prepare Your Files
```bash
# Run the preparation script
./prepare_upload.sh
```

### 2. Go to GitHub Repository
1. Visit: https://github.com/Elnino0009/FundSight
2. Click "uploading an existing file" or drag and drop
3. Upload files from the `FundSight_Clean` directory

### 3. After Upload - Set Environment Variables

#### For Railway (Backend):
- `OPENAI_API_KEY` = Your actual OpenAI API key
- `HOST` = 0.0.0.0
- `PORT` = 8000
- `DEBUG` = False
- `VECTOR_STORE_ID` = (will be set by setup.py)
- `EXCEL_FILE_ID` = (will be set by setup.py)

#### For Vercel (Frontend):
- `NEXT_PUBLIC_API_URL` = Your Railway backend URL

## Security Best Practices

### ✅ What We've Done:
1. Created `.gitignore` to exclude sensitive files
2. Used `env.example` files as templates
3. Added security warnings in documentation
4. Created preparation script to exclude sensitive files

### 🔍 Double-Check Before Upload:
1. No `.env` files in the upload
2. No API keys in the code
3. No personal information in comments
4. No database credentials
5. No private tokens or secrets

## After Upload - Next Steps

### 1. Deploy Backend to Railway
1. Connect GitHub repository to Railway
2. Set environment variables
3. Deploy
4. Run `python setup.py` to initialize AI knowledge base

### 2. Deploy Frontend to Vercel
1. Connect GitHub repository to Vercel
2. Set `NEXT_PUBLIC_API_URL` to your Railway URL
3. Deploy

### 3. Test the Application
1. Check Railway health endpoint
2. Test frontend connection to backend
3. Verify AI functionality

## Emergency Response

If you accidentally upload sensitive data:
1. **Immediately** revoke your OpenAI API key
2. Generate a new API key
3. Update all environment variables
4. Consider the old key compromised

## Support

If you have any questions about security or need help with the upload process, refer to the DEPLOYMENT.md file or create an issue in the repository.
