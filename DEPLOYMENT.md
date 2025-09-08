# Deployment Guide for Kristal.AI's J.A.R.V.I.S

This guide will help you deploy the Kristal.AI's J.A.R.V.I.S application using Vercel (frontend) and Railway (backend).

## Architecture Overview

- **Frontend**: Next.js 15 application deployed on Vercel
- **Backend**: FastAPI application deployed on Railway
- **AI**: OpenAI Responses API with Code Interpreter
- **Data**: PDF documents and Excel returns data

## Prerequisites

1. **GitHub Account**: For hosting the code repository
2. **Vercel Account**: For frontend deployment
3. **Railway Account**: For backend deployment
4. **OpenAI Account**: With API key and access to Responses API

## Step 1: Prepare the Repository

### 1.1 Push to GitHub

```bash
# Initialize git repository
git init

# Add all files
git add .

# Commit changes
git commit -m "Initial commit: Kristal.AI JARVIS - AI-powered fund analysis system"

# Add remote origin
git remote add origin https://github.com/Elnino0009/FundSight.git

# Push to GitHub
git push -u origin main
```

### 1.2 Repository Structure

Ensure your repository has this structure:
```
FundSight/
├── frontend/                 # Next.js frontend
│   ├── src/
│   ├── package.json
│   ├── vercel.json
│   └── env.example
├── main.py                  # FastAPI backend
├── config.py
├── models.py
├── setup.py
├── requirements.txt
├── railway.json
├── Procfile
├── documents/               # PDF fund documents
├── metadata/               # JSON metadata files
└── Returns/                # Excel returns data
    ├── Returns.xlsx
    └── Returns.csv
```

## Step 2: Deploy Backend to Railway

### 2.1 Create Railway Project

1. Go to [Railway.app](https://railway.app)
2. Sign in with your GitHub account
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose your `FundSight` repository
6. Select the root directory (not frontend)

### 2.2 Configure Environment Variables

In Railway dashboard, go to your project → Variables tab and add:

```env
OPENAI_API_KEY=your_openai_api_key_here
HOST=0.0.0.0
PORT=8000
DEBUG=False
VECTOR_STORE_ID=
EXCEL_FILE_ID=
```

### 2.3 Deploy

1. Railway will automatically detect the Python project
2. It will install dependencies from `requirements.txt`
3. It will start the application using `main.py`
4. Note the generated URL (e.g., `https://your-app-name.railway.app`)

### 2.4 Setup AI Knowledge Base

After deployment, you need to run the setup script to initialize the AI knowledge base:

```bash
# SSH into your Railway deployment or run locally with Railway environment
python setup.py
```

This will:
- Upload all PDF documents to OpenAI
- Create a vector store
- Upload Excel returns data
- Save configuration to environment variables

## Step 3: Deploy Frontend to Vercel

### 3.1 Create Vercel Project

1. Go to [Vercel.com](https://vercel.com)
2. Sign in with your GitHub account
3. Click "New Project"
4. Import your `FundSight` repository
5. Set the **Root Directory** to `frontend`

### 3.2 Configure Environment Variables

In Vercel dashboard, go to your project → Settings → Environment Variables and add:

```env
NEXT_PUBLIC_API_URL=https://your-app-name.railway.app
```

Replace `your-app-name.railway.app` with your actual Railway backend URL.

### 3.3 Deploy

1. Vercel will automatically detect the Next.js project
2. It will install dependencies and build the project
3. It will deploy to a Vercel URL (e.g., `https://your-app.vercel.app`)

## Step 4: Update CORS Configuration

After getting your Vercel URL, update the CORS configuration in your Railway backend:

1. Go to Railway dashboard → Your project → Variables
2. Add a new environment variable:
   ```env
   FRONTEND_URL=https://your-app.vercel.app
   ```

3. Update `main.py` to use this environment variable for CORS origins

## Step 5: Test the Deployment

### 5.1 Test Backend

Visit your Railway URL + `/health`:
```
https://your-app-name.railway.app/health
```

You should see:
```json
{
  "status": "healthy",
  "files_configured": true,
  "api_type": "Responses API with Code Interpreter"
}
```

### 5.2 Test Frontend

Visit your Vercel URL and try asking a question about the funds.

## Step 6: Production Considerations

### 6.1 Security

- Keep your OpenAI API key secure
- Use environment variables for all sensitive data
- Consider rate limiting for production use
- Implement proper error handling

### 6.2 Performance

- Monitor API usage and costs
- Consider caching for frequently asked questions
- Optimize document processing
- Monitor response times

### 6.3 Monitoring

- Set up logging and monitoring
- Monitor API health
- Track usage metrics
- Set up alerts for failures

## Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure your frontend URL is added to CORS origins
2. **API Key Issues**: Verify your OpenAI API key is correct and has sufficient credits
3. **File Upload Failures**: Check that all documents are properly uploaded
4. **Build Failures**: Check the build logs in Vercel/Railway dashboards

### Debug Commands

```bash
# Check backend health
curl https://your-app-name.railway.app/health

# Test API endpoint
curl -X POST https://your-app-name.railway.app/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What funds are available?"}'
```

## Environment Variables Reference

### Backend (Railway)
- `OPENAI_API_KEY`: Your OpenAI API key
- `VECTOR_STORE_ID`: Created by setup.py
- `EXCEL_FILE_ID`: Created by setup.py
- `HOST`: Server host (0.0.0.0 for Railway)
- `PORT`: Server port (8000)
- `DEBUG`: Debug mode (False for production)

### Frontend (Vercel)
- `NEXT_PUBLIC_API_URL`: Your Railway backend URL

## Support

For issues or questions:
1. Check the deployment logs in Vercel/Railway dashboards
2. Verify all environment variables are set correctly
3. Ensure the setup.py script ran successfully
4. Check the health endpoint for backend status
