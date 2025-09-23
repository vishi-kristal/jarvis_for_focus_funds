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
    """Enhanced service class for handling AI interactions using Responses API with Code Interpreter."""
    
    def __init__(self):
        # For Responses API, we need the vector store ID for file search and CSV data for calculations
        self.vector_store_id = config.vector_store_id
        self.excel_file_id = config.excel_file_id
        self.metadata_file_id = getattr(config, 'metadata_file_id', None)
        self.csv_data = self.load_csv_data()
        self.metadata_csv_data = self.load_metadata_csv_data()
        self.files_configured = bool(self.vector_store_id and self.csv_data)
        
        if not self.files_configured:
            logger.warning("Vector store or CSV data not configured. Run setup.py first.")
        else:
            logger.info(f"Enhanced J.A.R.V.I.S service initialized")
            logger.info(f"📁 Vector store: {self.vector_store_id}")
            logger.info(f"📊 Excel file: {self.excel_file_id}")
            logger.info(f"📄 CSV data loaded: {len(self.csv_data)} characters")
            if self.metadata_csv_data:
                logger.info(f"📋 Metadata CSV data loaded: {len(self.metadata_csv_data)} characters")
    
    def load_metadata_csv_data(self) -> str:
        """Load CSV data from the focus_funds_metadata.csv file."""
        metadata_path = Path("metadata/focus_funds_metadata.csv")
        
        if not metadata_path.exists():
            logger.warning(f"Metadata CSV file not found: {metadata_path}")
            return None
        
        try:
            with open(metadata_path, 'r', encoding='utf-8') as f:
                csv_data = f.read()
            logger.info(f"Metadata CSV data loaded: {len(csv_data)} characters")
            return csv_data
        except Exception as e:
            logger.error(f"Failed to load metadata CSV data: {str(e)}")
            return None
    
    def load_csv_data(self) -> str:
        """Load CSV data from the Returns.csv file."""
        csv_path = Path("Returns/Returns.csv")
        
        if not csv_path.exists():
            logger.warning(f"CSV file not found: {csv_path}")
            return None
        
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                csv_data = f.read()
            logger.info(f"CSV data loaded: {len(csv_data)} characters")
            return csv_data
        except Exception as e:
            logger.error(f"Failed to load CSV data: {str(e)}")
            return None
    
    def classify_question(self, question: str) -> str:
        """Classify question type to determine processing approach."""
        
        # Metadata query keywords
        metadata_keywords = [
            "list", "show", "which", "what funds", "available", "funds in",
            "geography", "asset type", "instrument type", "strategy", "sub-category",
            "hedge fund", "mutual fund", "equity", "fixed income", "market neutral",
            "alternatives", "low vol", "high vol", "global", "asia", "emerging markets",
            "india", "united states", "arbitrage", "global macro", "long short",
            "cryptocurrency", "technology", "credit", "options", "multi-asset"
        ]
        
        calculation_keywords = [
            "calculate", "compute", "max drawdown", "sharpe ratio",
            "volatility", "vol", "annualized", "correlation", "beta", "alpha", "sortino",
            "information ratio", "treynor ratio", "calmar ratio",
            "var", "cvar", "skewness", "kurtosis", "jensen's alpha",
            "what is the", "show me the", "how much", "performance"
        ]
        
        question_lower = question.lower()
        
        # Check for calculation queries first (most specific)
        if any(keyword in question_lower for keyword in calculation_keywords):
            return "CALCULATION_REQUIRED"
        # Check for metadata queries second
        elif any(keyword in question_lower for keyword in metadata_keywords):
            return "METADATA_QUERY"
        elif "compare" in question_lower and any(metric in question_lower for metric in ["performance", "return", "risk", "ratio"]):
            return "COMPARISON_REQUIRED"
        else:
            return "DOCUMENT_SEARCH"
    
    def requires_calculation(self, question: str, document_response: str) -> bool:
        """Determine if calculation is needed based on question and document response."""
        
        # Check if document response indicates missing data
        if any(phrase in document_response.lower() for phrase in [
            "data not available", "not found in documents", 
            "information not provided", "no data available"
        ]):
            return True
        
        # Check for specific calculation requests
        calculation_indicators = [
            "max drawdown", "sharpe ratio", "volatility", "correlation",
            "calculate", "compute", "what is the", "show me the"
        ]
        
        return any(indicator in question.lower() for indicator in calculation_indicators)
    
    async def ask_question(self, question: str) -> dict:
        """
        Enhanced question processing with hybrid document search + Excel calculations.
        
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
                detail="Files not configured. Please run setup.py first."
            )
        
        try:
            logger.info(f"Processing question: {question[:100]}...")
            
            # Step 1: Classify question type
            question_type = self.classify_question(question)
            logger.info(f"Question type: {question_type}")
            
            if question_type == "METADATA_QUERY":
                return await self.query_metadata(question)
            elif question_type == "CALCULATION_REQUIRED":
                logger.info("Calculation required, using hybrid approach")
                return await self.hybrid_analysis(question, "")
            elif question_type == "COMPARISON_REQUIRED":
                logger.info("Comparison required, using hybrid approach")
                return await self.hybrid_analysis(question, "")
            elif question_type == "DOCUMENT_SEARCH":
                return await self.search_documents_only(question)
            
            # Fallback: Try document search first
            document_response = await self.search_documents(question)
            
            # Check if calculation is needed
            if self.requires_calculation(question, document_response.get("content", "")):
                logger.info("Calculation required, using hybrid approach")
                return await self.hybrid_analysis(question, document_response.get("content", ""))
            
            return document_response
            
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
    
    async def query_metadata(self, question: str) -> dict:
        """Query fund metadata using code interpreter with CSV data."""
        
        logger.info("🔍 Starting metadata query...")
        
        # Use the local CSV data directly (works for both local and cloud deployment)
        if not self.metadata_csv_data:
            logger.warning("Metadata CSV data not available. Cannot process metadata query.")
            return {"content": "Metadata data not available. Please ensure the metadata CSV file is properly loaded.", "images": []}
        
        metadata_instructions = f"""
        You are J.A.R.V.I.S, an AI assistant for fund metadata analysis.

        ## AVAILABLE DATA:
        **Fund Metadata CSV Data:**
        {self.metadata_csv_data}

        ## USER QUESTION: 
        {question}

        ## TASK:
        Analyze the fund metadata CSV data to answer the user's question about funds.

        ## DATA STRUCTURE:
        - kristalid: Unique fund identifier
        - kristal_name: Fund name
        - Asset Type Exposure: Equity, Fixed Income, Market Neutral, Alternatives - Low Vol, Alternatives - High Vol, Alternatives - Fixed Income
        - Instrument Type: Hedge Fund, Mutual Fund
        - Geography: Global, Emerging Markets, India, Asia, United States
        - Sub-Category: Specific strategy (e.g., Equity Long/Short, Arbitrage, Global Macro, etc.)

        ## REQUIREMENTS:
        1. **Load and analyze the CSV data** using pandas
        2. **Filter and query** based on the user's question
        3. **Provide clear, structured results** with fund names and key details
        4. **Create visualizations** if helpful (charts, tables, graphs)
        5. **Format results professionally** with proper tables and formatting
        6. **Include counts and summaries** where relevant

        ## RESPONSE FORMAT:
        - Use markdown formatting for better readability
        - Include tables for fund listings
        - Use bullet points for lists and key points
        - Bold important information
        - Provide clear section headers
        - Include summary statistics

        ## EXAMPLES OF GOOD RESPONSES:
        - "Found 3 funds in Asia: [list with details]"
        - "There are 12 hedge funds available: [table with all hedge funds]"
        - "Equity funds breakdown: [chart showing distribution]"

        Remember: Focus on providing accurate, helpful information about the fund metadata.
        """
        
        try:
            logger.info("🤖 Calling OpenAI API for metadata query...")
            logger.info(f"🔧 Using code interpreter with CSV data ({len(self.metadata_csv_data)} characters)")
            
            response = client.responses.create(
                model="gpt-4o",
                input=question,
                instructions=metadata_instructions,
                tools=[{"type": "code_interpreter", "container": {"type": "auto"}}],
                max_tool_calls=5
            )
            
            logger.info("✅ Metadata query completed successfully")
            logger.info("📝 Extracting response content...")
            
            result = self.extract_response_content(response)
            logger.info(f"📊 Response extracted: {len(result.get('content', ''))} characters")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Error in metadata query: {str(e)}")
            logger.error(f"Error type: {type(e).__name__}")
            return {"content": f"Error in metadata query: {str(e)}", "images": []}
    
    
    async def hybrid_analysis(self, question: str, document_context: str) -> dict:
        """Combine document search with Excel calculations"""
        
        enhanced_instructions = f"""
        You are J.A.R.V.I.S (Just A Rather Very Intelligent System), Kristal.AI's specialized AI assistant for fund analysis.

        ## AVAILABLE DATA:
        **Returns Data**: CSV with monthly returns for all funds (provided below)

        ## USER QUESTION: 
        {question}

        ## PROCESSING APPROACH:
        1. **Load and analyze the returns data** from the CSV data provided below
        2. **Calculate the requested financial metrics** accurately using the actual data
        3. **Provide exact formulas and methodology** used for calculations
        4. **Include confidence intervals** where appropriate
        5. **Create visualizations** for complex metrics (charts, graphs, plots)

        ## RETURNS DATA (CSV Format):
        {self.csv_data}

        ## CALCULATION REQUIREMENTS:
        - Load and analyze the returns data from the CSV data provided above
        - Calculate the requested financial metrics accurately using the actual data
        - Provide exact formulas and methodology used for calculations
        - Include confidence intervals where appropriate
        - Create visualizations for complex metrics (charts, graphs, plots)
        - Format results professionally with proper units

        ## RESPONSE FORMAT:
        - Use markdown formatting for better readability
        - Include tables for comparative data
        - Use bullet points for lists and key points
        - Bold important metrics and conclusions
        - Provide clear section headers
        - Show exact formulas and calculations

        ## DATA ACCURACY REQUIREMENTS:
        1. **ONLY use data from the provided CSV** - Never make assumptions
        2. **If data is missing, explicitly state "Data not available"**
        3. **For calculations, show the exact formula used**
        4. **Include confidence intervals for statistical measures**

        Remember: Your goal is to provide accurate calculations using the actual returns data provided.
        """
        
        response = client.responses.create(
            model="gpt-4o",
            input=question,
            instructions=enhanced_instructions,
            tools=[
                {"type": "file_search", "vector_store_ids": [self.vector_store_id]},
                {"type": "code_interpreter", "container": {"type": "auto"}}
            ],
            max_tool_calls=10
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
    """Enhanced health check with Excel file status."""
    return {
        "status": "healthy",
        "files_configured": service.files_configured,
        "api_type": "Responses API with Code Interpreter",
        "data_sources": {
            "documents": bool(config.vector_store_id),
            "excel_returns": bool(config.excel_file_id),
            "csv_returns": bool(service.csv_data)
        },
        "vector_store_id": config.vector_store_id,
        "excel_file_id": config.excel_file_id,
        "capabilities": [
            "Document search and analysis",
            "Financial metrics calculations",
            "Excel data processing",
            "Hybrid analysis (documents + calculations)"
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
