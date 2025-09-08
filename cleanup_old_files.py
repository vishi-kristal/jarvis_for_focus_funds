#!/usr/bin/env python3
"""
Script to clean up old duplicate files from OpenAI.
WARNING: This will delete files permanently!
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def cleanup_old_files():
    """Remove old duplicate files, keeping only the latest ones."""
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    print("🧹 Cleaning up old duplicate files...")
    print("⚠️  WARNING: This will permanently delete files!")
    
    # Get current vector store ID
    with open('.env', 'r') as f:
        content = f.read()
        current_vs_id = None
        for line in content.split('\n'):
            if 'VECTOR_STORE_ID' in line and line.strip():
                current_vs_id = line.split('=')[1]
                break
    
    if not current_vs_id:
        print("❌ No vector store ID found")
        return
    
    # Get files in current vector store (these we want to keep)
    current_files = set()
    try:
        vs_files = client.vector_stores.files.list(vector_store_id=current_vs_id)
        for file in vs_files.data:
            current_files.add(file.id)
        print(f"✅ Found {len(current_files)} files in current vector store")
    except Exception as e:
        print(f"❌ Error getting current vector store files: {e}")
        return
    
    # Get all files
    try:
        all_files = client.files.list()
        files_to_delete = []
        
        for file in all_files.data:
            if file.id not in current_files:
                files_to_delete.append(file)
        
        print(f"📋 Found {len(files_to_delete)} old files to delete")
        
        if not files_to_delete:
            print("✅ No old files to clean up")
            return
        
        # Show files that will be deleted
        print("\nFiles to be deleted:")
        for file in files_to_delete:
            print(f"  - {file.filename} ({file.id})")
        
        # Ask for confirmation
        confirm = input("\n❓ Do you want to proceed with deletion? (yes/no): ")
        if confirm.lower() != 'yes':
            print("❌ Deletion cancelled")
            return
        
        # Delete files
        deleted_count = 0
        for file in files_to_delete:
            try:
                client.files.delete(file.id)
                print(f"✅ Deleted: {file.filename}")
                deleted_count += 1
            except Exception as e:
                print(f"❌ Error deleting {file.filename}: {e}")
        
        print(f"\n🎉 Cleanup complete! Deleted {deleted_count} files")
        
    except Exception as e:
        print(f"❌ Error during cleanup: {e}")

if __name__ == "__main__":
    cleanup_old_files()
