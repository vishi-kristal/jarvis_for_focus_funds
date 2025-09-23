# Kristal.AI's J.A.R.V.I.S System Flow Chart

## Complete System Flow

```mermaid
flowchart TD
    %% User Interface
    A[User Types Question] --> B[ChatWindow Component]
    B --> C[UserInput Component]
    C --> D[API Client - askQuestion]
    
    %% Backend Processing
    D --> E[FastAPI /api/ask endpoint]
    E --> F[EnhancedKristalJARVISService]
    F --> G[Question Classifier]
    
    %% Classification Decision
    G --> H{Question Type?}
    
    %% Document Search Path
    H -->|DOCUMENT_SEARCH| I[search_documents_only]
    I --> J[OpenAI API with file_search tool]
    J --> K[Vector Store - PDF Documents]
    K --> L[GPT-4o Analysis]
    L --> M[Extract Response Content]
    
    %% Metadata Query Path
    H -->|METADATA_QUERY| N[query_metadata]
    N --> O[Load focus_funds_metadata.csv]
    O --> P[OpenAI API with code_interpreter]
    P --> Q[Python Code Execution]
    Q --> R[Generate Fund List/Table]
    R --> M
    
    %% Hybrid Analysis Path
    H -->|CALCULATION_REQUIRED| S[hybrid_analysis]
    H -->|COMPARISON_REQUIRED| S
    S --> T[Load Returns.csv Data]
    S --> U[OpenAI API with both tools]
    U --> V[file_search + code_interpreter]
    V --> K
    V --> W[Python Calculations]
    W --> X[Generate Charts/Visualizations]
    X --> M
    
    %% Response Processing
    M --> Y[Format Response with Images]
    Y --> Z[Return to Frontend]
    Z --> AA[MessageList Component]
    AA --> BB[Display Response to User]
    
    %% Processing Indicators
    BB --> CC[ProcessingIndicator]
    CC --> DD[Searching Stage]
    CC --> EE[Calculating Stage]
    CC --> FF[Analyzing Stage]
    CC --> GG[Complete Stage]
    
    %% Data Sources
    subgraph "Data Sources"
        K
        O
        T
        HH[Excel File]
    end
    
    %% External Services
    subgraph "External Services"
        J
        P
        U
    end
    
    %% Styling
    classDef userInterface fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    classDef backend fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef ai fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    classDef data fill:#e8f5e8,stroke:#388e3c,stroke-width:2px
    classDef external fill:#ffebee,stroke:#d32f2f,stroke-width:2px
    
    class A,B,C,D,AA,BB,CC,DD,EE,FF,GG userInterface
    class E,F,G,H,I,N,S,M,Y,Z backend
    class J,P,U,V,L,Q,W,X ai
    class K,O,T,HH data
    class J,P,U external
```

## Detailed Information Flow Examples

### Example 1: Document Search Flow
```mermaid
sequenceDiagram
    participant U as User
    participant CW as ChatWindow
    participant API as API Client
    participant BE as Backend
    participant AI as OpenAI API
    participant VS as Vector Store
    
    U->>CW: "What is Point72's strategy?"
    CW->>API: askQuestion(question)
    API->>BE: POST /api/ask
    BE->>BE: classify_question() → DOCUMENT_SEARCH
    BE->>AI: responses.create() with file_search
    AI->>VS: Search PDF documents
    VS-->>AI: Relevant document chunks
    AI-->>BE: Structured response
    BE-->>API: {answer, images}
    API-->>CW: Response data
    CW-->>U: Display formatted answer
```

### Example 2: Financial Calculation Flow
```mermaid
sequenceDiagram
    participant U as User
    participant CW as ChatWindow
    participant API as API Client
    participant BE as Backend
    participant AI as OpenAI API
    participant CSV as Returns.csv
    participant CI as Code Interpreter
    
    U->>CW: "Calculate Sharpe ratio for Point72"
    CW->>API: askQuestion(question)
    API->>BE: POST /api/ask
    BE->>BE: classify_question() → CALCULATION_REQUIRED
    BE->>AI: responses.create() with both tools
    AI->>CI: Execute Python code
    CI->>CSV: Load monthly returns data
    CSV-->>CI: Returns data
    CI->>CI: Calculate Sharpe ratio
    CI-->>AI: Calculated metrics + charts
    AI-->>BE: Response with calculations
    BE-->>API: {answer, images}
    API-->>CW: Response with charts
    CW-->>U: Display calculated results
```

### Example 3: Metadata Query Flow
```mermaid
sequenceDiagram
    participant U as User
    participant CW as ChatWindow
    participant API as API Client
    participant BE as Backend
    participant AI as OpenAI API
    participant MD as Metadata CSV
    participant CI as Code Interpreter
    
    U->>CW: "List all hedge funds"
    CW->>API: askQuestion(question)
    API->>BE: POST /api/ask
    BE->>BE: classify_question() → METADATA_QUERY
    BE->>AI: responses.create() with code_interpreter
    AI->>CI: Execute Python code
    CI->>MD: Load fund metadata
    MD-->>CI: Fund data
    CI->>CI: Filter hedge funds
    CI->>CI: Create formatted table
    CI-->>AI: Structured fund list
    AI-->>BE: Response with table
    BE-->>API: {answer, images}
    API-->>CW: Response with table
    CW-->>U: Display fund list
```

## Key Processing Stages

```mermaid
stateDiagram-v2
    [*] --> UserInput
    UserInput --> QuestionClassification
    QuestionClassification --> DocumentSearch : DOCUMENT_SEARCH
    QuestionClassification --> MetadataQuery : METADATA_QUERY
    QuestionClassification --> HybridAnalysis : CALCULATION_REQUIRED
    QuestionClassification --> HybridAnalysis : COMPARISON_REQUIRED
    
    DocumentSearch --> Searching
    MetadataQuery --> Searching
    HybridAnalysis --> Searching
    
    Searching --> Calculating : If calculations needed
    Searching --> Analyzing : If no calculations
    
    Calculating --> Analyzing
    Analyzing --> Complete
    Complete --> ResponseDisplay
    ResponseDisplay --> [*]
    
    note right of Searching : Load data sources
    note right of Calculating : Execute Python code
    note right of Analyzing : Generate insights
    note right of Complete : Format response
```

## Data Flow Architecture

```mermaid
graph LR
    subgraph "Frontend (Next.js)"
        A[User Input] --> B[Chat Interface]
        B --> C[API Calls]
    end
    
    subgraph "Backend (FastAPI)"
        C --> D[API Endpoints]
        D --> E[Service Layer]
        E --> F[Question Router]
    end
    
    subgraph "AI Processing"
        F --> G[Document Search]
        F --> H[Metadata Query]
        F --> I[Hybrid Analysis]
    end
    
    subgraph "Data Layer"
        J[PDF Documents] --> K[Vector Store]
        L[Returns Data] --> M[CSV Files]
        N[Fund Metadata] --> O[Metadata CSV]
    end
    
    subgraph "External AI"
        P[OpenAI API] --> Q[GPT-4o Model]
        Q --> R[File Search Tool]
        Q --> S[Code Interpreter]
    end
    
    G --> K
    G --> R
    H --> O
    H --> S
    I --> K
    I --> M
    I --> R
    I --> S
    
    R --> P
    S --> P
    
    P --> E
    E --> D
    D --> C
    C --> B
    B --> A
```
