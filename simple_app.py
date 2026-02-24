#!/usr/bin/env python3
"""
Simplified Flask API for Q&A Testing (No LangChain Dependencies)
==============================================================
"""

from flask import Flask, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Mock data for testing
SAMPLE_TOPICS = [
    "Mortgage applications and documentation requirements",
    "Interest rate calculations and payment schedules",
    "Credit score requirements for loan approval",
    "Down payment options and first-time buyer programs",
    "Refinancing benefits and eligibility criteria",
    "Home equity loans and lines of credit",
    "Investment property financing options",
    "Commercial loan application processes",
    "Student loan consolidation and payment options",
    "Personal loan terms and conditions"
]

SAMPLE_TOOLS = [
    "mortgage_calculator", "credit_checker", "document_processor", 
    "rate_analyzer", "payment_scheduler", "loan_evaluator"
]

def generate_mock_qa_pair(topic, tool):
    """Generate a mock Q&A pair for testing."""
    questions = [
        f"What are the requirements for {topic.lower()}?",
        f"How does {topic.lower()} work in practice?", 
        f"Can you explain the process of {topic.lower()}?",
        f"What should I know about {topic.lower()}?",
        f"Help me understand {topic.lower()}."
    ]
    
    answers = [
        f"For {topic.lower()}, you'll need to consider several key factors including documentation, eligibility criteria, and processing timelines. Our {tool} can help you navigate this process effectively.",
        f"The {topic.lower()} process involves multiple steps that we can break down for you. Using our {tool}, we can provide personalized guidance based on your specific situation.",
        f"When dealing with {topic.lower()}, it's important to understand the requirements and options available. The {tool} tool helps analyze your specific needs and provide tailored recommendations."
    ]
    
    return {
        "question": random.choice(questions),
        "answer": random.choice(answers),
        "topic": topic,
        "tool_used": f"(function) {tool}",
        "parameters": {"query": "sample query", "user_id": "test_user"},
        "description": f"Tool for analyzing {topic.lower()}"
    }

@app.route('/run_new_caller/<int:npairs>', methods=['GET'])
def run_new_caller(npairs: int):
    """Generate npairs of mock question/answer pairs for testing."""
    
    # Input validation
    if npairs <= 0:
        return jsonify({"error": "npairs must be a positive integer"}), 400
    
    if npairs > 100:  # Set reasonable limit
        return jsonify({"error": "npairs cannot exceed 100"}), 400
    
    # Generate mock Q&A pairs
    qa_pairs = []
    tools_used = set()
    tool_usage_count = {}
    topics_used = set()
    
    for i in range(npairs):
        # Select random topic and tool
        topic = random.choice(SAMPLE_TOPICS)
        tool = random.choice(SAMPLE_TOOLS)
        
        # Generate mock Q&A pair
        qa_pair = generate_mock_qa_pair(topic, tool)
        qa_pair["topic_index"] = SAMPLE_TOPICS.index(topic) + 1
        
        qa_pairs.append(qa_pair)
        
        # Track usage
        topics_used.add(topic)
        tools_used.add(tool)
        tool_usage_count[tool] = tool_usage_count.get(tool, 0) + 1
    
    # Prepare result structure (matching the original API)
    result = {
        "qa_pairs": qa_pairs,
        "tools_used": list(tools_used),
        "tool_summary": {
            "unique_tools": list(tools_used),
            "total_tools_used": len(tools_used),
            "tool_usage_count": tool_usage_count,
            "total_qa_pairs": len(qa_pairs)
        },
        "topics": list(topics_used)
    }
    
    # Return JSON response (matching original API structure)
    return jsonify({
        "success": True,
        "count": npairs,
        "actual_count": len(qa_pairs),
        "tools_used": list(tools_used),
        "result": result
    })

@app.route('/run_new_caller/tool_list', methods=['GET'])
def get_tool_list():
    """Get the list of available tools."""
    return jsonify({"tools": SAMPLE_TOOLS})

@app.route('/run_new_caller/topics_list', methods=['GET'])
def get_topics_list():
    """Get the list of available topics."""
    return jsonify({"topics": SAMPLE_TOPICS})

@app.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint."""
    return jsonify({"status": "healthy", "message": "Mock Flask API is running"})

if __name__ == '__main__':
    print("Starting Mock Flask API for Q&A Testing...")
    print("API Endpoints:")
    print("  GET /run_new_caller/<int:npairs> - Generate Q&A pairs")
    print("  GET /run_new_caller/tool_list - Get available tools")
    print("  GET /run_new_caller/topics_list - Get available topics") 
    print("  GET /health - Health check")
    print("\nServer running at: http://localhost:5000")
    
    app.run(host='0.0.0.0', port=5000, debug=True)