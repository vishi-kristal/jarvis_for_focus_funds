#!/usr/bin/env python3
"""
Test script for the GenAI FundScreener backend API.
"""

import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:8000"

def test_health():
    """Test the health endpoint."""
    print("🔍 Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_question(question):
    """Test asking a question to the API."""
    print(f"❓ Question: {question}")
    print("⏳ Processing...")
    
    start_time = time.time()
    response = requests.post(
        f"{BASE_URL}/api/ask",
        headers={"Content-Type": "application/json"},
        json={"question": question}
    )
    end_time = time.time()
    
    print(f"⏱️  Response time: {end_time - start_time:.2f} seconds")
    print(f"📊 Status: {response.status_code}")
    
    if response.status_code == 200:
        answer = response.json()["answer"]
        print(f"✅ Answer:\n{answer}")
    else:
        print(f"❌ Error: {response.text}")
    print("-" * 80)
    print()

def main():
    """Run all tests."""
    print("🚀 Testing GenAI FundScreener Backend")
    print("=" * 80)
    
    # Test health
    test_health()
    
    # Test questions
    test_questions = [
        "Which are the alternatives low vol funds available in the system?"
    ]
    
    for question in test_questions:
        test_question(question)
        time.sleep(1)  # Small delay between requests
    
    print("🎉 Testing completed!")

if __name__ == "__main__":
    main()
