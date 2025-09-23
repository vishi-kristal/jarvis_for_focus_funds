#!/bin/bash

# J.A.R.V.I.S Local Development Setup Script
# This script helps you run the application locally without cloud deployment

echo "🚀 Starting J.A.R.V.I.S Local Development Environment"
echo "=================================================="

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ Error: .env file not found!"
    echo "Please copy env.example to .env and add your OpenAI API key"
    exit 1
fi

# Check if OpenAI API key is set
if ! grep -q "OPENAI_API_KEY=sk-" .env; then
    echo "⚠️  Warning: OpenAI API key not found in .env file"
    echo "Please add your OpenAI API key to the .env file"
    echo "Example: OPENAI_API_KEY=sk-your-key-here"
    echo ""
fi

echo "📋 Available Commands:"
echo "1. Start Backend Only"
echo "2. Start Frontend Only" 
echo "3. Start Both (Backend + Frontend)"
echo "4. Setup AI Knowledge Base (One-time)"
echo "5. Test Backend Health"
echo "6. Exit"
echo ""

read -p "Choose an option (1-6): " choice

case $choice in
    1)
        echo "🔧 Starting Backend Server..."
        echo "Backend will be available at: http://localhost:8000"
        echo "API Documentation: http://localhost:8000/docs"
        echo "Press Ctrl+C to stop the server"
        echo ""
        python3 main.py
        ;;
    2)
        echo "🎨 Starting Frontend Server..."
        echo "Frontend will be available at: http://localhost:3000"
        echo "Press Ctrl+C to stop the server"
        echo ""
        cd frontend && npm run dev
        ;;
    3)
        echo "🚀 Starting Both Backend and Frontend..."
        echo ""
        echo "Backend: http://localhost:8000"
        echo "Frontend: http://localhost:3000"
        echo "API Docs: http://localhost:8000/docs"
        echo ""
        echo "Starting Backend in background..."
        python3 main.py &
        BACKEND_PID=$!
        
        echo "Starting Frontend..."
        cd frontend && npm run dev &
        FRONTEND_PID=$!
        
        echo ""
        echo "✅ Both servers are running!"
        echo "Backend PID: $BACKEND_PID"
        echo "Frontend PID: $FRONTEND_PID"
        echo ""
        echo "Press Ctrl+C to stop both servers"
        
        # Wait for user to stop
        wait
        ;;
    4)
        echo "🤖 Setting up AI Knowledge Base..."
        echo "This will upload documents and create the AI assistant"
        echo "This is a one-time setup process"
        echo ""
        read -p "Continue? (y/n): " confirm
        if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
            python3 setup.py
        else
            echo "Setup cancelled"
        fi
        ;;
    5)
        echo "🔍 Testing Backend Health..."
        echo "Starting backend for testing..."
        python3 main.py &
        BACKEND_PID=$!
        
        # Wait a moment for server to start
        sleep 3
        
        echo "Testing health endpoint..."
        curl -s http://localhost:8000/health | python3 -m json.tool
        
        echo ""
        echo "Stopping test server..."
        kill $BACKEND_PID
        ;;
    6)
        echo "👋 Goodbye!"
        exit 0
        ;;
    *)
        echo "❌ Invalid option. Please choose 1-6"
        exit 1
        ;;
esac
