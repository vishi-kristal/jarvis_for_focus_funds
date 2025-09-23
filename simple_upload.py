#!/usr/bin/env python3
"""
Minimal script to upload metadata CSV using requests directly.
"""

import requests
import os
from pathlib import Path

def upload_metadata_csv():
    """Upload metadata CSV using direct API call."""
    
    # API key - use environment variable
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OPENAI_API_KEY environment variable not set")
        return None
    
    # File path
    file_path = Path("metadata/focus_funds_metadata.csv")
    if not file_path.exists():
        print(f"❌ File not found: {file_path}")
        return None
    
    print(f"📁 Uploading: {file_path}")
    
    # Prepare the request
    url = "https://api.openai.com/v1/files"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    # Upload file
    with open(file_path, "rb") as f:
        files = {
            "file": (file_path.name, f, "text/csv")
        }
        data = {
            "purpose": "assistants"
        }
        
        try:
            response = requests.post(url, headers=headers, files=files, data=data)
            response.raise_for_status()
            
            result = response.json()
            file_id = result["id"]
            
            print(f"✅ Upload successful!")
            print(f"📄 File ID: {file_id}")
            print(f"📊 File name: {result.get('filename', 'unknown')}")
            print(f"📏 File size: {result.get('bytes', 0)} bytes")
            
            return file_id
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Upload failed: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")
            return None

if __name__ == "__main__":
    print("🧪 Uploading metadata CSV using direct API...")
    file_id = upload_metadata_csv()
    if file_id:
        print(f"\n🎉 Success! Add this to your .env file:")
        print(f"METADATA_FILE_ID={file_id}")
    else:
        print("\n❌ Upload failed.")
