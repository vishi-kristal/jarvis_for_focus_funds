#!/usr/bin/env python3
"""
Update .env file with metadata file ID.
"""

import os
from pathlib import Path

def update_env_file():
    """Update .env file with metadata file ID."""
    
    env_file = Path(".env")
    metadata_file_id = "file-3c5gfRh9jPFPTgJKHqsXRe"
    
    # Read existing .env content
    if env_file.exists():
        with open(env_file, 'r') as f:
            lines = f.readlines()
    else:
        # Create new .env file
        lines = []
    
    # Update or add METADATA_FILE_ID
    updated_lines = []
    metadata_found = False
    
    for line in lines:
        if line.startswith("METADATA_FILE_ID="):
            updated_lines.append(f"METADATA_FILE_ID={metadata_file_id}\n")
            metadata_found = True
        else:
            updated_lines.append(line)
    
    # Add METADATA_FILE_ID if not found
    if not metadata_found:
        updated_lines.append(f"METADATA_FILE_ID={metadata_file_id}\n")
    
    # Write back to .env file
    with open(env_file, 'w') as f:
        f.writelines(updated_lines)
    
    print(f"✅ Updated .env file with METADATA_FILE_ID={metadata_file_id}")

if __name__ == "__main__":
    update_env_file()
