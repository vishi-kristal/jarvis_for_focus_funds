#!/usr/bin/env python3
"""
Script to check documents and vector stores in OpenAI.
This will show you what files are uploaded and which vector store they belong to.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_documents():
    """Check uploaded documents and vector stores."""
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    print("🔍 Checking OpenAI Documents and Vector Stores")
    print("=" * 60)
    
    # Check uploaded files
    print("\n📁 UPLOADED FILES:")
    print("-" * 30)
    
    try:
        files = client.files.list()
        if files.data:
            for file in files.data:
                print(f"📄 {file.filename}")
                print(f"   ID: {file.id}")
                print(f"   Purpose: {file.purpose}")
                print(f"   Size: {file.bytes} bytes")
                print(f"   Created: {file.created_at}")
                print()
        else:
            print("No files found.")
    except Exception as e:
        print(f"Error fetching files: {e}")
    
    # Check vector stores
    print("\n🗂️  VECTOR STORES:")
    print("-" * 30)
    
    try:
        vector_stores = client.vector_stores.list()
        if vector_stores.data:
            for vs in vector_stores.data:
                print(f"📊 Vector Store: {vs.name}")
                print(f"   ID: {vs.id}")
                print(f"   Status: {vs.status}")
                print(f"   File Count: {vs.file_counts.total}")
                print(f"   Created: {vs.created_at}")
                
                # Get files in this vector store
                try:
                    vs_files = client.vector_stores.files.list(vector_store_id=vs.id)
                    if vs_files.data:
                        print("   Files in this vector store:")
                        for file in vs_files.data:
                            print(f"     - {file.id} (Status: {file.status})")
                    else:
                        print("   No files in this vector store.")
                except Exception as e:
                    print(f"   Error fetching files: {e}")
                print()
        else:
            print("No vector stores found.")
    except Exception as e:
        print(f"Error fetching vector stores: {e}")
    
    # Check your current configuration
    print("\n⚙️  CURRENT CONFIGURATION:")
    print("-" * 30)
    
    try:
        with open('.env', 'r') as f:
            content = f.read()
            for line in content.split('\n'):
                if 'VECTOR_STORE_ID' in line and line.strip():
                    print(f"Vector Store ID: {line.split('=')[1]}")
                    break
    except Exception as e:
        print(f"Error reading .env file: {e}")

def test_vector_store_search():
    """Test if the vector store is working by doing a simple search."""
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    print("\n🧪 TESTING VECTOR STORE SEARCH:")
    print("-" * 30)
    
    try:
        # Read vector store ID from .env
        with open('.env', 'r') as f:
            content = f.read()
            vector_store_id = None
            for line in content.split('\n'):
                if 'VECTOR_STORE_ID' in line and line.strip():
                    vector_store_id = line.split('=')[1]
                    break
        
        if not vector_store_id:
            print("❌ No vector store ID found in .env file")
            return
        
        print(f"Using Vector Store ID: {vector_store_id}")
        
        # Test with a simple question
        response = client.responses.create(
            model='gpt-4o',
            input='What funds are available in the system?',
            instructions='You are a fund analysis expert. Use file search to find information about available funds.',
            tools=[{'type': 'file_search', 'vector_store_ids': [vector_store_id]}],
            max_tool_calls=3
        )
        
        if response.output and len(response.output) > 0:
            # Find the message with content
            for item in response.output:
                if hasattr(item, 'content') and item.content:
                    print("✅ Vector store search is working!")
                    print(f"Response: {item.content[0].text[:200]}...")
                    return
        
        print("❌ No response received from vector store search")
        
    except Exception as e:
        print(f"❌ Error testing vector store: {e}")

if __name__ == "__main__":
    check_documents()
    test_vector_store_search()
