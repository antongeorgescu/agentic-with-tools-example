#!/usr/bin/env python3
"""
Test script to verify tool classification is working correctly
"""

import chat_tools

# Test the specific user query that was failing
test_query = "I've just been pre-approved for a mortgage, and I'm wondering what the next steps are. What documents do I need to submit, and how long does the income verification and credit check process usually take?"

print("🧪 Testing Tool Classification")
print("=" * 60)
print(f"Query: {test_query}")
print()

# Get the agent and test classification
agent = chat_tools.get_agent()
result = agent._classify_user_query(test_query)

print()
print("🎯 Classification Result:")
print(f"Tool: {result['tool_name']}")
print(f"Description: {result['description']}")
print()

# Test a few more queries to verify the fix
test_queries = [
    "What's my current loan balance?",
    "Can I increase my monthly payment?", 
    "What interest rate am I paying?",
    "I got pre-approved yesterday",
    "I need to refinance my mortgage",
    "What documents do I need for my application?"
]

print("🧪 Additional Test Cases:")
print("=" * 60)
for query in test_queries:
    result = agent._classify_user_query(query)
    print(f"Query: '{query[:40]}...'")
    print(f"  → {result['tool_name']}")
    print()