# Kristal.AI's J.A.R.V.I.S Frontend

A modern, responsive Next.js frontend for Kristal.AI's J.A.R.V.I.S application that provides an intuitive chat interface for querying investment fund documents using AI.

## Features

- **Modern Chat Interface**: Clean, professional chat UI with real-time messaging
- **Sample Questions**: Pre-built questions to help users get started
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Error Handling**: Comprehensive error handling with user-friendly messages
- **Loading States**: Visual feedback during AI processing
- **Markdown Support**: Rich text formatting for AI responses
- **TypeScript**: Full type safety throughout the application

## Technology Stack

- **Framework**: Next.js 15 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **State Management**: React hooks (useState, useCallback)
- **API Integration**: Fetch API with custom error handling

## Project Structure

```
frontend/
├── src/
│   ├── app/
│   │   ├── page.tsx              # Main page component
│   │   └── layout.tsx            # Root layout
│   ├── components/
│   │   ├── ChatWindow.tsx        # Main chat interface
│   │   ├── MessageList.tsx       # Message display component
│   │   ├── MessageBubble.tsx     # Individual message component
│   │   ├── UserInput.tsx         # Message input component
│   │   ├── SampleQuestions.tsx   # Sample questions component
│   │   └── LoadingIndicator.tsx  # Loading state component
│   ├── lib/
│   │   ├── api.ts                # API integration functions
│   │   └── utils.ts              # Utility functions
│   ├── types/
│   │   └── index.ts              # TypeScript type definitions
│   └── data/
│       └── sample-questions.ts   # Sample questions data
├── .env.local                    # Environment variables
├── package.json                  # Dependencies and scripts
└── README.md                     # This file
```

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn
- Backend server running on http://localhost:8000

### Installation

1. **Navigate to the frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Set up environment variables**:
   ```bash
   cp env.local.example .env.local
   ```
   
   Edit `.env.local` and ensure the backend URL is correct:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

4. **Start the development server**:
   ```bash
   npm run dev
   ```

5. **Open your browser**:
   Navigate to [http://localhost:3000](http://localhost:3000)

## Usage

### Basic Usage

1. **Start the Application**: Open http://localhost:3000 in your browser
2. **Choose a Sample Question**: Click on any of the pre-built questions to get started
3. **Ask Custom Questions**: Type your own questions in the input field
4. **View Responses**: AI responses are displayed with proper formatting and citations

### Sample Questions

The application includes categorized sample questions:

- **Discovery**: "What funds are available in the system?"
- **Strategy**: "What is the investment strategy of the Peregrine Fund?"
- **Risk**: "What is the GBAF fund's approach to risk management?"
- **Comparison**: "Compare the investment strategies of both funds"
- **Performance**: "What are the key performance metrics mentioned in the fund documents?"
- **Assets**: "What types of assets does the GBAF fund invest in?"
- **Liquidity**: "What are the liquidity characteristics of both funds?"
- **Compliance**: "What regulatory considerations are mentioned for these funds?"

### Features

#### Chat Interface
- **Real-time Messaging**: Send and receive messages instantly
- **Message History**: View complete conversation history
- **Typing Indicators**: Visual feedback when AI is processing
- **Auto-resize Input**: Input field automatically adjusts to content

#### Error Handling
- **Connection Errors**: Clear messages when backend is unavailable
- **API Errors**: User-friendly error messages with retry options
- **Network Issues**: Graceful handling of network problems

#### Responsive Design
- **Mobile-First**: Optimized for mobile devices
- **Desktop Support**: Full functionality on desktop browsers
- **Flexible Layout**: Adapts to different screen sizes

## API Integration

The frontend communicates with the backend through a REST API:

### Endpoints

- **Health Check**: `GET /health`
- **Ask Question**: `POST /api/ask`

### Request Format

```typescript
// Ask Question Request
{
  "question": "What funds are available in the system?"
}
```

### Response Format

```typescript
// Success Response
{
  "answer": "The available funds in the system are..."
}

// Error Response
{
  "error": "Error message",
  "detail": "Additional error details"
}
```

## Development

### Available Scripts

- `npm run dev`: Start development server
- `npm run build`: Build for production
- `npm run start`: Start production server
- `npm run lint`: Run ESLint

### Code Structure

#### Components

- **ChatWindow**: Main container component that manages the entire chat interface
- **MessageList**: Displays the conversation history
- **MessageBubble**: Individual message component with user/assistant styling
- **UserInput**: Input form with auto-resize and keyboard shortcuts
- **SampleQuestions**: Grid of categorized sample questions
- **LoadingIndicator**: Loading state with spinner

#### State Management

The application uses React hooks for state management:

- **Messages**: Array of conversation messages
- **Loading State**: Boolean for AI processing status
- **Error State**: String for error messages

#### API Layer

The `api.ts` file provides:

- **askQuestion()**: Send questions to the backend
- **checkHealth()**: Verify backend connectivity
- **ApiError**: Custom error class for API errors

### Styling

The application uses Tailwind CSS for styling:

- **Utility Classes**: Consistent spacing, colors, and typography
- **Responsive Design**: Mobile-first approach with breakpoints
- **Component Styling**: Scoped styles for each component
- **Dark Mode Ready**: Prepared for dark mode implementation

## Deployment

### Production Build

1. **Build the application**:
   ```bash
   npm run build
   ```

2. **Start production server**:
   ```bash
   npm run start
   ```

### Environment Variables

For production deployment, set:

```bash
NEXT_PUBLIC_API_URL=https://your-backend-domain.com
```

### Deployment Platforms

The application can be deployed to:

- **Vercel**: Recommended for Next.js applications
- **Netlify**: Static site deployment
- **AWS Amplify**: Full-stack deployment
- **Docker**: Containerized deployment

## Troubleshooting

### Common Issues

1. **Backend Connection Error**:
   - Ensure backend server is running on http://localhost:8000
   - Check CORS configuration in backend
   - Verify environment variables

2. **Build Errors**:
   - Clear `.next` directory: `rm -rf .next`
   - Reinstall dependencies: `rm -rf node_modules && npm install`
   - Check TypeScript errors: `npm run lint`

3. **Styling Issues**:
   - Ensure Tailwind CSS is properly configured
   - Check for conflicting CSS classes
   - Verify responsive breakpoints

### Debug Mode

Enable debug logging by adding to `.env.local`:

```bash
NEXT_PUBLIC_DEBUG=true
```

## Contributing

1. Follow TypeScript best practices
2. Use meaningful component and variable names
3. Add proper error handling
4. Ensure responsive design
5. Test on multiple devices and browsers

## License

This project is part of the GenAI FundScreener application.