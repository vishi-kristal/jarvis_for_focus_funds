# Kristal.AI's J.A.R.V.I.S - AI-Powered Fund Analysis System

An intelligent fund analysis platform that combines document search with financial calculations using OpenAI's Responses API, Code Interpreter, and modern web technologies.

## 🚀 Quick Deploy

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/deploy)
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new)

## 📋 Overview

This full-stack application provides AI-powered analysis of investment fund documents with the following capabilities:

- **Document Analysis**: Search and analyze 100+ fund documents using vector search.
- **Financial Calculations**: Compute metrics like Sharpe ratio, max drawdown, volatility using real returns data.
- **Hybrid Intelligence**: Combines document insights with precise Excel calculations
- **Modern UI**: Beautiful Next.js 15 frontend with real-time chat interface
- **Production Ready**: Deployed on Vercel (frontend) + Railway (backend)

## Overview

This backend provides a FastAPI-based service that allows financial analysts to query a knowledge base of 100+ fund documents using natural language. The system leverages OpenAI's file search capabilities and vector stores to provide accurate, context-aware answers about investment funds.

## Features

- **Document Processing**: Upload and process PDF fund documents and JSON metadata files
- **Vector Store Management**: Automatic creation and management of OpenAI vector stores
- **AI Assistant**: Specialized fund analysis assistant with file search capabilities
- **RESTful API**: FastAPI-based API with comprehensive error handling
- **CORS Support**: Configured for frontend integration
- **Comprehensive Logging**: Detailed logging for debugging and monitoring.

## Project Structure

```
├── main.py              # FastAPI application and runtime API
├── setup.py             # One-time setup script for initialization
├── config.py            # Configuration management
├── models.py            # Pydantic models for request/response validation
├── requirements.txt     # Python dependencies
├── env.example          # Environment variables template
├── README.md           # This file
├── documents/          # Directory for PDF fund documents (create this)
└── metadata/           # Directory for JSON metadata files (create this)
```

## Prerequisites

- Python 3.8 or higher
- OpenAI API key with access to the Responses API
- Fund documents in PDF format
- Optional: JSON metadata files

## 🚀 Deployment

### Option 1: One-Click Deploy (Recommended)

1. **Deploy Backend to Railway**:
   - Click the Railway deploy button above
   - Connect your GitHub account
   - Set environment variables (see DEPLOYMENT.md)
   - Deploy!

2. **Deploy Frontend to Vercel**:
   - Click the Vercel deploy button above
   - Connect your GitHub account
   - Set `NEXT_PUBLIC_API_URL` to your Railway backend URL
   - Deploy!

### Option 2: Manual Deployment

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed step-by-step instructions.

## 🛠️ Local Development

### Prerequisites

- Python 3.8+
- Node.js 18+
- OpenAI API key

### Backend Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**:
   ```bash
   cp env.example .env
   ```
   
   Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. **Prepare your documents**:
   - Add PDF fund documents to `documents/` directory
   - Add JSON metadata files to `metadata/` directory (optional)
   - Add `Returns.xlsx` to `Returns/` directory

4. **Initialize AI knowledge base**:
   ```bash
   python setup.py
   ```

5. **Start the backend**:
   ```bash
   python main.py
   ```

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Set up environment variables**:
   ```bash
   cp env.example .env.local
   ```
   
   Edit `.env.local` and set your backend URL:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

4. **Start the frontend**:
   ```bash
   npm run dev
   ```

5. **Open your browser**:
   Visit `http://localhost:3000`

## Setup (One-time initialization)

Before running the API, you need to initialize the AI knowledge base:

```bash
python setup.py
```

This script will:
1. Upload all PDF files from `documents/` directory
2. Upload all JSON files from `metadata/` directory
3. Create a vector store with all uploaded documents
4. Create an AI assistant with file search capabilities
5. Save the configuration to your `.env` file

**Important**: This is a one-time setup process. The script will create persistent resources in your OpenAI account.

## Running the API

Start the FastAPI server:

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at:
- **API Base URL**: `http://localhost:8000`
- **Interactive Docs**: `http://localhost:8000/docs`
- **Health Check**: `http://localhost:8000/health`

## API Endpoints

### POST /api/ask

Ask a question about fund documents.

**Request Body**:
```json
{
  "question": "What is the expense ratio of the ABC Growth Fund?"
}
```

**Response**:
```json
{
  "answer": "Based on the fund documents, the ABC Growth Fund has an expense ratio of 0.75%..."
}
```

### GET /health

Check the health status of the API and configuration.

**Response**:
```json
{
  "status": "healthy",
  "assistant_configured": true,
  "vector_store_configured": true
}
```

### GET /

Root endpoint for basic health check.

**Response**:
```json
{
  "message": "GenAI FundScreener API is running",
  "version": "1.0.0",
  "status": "healthy"
}
```

## Configuration

The application uses the following environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `ASSISTANT_ID`: ID of the created assistant (set by setup.py)
- `VECTOR_STORE_ID`: ID of the created vector store (set by setup.py)
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)
- `DEBUG`: Debug mode (default: True)

## Usage Examples

### Example Questions

The AI assistant can handle various types of questions:

- **Specific Fund Information**: "What is the performance of XYZ Fund over the last 3 years?"
- **Comparison Questions**: "Compare the expense ratios of Fund A and Fund B"
- **Data Extraction**: "What are the top 10 holdings in the Technology Fund?"
- **Analysis Questions**: "What is the risk profile of the Emerging Markets Fund?"
- **Summary Requests**: "Summarize the investment strategy of the Balanced Fund"

### Frontend Integration

The API is configured with CORS to allow requests from `http://localhost:3000` (Next.js development server). To integrate with your frontend:

```javascript
const response = await fetch('http://localhost:8000/api/ask', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    question: 'Your question here'
  })
});

const data = await response.json();
console.log(data.answer);
```

## Error Handling

The API includes comprehensive error handling:

- **400 Bad Request**: Invalid request format
- **500 Internal Server Error**: Assistant not configured or API errors
- **504 Gateway Timeout**: Request timeout (5 minutes)

All errors return a consistent format:
```json
{
  "error": "Error message",
  "detail": "Additional details if available"
}
```

## Logging

The application logs important events and errors:

- File upload progress during setup
- API request processing
- Error conditions and debugging information

Logs are written to the console with timestamps and log levels.

## Troubleshooting

### Common Issues

1. **"Assistant not configured" error**:
   - Run `python setup.py` to initialize the assistant
   - Ensure your `.env` file contains the `ASSISTANT_ID` and `VECTOR_STORE_ID`

2. **"OPENAI_API_KEY is required" error**:
   - Add your OpenAI API key to the `.env` file
   - Ensure the key has access to the Responses API

3. **File upload failures**:
   - Check that PDF files are not corrupted
   - Ensure files are in the correct directories (`documents/` and `metadata/`)
   - Verify your OpenAI API key has sufficient credits

4. **CORS errors in frontend**:
   - Ensure the frontend is running on `http://localhost:3000`
   - Check that the backend is running on `http://localhost:8000`

### Debug Mode

Run with debug mode enabled for detailed logging:
```bash
DEBUG=True python main.py
```

## Development

### Adding New Features

1. **New API Endpoints**: Add to `main.py`
2. **New Models**: Add to `models.py`
3. **Configuration Changes**: Update `config.py`
4. **Setup Modifications**: Update `setup.py`

### Testing

Test the API using the interactive documentation at `http://localhost:8000/docs` or with curl:

```bash
curl -X POST "http://localhost:8000/api/ask" \
     -H "Content-Type: application/json" \
     -d '{"question": "What funds are available?"}'
```

## License

This project is part of the GenAI FundScreener application. Please ensure you have appropriate licenses for any fund documents you process.

## Support

For issues or questions:
1. Check the logs for error messages
2. Verify your OpenAI API key and credits
3. Ensure all setup steps were completed successfully
4. Check the health endpoint for configuration status
