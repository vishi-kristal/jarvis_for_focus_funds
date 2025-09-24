#!/usr/bin/env python3
"""
One-time setup script for Kristal.AI's J.A.R.V.I.S application.
This script initializes the AI knowledge base using OpenAI's Responses API.
"""

import os
import json
import logging
from pathlib import Path
from typing import List, Dict, Any
from openai import OpenAI
from config import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class KristalJARVISSetup:
    """Handles the one-time setup of the AI knowledge base using Responses API."""
    
    def __init__(self):
        self.client = OpenAI(api_key=config.openai_api_key)
        self.documents_dir = Path("documents")
        self.uploaded_files: List[Dict[str, str]] = []
    
    def ensure_directories(self) -> None:
        """Ensure required directories exist."""
        self.documents_dir.mkdir(exist_ok=True)
        logger.info(f"Ensured documents directory exists: {self.documents_dir}")
    
    def upload_files(self) -> None:
        """Upload all PDF files to OpenAI's file storage."""
        logger.info("Starting PDF file upload process...")
        
        # Upload PDF files from documents directory
        pdf_files = list(self.documents_dir.glob("*.pdf"))
        logger.info(f"Found {len(pdf_files)} PDF files to upload")
        
        for pdf_file in pdf_files:
            try:
                with open(pdf_file, "rb") as f:
                    file_response = self.client.files.create(
                        file=f,
                        purpose="assistants"
                    )
                
                self.uploaded_files.append({
                    "file_id": file_response.id,
                    "filename": pdf_file.name,
                    "type": "pdf"
                })
                logger.info(f"✅ Uploaded PDF: {pdf_file.name} -> {file_response.id}")
                
            except Exception as e:
                logger.error(f"❌ Failed to upload PDF {pdf_file.name}: {str(e)}")
        
        logger.info(f"PDF file upload completed. Total files uploaded: {len(self.uploaded_files)}")
    
    
    def create_vector_store(self) -> str:
        """Create a vector store for the Responses API file search."""
        logger.info("Creating vector store for Responses API...")
        
        if not self.uploaded_files:
            raise ValueError("No PDF files uploaded. Cannot create vector store.")
        
        # Create vector store with PDF files only
        file_ids = [file_info["file_id"] for file_info in self.uploaded_files if file_info.get("type") == "pdf"]
        
        if not file_ids:
            raise ValueError("No PDF files available for vector store.")
        
        vector_store = self.client.vector_stores.create(
            name="Fund Documents Vector Store",
            file_ids=file_ids
        )
        
        logger.info(f"✅ Created vector store with {len(file_ids)} PDF files: {vector_store.id}")
        return vector_store.id
    
    def create_file_search_config(self, vector_store_id: str) -> Dict[str, Any]:
        """Create file search configuration for the Responses API."""
        logger.info("Creating file search configuration...")
        
        if not self.uploaded_files:
            raise ValueError("No files uploaded. Cannot create file search configuration.")
        
        file_ids = [file_info["file_id"] for file_info in self.uploaded_files]
        
        logger.info(f"File search configuration created with {len(file_ids)} files and vector store {vector_store_id}")
        return {
            "file_ids": file_ids,
            "uploaded_files": self.uploaded_files,
            "vector_store_id": vector_store_id
        }
    
    def save_configuration(self, file_config: Dict[str, Any]) -> None:
        """Save the configuration to the .env file."""
        logger.info("Saving configuration...")
        
        # Save the vector store ID for Responses API
        vector_store_id = file_config.get("vector_store_id", "")
        config.save_config("", vector_store_id, "", "")  # Empty assistant_id, excel_file_id, and metadata_file_id
        logger.info("✅ Configuration saved successfully")
    
    def run_setup(self) -> None:
        """Run the complete setup process."""
        try:
            logger.info("🚀 Starting Kristal.AI's J.A.R.V.I.S setup for document search...")
            
            # Step 1: Ensure directories exist
            self.ensure_directories()
            
            # Step 2: Upload PDF files
            self.upload_files()
            
            if not self.uploaded_files:
                logger.warning("❌ No PDF files found to upload. Please add PDF files to 'documents/' directory.")
                return
            
            # Step 3: Create vector store
            vector_store_id = self.create_vector_store()
            
            # Step 4: Create file search configuration
            file_config = self.create_file_search_config(vector_store_id)
            
            # Step 5: Save configuration
            self.save_configuration(file_config)
            
            logger.info("✅ Setup completed successfully!")
            logger.info(f"📁 Vector Store ID: {vector_store_id}")
            logger.info("🚀 You can now run the main application!")
            
        except Exception as e:
            logger.error(f"❌ Setup failed: {str(e)}")
            raise

def main():
    """Main entry point for the setup script."""
    setup = KristalJARVISSetup()
    setup.run_setup()

if __name__ == "__main__":
    main()
