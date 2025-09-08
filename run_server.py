#!/usr/bin/env python3
"""
Convenience script to run the FastAPI server with proper configuration.
"""

import uvicorn
from config import config

if __name__ == "__main__":
    print(f"Starting GenAI FundScreener API server...")
    print(f"Host: {config.host}")
    print(f"Port: {config.port}")
    print(f"Debug mode: {config.debug}")
    print(f"API Documentation: http://{config.host}:{config.port}/docs")
    print(f"Health Check: http://{config.host}:{config.port}/health")
    print("-" * 50)
    
    uvicorn.run(
        "main:app",
        host=config.host,
        port=config.port,
        reload=config.debug,
        log_level="info"
    )
