#!/usr/bin/env python3
"""
Test script to debug the API issue
"""

import requests
import json
import time

def test_health():
    """Test the health endpoint"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=10)
        print(f"Health check status: {response.status_code}")
        print(f"Health check response: {response.json()}")
        return True
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_ask_question():
    """Test the ask question endpoint"""
    try:
        question = "calculate the annualized volatility of peregrine in 2019 and 2022?"
        payload = {"question": question}
        
        print(f"Testing question: {question}")
        print("Sending request...")
        
        response = requests.post(
            "http://localhost:8000/api/ask",
            json=payload,
            timeout=60  # 1 minute timeout
        )
        
        print(f"Response status: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Answer: {result.get('answer', 'No answer')[:200]}...")
            print(f"Images: {len(result.get('images', []))}")
        else:
            print(f"Error response: {response.text}")
            
        return response.status_code == 200
        
    except requests.exceptions.Timeout:
        print("Request timed out after 60 seconds")
        return False
    except Exception as e:
        print(f"Request failed: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Testing J.A.R.V.I.S API")
    print("=" * 40)
    
    # Test health first
    print("\n1. Testing health endpoint...")
    if test_health():
        print("✅ Health check passed")
        
        # Test question
        print("\n2. Testing question endpoint...")
        if test_ask_question():
            print("✅ Question test passed")
        else:
            print("❌ Question test failed")
    else:
        print("❌ Health check failed - server not running")
