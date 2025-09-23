"""
Configuration management for the GenAI FundScreener application.
Handles loading environment variables and managing persistent configuration.
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration class."""
    
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.assistant_id = os.getenv("ASSISTANT_ID")
        self.vector_store_id = os.getenv("VECTOR_STORE_ID")
        self.excel_file_id = os.getenv("EXCEL_FILE_ID")
        self.metadata_file_id = os.getenv("METADATA_FILE_ID")
        self.host = os.getenv("HOST", "0.0.0.0")
        self.port = int(os.getenv("PORT", 8000))
        self.debug = os.getenv("DEBUG", "True").lower() == "true"
        
        # Validate required configuration
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required in environment variables")
    
    def save_config(self, assistant_id: str, vector_store_id: str, excel_file_id: str = None, metadata_file_id: str = None) -> None:
        """Save assistant, vector store, Excel file, and metadata file IDs to environment file."""
        env_file = Path(".env")
        
        # Read existing .env file
        env_content = ""
        if env_file.exists():
            env_content = env_file.read_text()
        
        # Update or add configuration values
        lines = env_content.split('\n') if env_content else []
        updated_lines = []
        assistant_found = False
        vector_store_found = False
        excel_file_found = False
        metadata_file_found = False
        
        for line in lines:
            if line.startswith("ASSISTANT_ID="):
                updated_lines.append(f"ASSISTANT_ID={assistant_id}")
                assistant_found = True
            elif line.startswith("VECTOR_STORE_ID="):
                updated_lines.append(f"VECTOR_STORE_ID={vector_store_id}")
                vector_store_found = True
            elif line.startswith("EXCEL_FILE_ID="):
                updated_lines.append(f"EXCEL_FILE_ID={excel_file_id or ''}")
                excel_file_found = True
            elif line.startswith("METADATA_FILE_ID="):
                updated_lines.append(f"METADATA_FILE_ID={metadata_file_id or ''}")
                metadata_file_found = True
            else:
                updated_lines.append(line)
        
        # Add missing configuration
        if not assistant_found:
            updated_lines.append(f"ASSISTANT_ID={assistant_id}")
        if not vector_store_found:
            updated_lines.append(f"VECTOR_STORE_ID={vector_store_id}")
        if not excel_file_found and excel_file_id:
            updated_lines.append(f"EXCEL_FILE_ID={excel_file_id}")
        if not metadata_file_found and metadata_file_id:
            updated_lines.append(f"METADATA_FILE_ID={metadata_file_id}")
        
        # Write back to .env file
        env_file.write_text('\n'.join(updated_lines))
        
        # Update instance variables
        self.assistant_id = assistant_id
        self.vector_store_id = vector_store_id
        if excel_file_id:
            self.excel_file_id = excel_file_id
        if metadata_file_id:
            self.metadata_file_id = metadata_file_id

# Global configuration instance
config = Config()
