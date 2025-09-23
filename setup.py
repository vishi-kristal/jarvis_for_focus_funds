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
import pandas as pd
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
        self.metadata_dir = Path("metadata")
        self.returns_dir = Path("Returns")
        self.uploaded_files: List[Dict[str, str]] = []
        self.excel_file_id = None
    
    def ensure_directories(self) -> None:
        """Ensure required directories exist."""
        self.documents_dir.mkdir(exist_ok=True)
        self.metadata_dir.mkdir(exist_ok=True)
        self.returns_dir.mkdir(exist_ok=True)
        logger.info(f"Ensured directories exist: {self.documents_dir}, {self.metadata_dir}, {self.returns_dir}")
    
    def upload_files(self) -> None:
        """Upload all PDF and JSON files to OpenAI's file storage."""
        logger.info("Starting file upload process...")
        
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
                logger.info(f"Uploaded PDF: {pdf_file.name} -> {file_response.id}")
                
            except Exception as e:
                logger.error(f"Failed to upload {pdf_file.name}: {str(e)}")
        
        # Upload JSON files from metadata directory
        json_files = list(self.metadata_dir.glob("*.json"))
        logger.info(f"Found {len(json_files)} JSON files to upload")
        
        for json_file in json_files:
            try:
                with open(json_file, "rb") as f:
                    file_response = self.client.files.create(
                        file=f,
                        purpose="assistants"
                    )
                
                self.uploaded_files.append({
                    "file_id": file_response.id,
                    "filename": json_file.name,
                    "type": "json"
                })
                logger.info(f"Uploaded JSON: {json_file.name} -> {file_response.id}")
                
            except Exception as e:
                logger.error(f"Failed to upload {json_file.name}: {str(e)}")
        
        # Upload CSV files from metadata directory
        csv_files = list(self.metadata_dir.glob("*.csv"))
        logger.info(f"Found {len(csv_files)} CSV files to upload")
        
        for csv_file in csv_files:
            try:
                with open(csv_file, "rb") as f:
                    file_response = self.client.files.create(
                        file=f,
                        purpose="assistants"
                    )
                
                self.uploaded_files.append({
                    "file_id": file_response.id,
                    "filename": csv_file.name,
                    "type": "csv"
                })
                logger.info(f"Uploaded CSV: {csv_file.name} -> {file_response.id}")
                
            except Exception as e:
                logger.error(f"Failed to upload {csv_file.name}: {str(e)}")
        
        logger.info(f"File upload completed. Total files uploaded: {len(self.uploaded_files)}")
    
    def convert_excel_to_csv(self) -> str:
        """Convert Excel file to CSV for use in instructions."""
        excel_path = self.returns_dir / "Returns.xlsx"
        csv_path = self.returns_dir / "Returns.csv"
        
        if not excel_path.exists():
            logger.warning(f"Excel file not found: {excel_path}")
            logger.warning("Please place Returns.xlsx in the Returns/ directory")
            return None
        
        try:
            # Read Excel file
            df = pd.read_excel(excel_path)
            logger.info(f"Excel file loaded: {df.shape[0]} rows, {df.shape[1]} columns")
            
            # Convert to CSV
            df.to_csv(csv_path, index=False)
            logger.info(f"Excel converted to CSV: {csv_path}")
            
            # Get CSV data for size check
            csv_size = csv_path.stat().st_size
            logger.info(f"CSV file size: {csv_size} bytes")
            
            return str(csv_path)
            
        except Exception as e:
            logger.error(f"Failed to convert Excel to CSV: {str(e)}")
            raise
    
    def upload_excel_file(self) -> str:
        """Upload Excel returns file to OpenAI for persistent access."""
        excel_path = self.returns_dir / "Returns.xlsx"
        
        if not excel_path.exists():
            logger.warning(f"Excel file not found: {excel_path}")
            logger.warning("Please place Returns.xlsx in the Returns/ directory")
            return None
        
        try:
            with open(excel_path, "rb") as f:
                file_response = self.client.files.create(
                    file=f,
                    purpose="assistants"  # Makes it persistent
                )
            
            self.excel_file_id = file_response.id
            logger.info(f"Excel file uploaded: {excel_path.name} -> {file_response.id}")
            return file_response.id
            
        except Exception as e:
            logger.error(f"Failed to upload Excel file: {str(e)}")
            raise
    
    def create_vector_store(self) -> str:
        """Create a vector store for the Responses API file search."""
        logger.info("Creating vector store for Responses API...")
        
        if not self.uploaded_files:
            raise ValueError("No files uploaded. Cannot create vector store.")
        
        # Create vector store with files (exclude CSV files as they're not supported for retrieval)
        file_ids = [file_info["file_id"] for file_info in self.uploaded_files if file_info.get("type") != "csv"]
        
        if not file_ids:
            raise ValueError("No supported files for vector store. CSV files are not supported for retrieval.")
        
        vector_store = self.client.vector_stores.create(
            name="Fund Documents Vector Store",
            file_ids=file_ids
        )
        
        logger.info(f"Created vector store with {len(file_ids)} files: {vector_store.id}")
        logger.info("Note: CSV files are excluded from vector store as they're not supported for retrieval")
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
        
        # Save the vector store ID and Excel file ID for Responses API
        vector_store_id = file_config.get("vector_store_id", "")
        excel_file_id = file_config.get("excel_file_id", "")
        metadata_file_id = file_config.get("metadata_file_id", "")
        config.save_config("", vector_store_id, excel_file_id, metadata_file_id)  # Empty assistant_id, but save vector_store_id, excel_file_id, and metadata_file_id
        logger.info("Configuration saved successfully")
    
    def run_setup(self) -> None:
        """Run the complete setup process."""
        try:
            logger.info("Starting enhanced Kristal.AI's J.A.R.V.I.S setup using Responses API...")
            
            # Step 1: Ensure directories exist
            self.ensure_directories()
            
            # Step 2: Upload files
            self.upload_files()
            
            if not self.uploaded_files:
                logger.warning("No files found to upload. Please add PDF files to 'documents/' and JSON files to 'metadata/' directories.")
                return
            
            # Step 3: Convert Excel to CSV
            csv_path = self.convert_excel_to_csv()
            
            # Step 4: Upload Excel file (for backup/reference)
            excel_file_id = self.upload_excel_file()
            
            # Step 5: Create vector store
            vector_store_id = self.create_vector_store()
            
            # Step 6: Find metadata file ID
            metadata_file_id = None
            for file_info in self.uploaded_files:
                if file_info.get("type") == "csv" and "focus_funds_metadata" in file_info.get("filename", ""):
                    metadata_file_id = file_info["file_id"]
                    logger.info(f"Found metadata file ID: {metadata_file_id}")
                    break
            
            # Step 7: Create file search configuration
            file_config = self.create_file_search_config(vector_store_id)
            file_config["excel_file_id"] = excel_file_id
            file_config["csv_path"] = csv_path
            file_config["metadata_file_id"] = metadata_file_id
            
            # Step 8: Save configuration
            self.save_configuration(file_config)
            
            logger.info("✅ Setup completed successfully!")
            logger.info(f"📁 Total files processed: {len(self.uploaded_files)}")
            logger.info(f"📊 Excel file ID: {excel_file_id}")
            logger.info(f"📄 CSV file: {csv_path}")
            logger.info(f"🔍 Vector store ID: {vector_store_id}")
            logger.info("Files are now ready for use with the Responses API and Code Interpreter")
            
        except Exception as e:
            logger.error(f"Setup failed: {str(e)}")
            raise

def main():
    """Main entry point for the setup script."""
    setup = KristalJARVISSetup()
    setup.run_setup()

if __name__ == "__main__":
    main()
