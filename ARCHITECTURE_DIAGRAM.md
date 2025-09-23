# Kristal.AI's J.A.R.V.I.S System Architecture

## System Overview
This is an AI-powered fund analysis system that combines document search, financial calculations, and metadata queries to provide comprehensive fund insights.

## Architecture Diagram

```mermaid
graph TB
    %% User Interface Layer
    subgraph "Frontend Layer (Next.js 15)"
        UI[ChatWindow Component]
        Input[UserInput Component]
        Messages[MessageList Component]
        Processing[ProcessingIndicator]
        API[API Client]
    end

    %% Backend API Layer
    subgraph "Backend Layer (FastAPI)"
        FastAPI[FastAPI Application]
        CORS[CORS Middleware]
        Routes[API Routes]
        Service[EnhancedKristalJARVISService]
        Config[Configuration Manager]
    end

    %% AI Processing Layer
    subgraph "AI Processing Layer"
        Classifier[Question Classifier]
        DocSearch[Document Search]
        MetadataQuery[Metadata Query]
        HybridAnalysis[Hybrid Analysis]
        CodeInterpreter[Code Interpreter]
    end

    %% Data Sources
    subgraph "Data Sources"
        VectorStore[Vector Store<br/>PDF Documents]
        ReturnsCSV[Returns.csv<br/>Monthly Returns Data]
        MetadataCSV[focus_funds_metadata.csv<br/>Fund Metadata]
        ExcelFile[Excel File<br/>Structured Data]
    end

    %% External Services
    subgraph "External Services"
        OpenAI[OpenAI API<br/>GPT-4o + Responses API]
        FileSearch[File Search Tool]
        CodeTool[Code Interpreter Tool]
    end

    %% Data Flow
    UI --> Input
    Input --> API
    API --> FastAPI
    FastAPI --> CORS
    CORS --> Routes
    Routes --> Service
    Service --> Classifier

    %% Question Classification Flow
    Classifier -->|METADATA_QUERY| MetadataQuery
    Classifier -->|CALCULATION_REQUIRED| HybridAnalysis
    Classifier -->|COMPARISON_REQUIRED| HybridAnalysis
    Classifier -->|DOCUMENT_SEARCH| DocSearch

    %% Processing Paths
    DocSearch --> VectorStore
    DocSearch --> OpenAI
    OpenAI --> FileSearch
    FileSearch --> VectorStore

    MetadataQuery --> MetadataCSV
    MetadataQuery --> OpenAI
    OpenAI --> CodeTool
    CodeTool --> MetadataCSV

    HybridAnalysis --> VectorStore
    HybridAnalysis --> ReturnsCSV
    HybridAnalysis --> OpenAI
    OpenAI --> FileSearch
    OpenAI --> CodeTool
    FileSearch --> VectorStore
    CodeTool --> ReturnsCSV

    %% Response Flow
    OpenAI --> Service
    Service --> Routes
    Routes --> API
    API --> Messages
    Messages --> UI

    %% Configuration
    Config --> Service
    Config --> VectorStore
    Config --> ExcelFile
    Config --> MetadataCSV

    %% Styling
    classDef frontend fill:#e1f5fe
    classDef backend fill:#f3e5f5
    classDef ai fill:#fff3e0
    classDef data fill:#e8f5e8
    classDef external fill:#ffebee

    class UI,Input,Messages,Processing,API frontend
    class FastAPI,CORS,Routes,Service,Config backend
    class Classifier,DocSearch,MetadataQuery,HybridAnalysis,CodeInterpreter ai
    class VectorStore,ReturnsCSV,MetadataCSV,ExcelFile data
    class OpenAI,FileSearch,CodeTool external
```

## Information Flow Examples

### Example 1: Document Search Query
**User Question**: "What is the investment strategy of the Point72 fund?"

1. **Frontend**: User types question in ChatWindow
2. **API Call**: POST to `/api/ask` with question
3. **Classification**: Question classified as "DOCUMENT_SEARCH"
4. **Document Search**: 
   - OpenAI API called with file_search tool
   - Vector store searched for relevant PDF documents
   - GPT-4o analyzes document content
5. **Response**: Structured answer with source citations
6. **Display**: MessageList shows formatted response

### Example 2: Financial Calculation Query
**User Question**: "Calculate the Sharpe ratio for Point72 fund"

1. **Frontend**: User submits calculation request
2. **Classification**: Question classified as "CALCULATION_REQUIRED"
3. **Hybrid Analysis**:
   - Document search for context
   - Code interpreter loads Returns.csv data
   - Python code calculates Sharpe ratio using actual returns
   - Visualization generated if needed
4. **Response**: Calculated metric with formula and methodology
5. **Display**: Response with potential charts/images

### Example 3: Metadata Query
**User Question**: "List all hedge funds available"

1. **Frontend**: User asks for fund listing
2. **Classification**: Question classified as "METADATA_QUERY"
3. **Metadata Processing**:
   - Code interpreter loads focus_funds_metadata.csv
   - Filters for Instrument Type = "Hedge Fund"
   - Creates structured table with fund details
4. **Response**: Formatted table with fund names and details
5. **Display**: Markdown-formatted table in chat

## Key Components

### Frontend (Next.js 15)
- **ChatWindow**: Main interface component
- **UserInput**: Text input with send functionality
- **MessageList**: Displays conversation history
- **ProcessingIndicator**: Shows processing stages
- **API Client**: Handles backend communication

### Backend (FastAPI)
- **EnhancedKristalJARVISService**: Core AI service
- **Question Classifier**: Determines processing approach
- **CORS Middleware**: Handles cross-origin requests
- **Configuration Manager**: Manages environment variables

### AI Processing
- **Document Search**: Uses OpenAI file_search tool
- **Metadata Query**: Uses code interpreter with CSV data
- **Hybrid Analysis**: Combines document search + calculations
- **Code Interpreter**: Executes Python code for calculations

### Data Sources
- **Vector Store**: Contains PDF documents (fund factsheets, marketing docs)
- **Returns.csv**: Monthly returns data for all funds
- **Metadata CSV**: Fund metadata (names, types, geographies, strategies)
- **Excel File**: Additional structured data

## Processing Stages

1. **Searching**: Document search and data loading
2. **Calculating**: Code interpreter execution for calculations
3. **Analyzing**: Data analysis and insight generation
4. **Complete**: Final response formatting and delivery

## Error Handling

- **Configuration Errors**: Missing API keys or file IDs
- **API Errors**: OpenAI service failures
- **Data Errors**: Missing or corrupted data files
- **Network Errors**: Connection issues between frontend and backend

## Security Features

- **CORS Configuration**: Restricted to specific domains
- **Input Validation**: Pydantic models for request/response validation
- **Error Sanitization**: Safe error messages without sensitive data
- **Environment Variables**: Secure configuration management
