#!/bin/bash

# Script to prepare code for safe manual upload
echo "🔒 Preparing code for safe manual upload..."

# Create a temporary directory for the clean version
CLEAN_DIR="../FundSight_Clean"
rm -rf "$CLEAN_DIR"
mkdir -p "$CLEAN_DIR"

echo "📁 Copying files to clean directory..."

# Copy all files except sensitive ones
rsync -av --exclude='.env' \
          --exclude='.env.local' \
          --exclude='frontend/.env.local' \
          --exclude='frontend/frontend_backup/.env.local' \
          --exclude='__pycache__' \
          --exclude='*.pyc' \
          --exclude='.git' \
          --exclude='node_modules' \
          --exclude='frontend/.next' \
          --exclude='frontend/out' \
          --exclude='.DS_Store' \
          --exclude='*.log' \
          . "$CLEAN_DIR/"

echo "✅ Clean version created in: $CLEAN_DIR"
echo ""
echo "📋 Files to manually upload:"
echo "1. Go to https://github.com/Elnino0009/FundSight"
echo "2. Click 'uploading an existing file' or drag and drop"
echo "3. Upload all files from the $CLEAN_DIR directory"
echo ""
echo "⚠️  IMPORTANT: Do NOT upload these sensitive files:"
echo "   - .env (contains your OpenAI API key)"
echo "   - .env.local (contains local configuration)"
echo "   - Any files with 'backup' in the name"
echo ""
echo "🔑 After upload, you'll need to set these environment variables:"
echo "   - OPENAI_API_KEY=your_actual_api_key"
echo "   - VECTOR_STORE_ID=will_be_set_by_setup.py"
echo "   - EXCEL_FILE_ID=will_be_set_by_setup.py"
