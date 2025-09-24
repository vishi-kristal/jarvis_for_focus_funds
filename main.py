"""
FastAPI application for the GenAI FundScreener backend.
Provides the runtime API for the Next.js frontend to interact with the AI using Responses API.
"""

import logging
from typing import Dict, Any, List
from pathlib import Path
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from openai import OpenAI
from config import config
from models import QuestionRequest, AnswerResponse, ErrorResponse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Kristal.AI's J.A.R.V.I.S API",
    description="AI-powered fund analysis API using OpenAI's Responses API",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://127.0.0.1:3000",
        "https://jarvis-for-focus-funds.vercel.app",
        "https://jarvis-for-focus-funds-hoemvmfhe.vercel.app",
        "https://jarvis-for-focus-funds-m47bbmm5n.vercel.app",
        "https://web-production-1ea6.up.railway.app"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Initialize OpenAI client
client = OpenAI(api_key=config.openai_api_key)

class EnhancedKristalJARVISService:
    """Service class for handling AI interactions using Responses API for document search."""
    
    def __init__(self):
        # For Responses API, we need the vector store ID for file search
        self.vector_store_id = config.vector_store_id
        self.files_configured = bool(self.vector_store_id)
        
        if not self.files_configured:
            logger.warning("Vector store not configured. Run setup.py first.")
        else:
            logger.info(f"J.A.R.V.I.S service initialized")
            logger.info(f"📁 Vector store: {self.vector_store_id}")
    
    
    
    async def ask_question(self, question: str) -> dict:
        """
        Process question using document search only.
        
        Args:
            question: The user's question about fund documents
            
        Returns:
            Dictionary with AI's answer and any generated images
            
        Raises:
            HTTPException: If files are not configured or if there's an API error
        """
        if not self.files_configured:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Vector store not configured. Please run setup.py first."
            )
        
        try:
            logger.info(f"Processing question: {question[:100]}...")
            
            # Use document search only
            return await self.search_documents_only(question)
            
        except Exception as e:
            logger.error(f"Error processing question: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to process question: {str(e)}"
            )
    
    async def search_documents_only(self, question: str) -> dict:
        """Search documents only (no calculations)"""
        response = client.responses.create(
            model="gpt-4o",
            input=question,
            instructions=self.get_document_search_instructions(),
            tools=[{"type": "file_search", "vector_store_ids": [self.vector_store_id]}],
            max_tool_calls=5
        )
        
        return self.extract_response_content(response)
    
    async def search_documents(self, question: str) -> dict:
        """Search documents for context"""
        response = client.responses.create(
            model="gpt-4o",
            input=question,
            instructions=self.get_document_search_instructions(),
            tools=[{"type": "file_search", "vector_store_ids": [self.vector_store_id]}],
            max_tool_calls=5
        )
        
        return self.extract_response_content(response)
    
    
    
    
    def get_document_search_instructions(self) -> str:
        """Get instructions for document-only search"""
        return """You are J.A.R.V.I.S, Kristal.AI's specialized AI assistant for fund analysis.

        ## CRITICAL DATA ACCURACY REQUIREMENTS:
        1. **ONLY use data from provided documents** - Never make assumptions
        2. **If data is missing, explicitly state "Data not available in provided documents"**
        3. **Always cite the specific document source** for any data you provide
        4. **For performance data, include the exact date range and calculation method**

        ## Your Role and Expertise
        You are an expert in investment fund analysis, financial document interpretation, and fund performance metrics.

        ## Guidelines for Responses
        1. **Accuracy First**: Always base your answers on the provided documents
        2. **Professional Tone**: Maintain a professional, analytical tone
        3. **Data-Driven**: Include specific numbers, percentages, and metrics
        4. **Clear Structure**: Organize responses with clear headings and bullet points
        5. **Source Attribution**: Mention the source document for all data points

        ## Response Format
        - Use markdown formatting for better readability
        - Include tables for comparative data
        - Use bullet points for lists and key points
        - Bold important metrics and conclusions
        - Provide clear section headers

        ## Limitations
        - You can only access information from the provided fund documents
        - You cannot provide real-time market data or current fund prices
        - You cannot give specific investment advice or recommendations
        - Always recommend consulting with qualified financial advisors for investment decisions
        """
    
    def extract_response_content(self, response) -> dict:
        """Extract content and images from OpenAI response"""
        content = ""
        images = []
        
        if hasattr(response, 'output') and response.output and len(response.output) > 0:
            for item in response.output:
                if hasattr(item, 'content') and item.content:
                    if len(item.content) > 0:
                        content += item.content[0].text
                
                if hasattr(item, 'code_interpreter_outputs'):
                    for output in item.code_interpreter_outputs:
                        if hasattr(output, 'image'):
                            if hasattr(output.image, 'file_id'):
                                # If it's a file reference, we'd need to download it
                                # For now, we'll handle base64 data directly
                                pass
                            elif hasattr(output.image, 'data'):
                                # Base64 encoded image
                                images.append(output.image.data)
        
        return {
            "content": content if content else "No response generated",
            "images": images
        }

# Initialize enhanced service
service = EnhancedKristalJARVISService()

@app.get("/")
async def root():
    """Root endpoint for health check."""
    return {
        "message": "Kristal.AI's J.A.R.V.I.S API is running",
        "version": "1.0.0",
        "status": "healthy"
    }

@app.get("/health")
async def health_check():
    """Health check with vector store status."""
    return {
        "status": "healthy",
        "files_configured": service.files_configured,
        "api_type": "Responses API Document Search",
        "data_sources": {
            "documents": bool(config.vector_store_id)
        },
        "vector_store_id": config.vector_store_id,
        "capabilities": [
            "Document search and analysis"
        ]
    }

@app.post("/api/ask")
async def ask_question(request: QuestionRequest):
    """
    Ask a question to the AI assistant about fund documents.
    
    Args:
        request: The question request containing the user's question
        
    Returns:
        The AI assistant's answer with optional images
        
    Raises:
        HTTPException: If there's an error processing the question
    """
    try:
        result = await service.ask_question(request.question)
        return {
            "answer": result.get("content", ""),
            "images": result.get("images", [])
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in ask_question: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while processing your question."
        )

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "detail": f"Status code: {exc.status_code}"
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler for unexpected errors."""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "An unexpected error occurred",
            "detail": str(exc)
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=config.host,
        port=config.port,
        reload=config.debug
    )
