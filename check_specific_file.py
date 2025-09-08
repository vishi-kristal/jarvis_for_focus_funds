#!/usr/bin/env python3
"""
Script to check a specific file in OpenAI.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def check_file_details(file_id: str):
    """Check details of a specific file."""
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    try:
        file = client.files.retrieve(file_id)
        print(f"📄 File: {file.filename}")
        print(f"   ID: {file.id}")
        print(f"   Size: {file.bytes} bytes")
        print(f"   Purpose: {file.purpose}")
        print(f"   Status: {file.status}")
        print(f"   Created: {file.created_at}")
        
        # Check if file is in any vector stores
        vector_stores = client.vector_stores.list()
        for vs in vector_stores.data:
            try:
                vs_files = client.vector_stores.files.list(vector_store_id=vs.id)
                for vs_file in vs_files.data:
                    if vs_file.id == file_id:
                        print(f"   ✅ In Vector Store: {vs.name} ({vs.id})")
                        return
            except:
                continue
        
        print("   ❌ Not in any vector store")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Check one of your current files
    check_file_details("file-5TeL4jgCTBBahDk5urVGh3")  # GBAF factsheet
