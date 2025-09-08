#!/usr/bin/env python3
"""
Monthly script to refresh Excel returns data
Run this monthly to update the returns data
"""

import os
import logging
from pathlib import Path
from datetime import datetime
import pandas as pd
from openai import OpenAI
from config import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ExcelRefreshManager:
    def __init__(self):
        self.client = OpenAI(api_key=config.openai_api_key)
    
    def convert_excel_to_csv(self, excel_path: str) -> str:
        """Convert Excel file to CSV for use in instructions."""
        csv_path = "Returns/Returns.csv"
        
        try:
            # Read Excel file
            df = pd.read_excel(excel_path)
            logger.info(f"Excel file loaded: {df.shape[0]} rows, {df.shape[1]} columns")
            
            # Convert to CSV
            df.to_csv(csv_path, index=False)
            logger.info(f"Excel converted to CSV: {csv_path}")
            
            # Get CSV data for size check
            csv_size = Path(csv_path).stat().st_size
            logger.info(f"CSV file size: {csv_size} bytes")
            
            return csv_path
            
        except Exception as e:
            logger.error(f"Failed to convert Excel to CSV: {str(e)}")
            raise
    
    def refresh_excel_data(self, excel_path: str) -> str:
        """Refresh Excel data with new file"""
        
        if not Path(excel_path).exists():
            raise FileNotFoundError(f"Excel file not found: {excel_path}")
        
        try:
            # Step 1: Convert Excel to CSV
            csv_path = self.convert_excel_to_csv(excel_path)
            
            # Step 2: Upload new Excel file
            with open(excel_path, "rb") as f:
                file_response = self.client.files.create(
                    file=f,
                    purpose="assistants"
                )
            
            new_file_id = file_response.id
            logger.info(f"New Excel file uploaded: {file_response.id}")
            
            # Step 3: Update configuration
            config.save_config("", config.vector_store_id, new_file_id)
            
            logger.info(f"✅ Excel data refreshed successfully!")
            logger.info(f"📁 New file ID: {new_file_id}")
            logger.info(f"📄 CSV file: {csv_path}")
            logger.info(f"📅 Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            return new_file_id
            
        except Exception as e:
            logger.error(f"Failed to refresh Excel data: {str(e)}")
            raise

def main():
    """Main entry point for Excel refresh"""
    excel_path = "Returns/Returns.xlsx"
    
    try:
        refresh_manager = ExcelRefreshManager()
        new_file_id = refresh_manager.refresh_excel_data(excel_path)
        print(f"✅ Excel data refreshed successfully! New file ID: {new_file_id}")
        
    except Exception as e:
        print(f"❌ Excel refresh failed: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()
