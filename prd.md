Of course. Here is a comprehensive requirements document tailored for building your application in Cursor. This document outlines the full scope, from backend architecture to frontend components, providing a clear roadmap for development.

***

# **Project Requirements: GenAI FundScreener Application**

## **1. Project Overview**

### **1.1. Vision**
To create an intelligent, AI-powered web application that allows financial analysts to get instant, accurate answers to complex questions about a portfolio of investment funds. The system will leverage a Retrieval-Augmented Generation (RAG) model, using OpenAI's Responses API to query a private knowledge base of 100+ fund documents.

### **1.2. Core Problem**
Financial analysts spend a significant amount of time manually searching through hundreds of PDF documents (factsheets, marketing decks, reports) to find specific data points, compare funds, and synthesize information for client meetings. This process is slow, inefficient, and prone to error.

### **1.3. Solution**
This application will provide a simple, chat-like interface where users can ask questions in natural language and receive AI-generated answers grounded in the provided fund documents. The system will handle complex queries, including data extraction from tables, multi-document comparison, metadata-based filtering, and content summarization.

### **1.4. Technology Stack**
*   **Frontend:** Next.js
*   **Backend:** Python
*   **API Framework:** FastAPI
*   **AI Engine:** OpenAI Responses API (including File Search and Vector Stores)
*   **Deployment:** To be determined (initial version will run locally)

## **2. Backend Requirements (Python & FastAPI)**

### **2.1. Environment & Configuration**
*   The backend must load environment variables (specifically the `OPENAI_API_KEY`) securely from a `.env` file.
*   It must manage and store persistent configuration data, including the `ASSISTANT_ID` and `VECTOR_STORE_ID`, in a simple configuration file (e.g., `config.txt` or `config.ini`).

### **2.2. One-Time Setup Module (`setup.py`)**
This script will be a command-line utility to initialize the entire AI knowledge base. It is not part of the runtime API.

*   **File Ingestion:**
    *   The script must be ableto scan a local `documents/` directory for all PDF files.
    *   It must be able to scan a local `metadata/` directory for all JSON files.
    *   It must upload every PDF and JSON file to OpenAI's file storage using the OpenAI Python client.
    *   The script must log the `file_id` of each successfully uploaded document.
*   **Vector Store Creation:**
    *   After uploading all files, the script must create a single, persistent **Vector Store**.
    *   This Vector Store should be populated with all the `file_id`s from the uploaded documents.
*   **Assistant Creation:**
    *   The script must create a single, persistent **Assistant**.
    *   The Assistant's configuration must include:
        *   A descriptive name (e.g., "Fund Analysis Expert").
        *   A powerful LLM (e.g., `gpt-4o`).
        *   A detailed system prompt outlining its persona, capabilities, and rules for answering questions (as detailed in the previous guide).
        *   The `file_search` tool must be enabled.
        *   The `file_search` tool must be explicitly linked to the `VECTOR_STORE_ID` created in the previous step.
*   **Configuration Output:**
    *   The script must save the resulting `ASSISTANT_ID` and `VECTOR_STORE_ID` to the configuration file for the runtime API to use.

### **2.3. Runtime API (FastAPI)**
The FastAPI application will expose endpoints for the Next.js frontend to interact with the AI assistant.

*   **Endpoint: `POST /api/ask`**
    *   **Request Body:** The endpoint will accept a JSON payload containing a single field: `question` (string).
    *   **Core Logic:**
        1.  On receiving a request, the backend will create a new, temporary **Thread** with the OpenAI API. Threads isolate each user query session.
        2.  It will add the user's `question` as a new **Message** to this thread.
        3.  It will then create and poll a **Run**, passing the `thread_id` and the pre-configured `ASSISTANT_ID`. This triggers the entire RAG process on OpenAI's side.
        4.  The polling must handle the run's status (`queued`, `in_progress`, `completed`).
    *   **Response Body:**
        1.  Once the run is complete, the backend will retrieve the latest messages from the thread.
        2.  It will extract the text content from the Assistant's final response.
        3.  It will return a JSON object with a single field: `answer` (string).
*   **CORS Configuration:**
    *   The FastAPI app must be configured with Cross-Origin Resource Sharing (CORS) to allow requests from the Next.js frontend's development server (e.g., `http://localhost:3000`).

## **3. Frontend Requirements (Next.js)**

### **3.1. Main Chat Interface**
The primary UI will be a single-page chat interface.

*   **Layout:**
    *   A central content area to display the conversation history.
    *   A text input area at the bottom for the user to type their question.
    *   A "Send" button to submit the query.
*   **State Management:**
    *   The frontend must manage the state of the conversation, including the history of questions and answers.
    *   It must manage a "loading" state to provide user feedback while the backend is processing a request.
*   **API Interaction:**
    *   Submitting a question will trigger an asynchronous `POST` request to the backend's `/api/ask` endpoint.
    *   While waiting for the response, the UI should display a loading indicator (e.g., a spinner or a "Thinking..." message).
    *   On receiving a successful response, the UI will display the AI-generated answer.
    *   The UI must handle and display potential API errors gracefully.

### **3.2. UI Components**
*   **`ChatWindow`:** The main component that holds the `MessageList` and `UserInput` components.
*   **`MessageList`:** Renders the list of questions and answers. User messages and AI responses should be visually distinct (e.g., different background colors or alignment).
*   **`UserInput`:** A form containing a `<textarea>` for multi-line questions and a submit button. The textarea should resize dynamically with content.
*   **`MessageBubble`:** A component that displays a single message (either from the user or the AI). It should be ableto render Markdown for formatted responses from the AI (e.g., tables, bold text, lists).
*   **`LoadingIndicator`:** A component to be displayed while the API call is in progress.
*   **`SampleQuestions`:** A section on the initial screen that provides users with example prompts to guide them on how to use the application effectively.

### **3.3. Styling**
*   The application should have a clean, professional, and modern design.
*   Use a responsive layout that works well on standard desktop screen sizes.
*   The text in the answer bubbles must be formatted to correctly display pre-formatted text, including spaces and line breaks, and render Markdown tables correctly.

## **4. User Experience (UX) Flow**

1.  **Initial View:** The user sees the main chat interface, an empty message list, and a list of sample questions to get started.
2.  **Asking a Question:** The user types a question into the input box and clicks "Send."
3.  **Loading State:** The user's question appears in the chat window. The input box is disabled, and a loading indicator appears below the question to show the system is working.
4.  **Receiving an Answer:** The loading indicator is replaced by the AI's answer, which is displayed in a new message bubble. The input box is re-enabled.
5.  **Follow-up Questions:** The user can ask follow-up questions in the same interface, continuing the conversation. The context is managed by the backend thread.
