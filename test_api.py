#!/usr/bin/env python3
"""
Test script for Flask API
"""

import requests
import json

# Base URL
BASE_URL = "http://localhost:5000"

def test_get_endpoint():
    """Test GET endpoint with URL parameter."""
    print("Testing GET /run_new_caller/<npairs>...")
    
    # Test with 5 pairs
    response = requests.get(f"{BASE_URL}/run_new_caller/5")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Success: Got {data['count']} pairs")
        print(f"First pair: {data['qa_pairs'][0]}")
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")

# def test_post_endpoint():
#     """Test POST endpoint with JSON body."""
#     print("\nTesting POST /run_new_caller...")
    
#     # Test with 3 pairs
#     payload = {"npairs": 3}
#     headers = {"Content-Type": "application/json"}
    
#     response = requests.post(f"{BASE_URL}/run_new_caller", 
#                            json=payload, headers=headers)
    
#     if response.status_code == 200:
#         data = response.json()
#         print(f"✅ Success: Got {data['count']} pairs")
#         print(f"All pairs: {json.dumps(data['qa_pairs'], indent=2)}")
#     else:
#         print(f"❌ Error: {response.status_code} - {response.text}")

def test_tool_list_endpoint():
    """Test tool list endpoint."""
    print("\nTesting GET /run_new_caller/tool_list...")
    
    response = requests.get(f"{BASE_URL}/run_new_caller/tool_list")
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Success: Tool list retrieved")
        tools = data.get('tools', [])
        print(f"Available tools count: {len(tools)}")
        if tools:
            print(f"Sample tools: {tools[:3]}...")  # Show first 3 tools
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")

def test_home_endpoint():
    """Test home endpoint for documentation."""
    print("\nTesting GET /...")
    
    response = requests.get(f"{BASE_URL}/")
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Success: API documentation retrieved")
        print(f"Available endpoints: {list(data['endpoints'].keys())}")
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")

def test_error_cases():
    """Test error handling."""
    print("\nTesting error cases...")
    
    # Test negative number
    response = requests.get(f"{BASE_URL}/run_new_caller/-1")
    print(f"Negative npairs: {response.status_code} - {response.json()['error']}")
    
    # Test too large number  
    response = requests.get(f"{BASE_URL}/run_new_caller/1001")
    print(f"Too large npairs: {response.status_code} - {response.json()['error']}")
    
    # Test invalid POST body
    response = requests.post(f"{BASE_URL}/run_new_caller", 
                           json={"invalid": "data"})
    print(f"Invalid POST body: {response.status_code} - {response.json()['error']}")

if __name__ == "__main__":
    print("🚀 Testing Flask API...")
    print("Make sure the Flask server is running: python app.py")
    print("=" * 50)
    
    try:
        test_home_endpoint()
        test_tool_list_endpoint()
        test_get_endpoint()
        # test_post_endpoint()
        test_error_cases()
        print("\n🎉 All tests completed!")
        
    except requests.ConnectionError:
        print("❌ Connection Error: Make sure Flask server is running!")
        print("Run: python app.py")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")