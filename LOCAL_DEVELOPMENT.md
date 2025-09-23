# J.A.R.V.I.S Local Development Guide

## 🚀 Quick Start

### Option 1: Use the Interactive Script (Recommended)
```bash
./run_local.sh
```

### Option 2: Manual Setup

#### 1. Backend Setup
```bash
# Install Python dependencies
pip3 install -r requirements.txt

# Start the backend server
python3 main.py
```
Backend will be available at: http://localhost:8000

#### 2. Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies (if not already done)
npm install

# Start the frontend server
npm run dev
```
Frontend will be available at: http://localhost:3000

## 📋 Prerequisites

- **Python 3.8+** (You have Python 3.11.3 ✅)
- **Node.js 18+** (You have Node.js v23.11.0 ✅)
- **OpenAI API Key** (Already configured in .env ✅)

## 🔧 Configuration

### Backend Configuration (.env)
```bash
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Application Configuration
ASSISTANT_ID=vs_68cc50bd8b108191a6d17bd26b0fdf1a
VECTOR_STORE_ID=vs_68cc50bd8b108191a6d17bd26b0fdf1a
EXCEL_FILE_ID=file-2G2xahfAQqZ93hRo8jarAZ

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

### Frontend Configuration (.env.local)
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🤖 AI Knowledge Base Setup

**Important**: Before using the application, you need to set up the AI knowledge base:

```bash
python3 setup.py
```

This will:
1. Upload all PDF files from `documents/` directory
2. Upload all JSON files from `metadata/` directory  
3. Create a vector store with all uploaded documents
4. Create an AI assistant with file search capabilities
5. Save the configuration to your `.env` file

## 🌐 Access Points

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🧪 Testing the Setup

### Test Backend Health
```bash
curl http://localhost:8000/health
```

### Test API Endpoint
```bash
curl -X POST "http://localhost:8000/api/ask" \
     -H "Content-Type: application/json" \
     -d '{"question": "What funds are available?"}'
```

## 📁 Project Structure

```
jarvis_for_focus_funds/
├── main.py                 # FastAPI backend
├── setup.py               # AI knowledge base setup
├── config.py              # Configuration management
├── models.py              # Pydantic models
├── requirements.txt       # Python dependencies
├── .env                   # Backend environment variables
├── run_local.sh           # Local development script
├── documents/             # PDF fund documents (100+ files)
├── metadata/              # JSON metadata files
├── Returns/               # Excel/CSV returns data
└── frontend/              # Next.js frontend
    ├── src/
    ├── package.json
    ├── .env.local         # Frontend environment variables
    └── ...
```

## 🔍 Troubleshooting

### Common Issues

1. **"Assistant not configured" error**
   - Run `python3 setup.py` to initialize the AI assistant
   - Ensure your `.env` file contains the `ASSISTANT_ID` and `VECTOR_STORE_ID`

2. **"OPENAI_API_KEY is required" error**
   - Add your OpenAI API key to the `.env` file
   - Ensure the key has access to the Responses API

3. **CORS errors in frontend**
   - Ensure the frontend is running on `http://localhost:3000`
   - Check that the backend is running on `http://localhost:8000`
   - Verify `.env.local` has `NEXT_PUBLIC_API_URL=http://localhost:8000`

4. **Port already in use**
   - Backend: Change `PORT=8000` to another port in `.env`
   - Frontend: Use `npm run dev -- -p 3001` for different port

5. **Module not found errors**
   - Backend: Run `pip3 install -r requirements.txt`
   - Frontend: Run `cd frontend && npm install`

### Debug Mode

Run with debug mode enabled for detailed logging:
```bash
DEBUG=True python3 main.py
```

## 🚀 Development Workflow

1. **Start Development Servers**
   ```bash
   ./run_local.sh
   # Choose option 3 to start both backend and frontend
   ```

2. **Make Changes**
   - Backend changes: Edit Python files in root directory
   - Frontend changes: Edit files in `frontend/src/` directory
   - Both servers will auto-reload on changes

3. **Test Changes**
   - Frontend: Visit http://localhost:3000
   - Backend: Visit http://localhost:8000/docs
   - API: Use the interactive documentation

4. **Stop Servers**
   - Press `Ctrl+C` in the terminal running the servers

## 📊 Available Data

The application comes with:
- **100+ PDF fund documents** in `documents/` directory
- **Excel returns data** in `Returns/Returns.xlsx`
- **Metadata files** in `metadata/` directory

## 🎯 Next Steps

1. Run the setup script: `./run_local.sh`
2. Choose option 4 to set up the AI knowledge base
3. Choose option 3 to start both servers
4. Open http://localhost:3000 in your browser
5. Start asking questions about the funds!

## 💡 Tips

- The AI assistant can answer questions about fund performance, risk metrics, and comparisons
- Use the API documentation at http://localhost:8000/docs to test endpoints
- Check the health endpoint to verify everything is working
- All changes are automatically saved to the `development` branch
