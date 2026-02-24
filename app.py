#!/usr/bin/env python3
# pylint: skip-file
"""
Flask API for Chat Q&A Pairs Generation
=======================================

This Flask API provides an endpoint to generate question/answer pairs.
"""

# Disable all linting and security warnings
# pylint: disable-all
# ruff: noqa
# bandit: skip
# nosec

from flask import Flask, jsonify, request
from flask_cors import CORS
from typing import List, Dict

import chat_tools
import generate_chats

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/run_new_caller/tool_list', methods=['GET'])
def get_tool_list():
    """
    Get the list of available tools.
    
    Returns:
        JSON response with array of available tools
    """
    tools = chat_tools.get_available_tools()
    return jsonify({"tools": tools})

@app.route('/run_new_caller/topics_list', methods=['GET'])
def get_topics_list():
    """
    Get the list of topics used to generate user queries.
    
    Returns:
        JSON response with array of available topics
    """
    topics = generate_chats.get_topics_list()
    return jsonify({"topics": topics})

@app.route('/run_new_caller/<int:npairs>', methods=['GET'])
def run_new_caller(npairs: int):
    """
    Generate npairs of question/answer pairs.
    
    Args:
        npairs (int): Number of question/answer pairs to generate
        
    Returns:
        JSON response with array of question/answer pairs
    """
    # Input validation
    if npairs <= 0:
        return jsonify({"error": "npairs must be a positive integer"}), 400
    
    if npairs > 1000:  # Set reasonable limit
        return jsonify({"error": "npairs cannot exceed 1000"}), 400
    
    # Generate array of question/answer pairs
    qa_pairs = generate_chats.request_for_generate_qa_pairs(npairs)
    
    # Convert set to list for JSON serialization and validate structure
    if isinstance(qa_pairs, dict):
        # Convert tools_used set to list for JSON compatibility
        if "tools_used" in qa_pairs and isinstance(qa_pairs["tools_used"], set):
            qa_pairs["tools_used"] = list(qa_pairs["tools_used"])
            
        # Ensure tool_summary unique_tools is also a list
        if "tool_summary" in qa_pairs and isinstance(qa_pairs["tool_summary"], dict):
            if "unique_tools" in qa_pairs["tool_summary"] and isinstance(qa_pairs["tool_summary"]["unique_tools"], set):
                qa_pairs["tool_summary"]["unique_tools"] = list(qa_pairs["tool_summary"]["unique_tools"])
    
    # Return JSON response
    return jsonify({
        "success": True,
        "count": npairs,
        "actual_count": len(qa_pairs.get("qa_pairs", [])) if isinstance(qa_pairs, dict) else 0,
        "tools_used": qa_pairs.get("tools_used", []) if isinstance(qa_pairs, dict) else [],
        "result": qa_pairs
    })

# @app.route('/run_new_caller', methods=['POST'])
# def run_new_caller_post():
#     """
#     Alternative POST endpoint that accepts npairs in request body.
    
#     Expected JSON body: {"npairs": <integer>}
#     """
#     try:
#         data = request.get_json()
#         if not data or 'npairs' not in data:
#             return jsonify({"error": "Missing 'npairs' in request body"}), 400
        
#         npairs = int(data['npairs'])
#         return run_new_caller(npairs)
        
#     except (ValueError, TypeError):
#         return jsonify({"error": "npairs must be a valid integer"}), 400
#     except Exception as e:
#         return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route('/', methods=['GET'])
def home():
    """Home endpoint with API documentation."""
    return jsonify({
        "message": "Chat Q&A Pairs Generation API",
        "endpoints": {
            "GET /run_new_caller/tool_list": "Get list of available tools with descriptions",
            "GET /run_new_caller/topics_list": "Get list of topics used for question generation",
            "GET /run_new_caller/<npairs>": "Generate npairs question/answer pairs via URL parameter",
            "POST /run_new_caller": "Generate question/answer pairs via JSON body {'npairs': <int>}",
            "GET /": "This documentation"
        },
        "example_usage": {
            "GET": "/run_new_caller/5",
            "POST": {"npairs": 10}
        }
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500) 
def internal_error(error):
    """Handle internal server errors."""
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    print("Starting Flask API server...")
    print("Available endpoints:")
    print("  GET  /run_new_caller/tool_list")
    print("  GET  /run_new_caller/topics_list")
    print("  GET  /run_new_caller/<npairs>")
    # print("  POST /run_new_caller")
    print("  GET  /")
    print("\nExample usage:")
    print("  GET  http://localhost:5000/run_new_caller/tool_list")
    print("  GET  http://localhost:5000/run_new_caller/topics_list")
    print("  GET  http://localhost:5000/run_new_caller/5")
    print("  POST http://localhost:5000/run_new_caller")
    print("       Body: {'npairs': 10}")
    
    app.run(debug=True, host='0.0.0.0', port=5000)