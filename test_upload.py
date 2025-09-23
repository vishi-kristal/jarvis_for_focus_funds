#!/usr/bin/env python3
"""
Simple test script to upload the metadata CSV file.
"""

import os
from openai import OpenAI
from pathlib import Path

# API key should be set via environment variable
# Check if API key is available
if not os.getenv('OPENAI_API_KEY'):
    print("❌ OPENAI_API_KEY environment variable not set")
    print("Please set your OpenAI API key in the environment or .env file")
    exit(1)

def test_upload():
    """Test uploading the metadata CSV file."""
    client = OpenAI()
    
    # Check if metadata file exists
    metadata_path = Path("metadata/focus_funds_metadata.csv")
    if not metadata_path.exists():
        print(f"❌ Metadata file not found: {metadata_path}")
        return None
    
    print(f"📁 Found metadata file: {metadata_path}")
    
    try:
        # Upload the file
        with open(metadata_path, "rb") as f:
            file_response = client.files.create(
                file=f,
                purpose="assistants"
            )
        
        print(f"✅ File uploaded successfully!")
        print(f"📄 File ID: {file_response.id}")
        print(f"📊 File name: {file_response.filename}")
        print(f"📏 File size: {file_response.bytes} bytes")
        
        return file_response.id
        
    except Exception as e:
        print(f"❌ Upload failed: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        return None

if __name__ == "__main__":
    print("🧪 Testing metadata CSV file upload...")
    file_id = test_upload()
    if file_id:
        print(f"\n🎉 Success! Metadata file ID: {file_id}")
        print("Add this to your .env file as METADATA_FILE_ID")
    else:
        print("\n❌ Upload failed. Check the error above.")
