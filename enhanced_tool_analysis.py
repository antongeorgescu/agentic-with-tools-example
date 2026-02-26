#!/usr/bin/env python3
"""
Enhanced analysis of hardship vs missed payment tool selection.
Shows the tool ordering issue and conceptual differences.
"""

import chat_tools

agent = chat_tools.FinancialChatAgent()

print("=" * 80)
print("ENHANCED HARDSHIP vs MISSED PAYMENT ANALYSIS")
print("=" * 80)

test_cases = [
    {
        "query": "Hi, I'm Olivia Harrison, and my SIN is 204-332-181. I've been struggling financially and I won't be able to make my next three mortgage payments of $1,200 each due next month. What kind of penalties or repercussions should I expect if I miss these payments?",
        "description": "Mixed: Hardship + Penalty question",
        "expected_tools": ["hardship_tool", "missed_payment_tool"],
        "primary_intent": "Penalty consequences (missed_payment_tool)"
    },
    {
        "query": "Hi, I'm Olivia Harrison, and my SIN is 204-332-181. I've been having some financial difficulties and I will miss my next three mortgage payments of $1,200 each due next month. What kind of penalties or repercussions should I expect if I miss these payments?", 
        "description": "Mixed: Difficulties + Penalty question",
        "expected_tools": ["hardship_tool", "missed_payment_tool"],
        "primary_intent": "Penalty consequences (missed_payment_tool)"
    },
    {
        "query": "I'm struggling financially and need help with payment options. Are there any assistance programs available?",
        "description": "Pure hardship: seeking assistance",
        "expected_tools": ["hardship_tool"],
        "primary_intent": "Financial assistance (hardship_tool)"
    },
    {
        "query": "I missed my last three payments. What are the penalties and late fees I'll face?",
        "description": "Pure penalty: consequences focus", 
        "expected_tools": ["missed_payment_tool"],
        "primary_intent": "Penalty information (missed_payment_tool)"
    },
    {
        "query": "What happens if I miss my mortgage payment? What are the repercussions?",
        "description": "Pure penalty: general consequences",
        "expected_tools": ["missed_payment_tool"], 
        "primary_intent": "Penalty information (missed_payment_tool)"
    }
]

print("\n🔍 TOOL ORDERING ISSUE:")
print("Current order: hardship_tool (4th) → missed_payment_tool (6th)")
print("Problem: Hardship keywords match first, even for penalty-focused queries\n")

for i, test_case in enumerate(test_cases, 1):
    print(f"--- Test {i}: {test_case['description']} ---")
    print(f"Query: {test_case['query']}")
    
    result = agent._classify_user_query(test_case['query'])
    tool_name = result.get('tool_name', 'unknown')
    
    print(f"Selected: {tool_name}")
    print(f"Primary Intent: {test_case['primary_intent']}")
    
    if tool_name in test_case['expected_tools']:
        if tool_name == test_case['primary_intent'].split('(')[1].split(')')[0]:
            print("✅ CORRECT - matches primary intent")
        else:
            print("⚠️  ACCEPTABLE - but not ideal for primary intent")
    else:
        print("❌ UNEXPECTED")
    print()

print("=" * 80)
print("CONCEPTUAL TOOL DIFFERENCES")  
print("=" * 80)

print("""
🔧 HARDSHIP TOOL - Proactive Financial Assistance
├─ Purpose: Help people in financial distress BEFORE they miss payments
├─ Focus: Payment plans, deferments, assistance programs, forbearance  
├─ Typical queries: "I'm struggling", "Can't make payments", "Need help"
├─ Keywords: struggling, financial difficulties, can't pay, payment help
└─ Outcome: Assistance options and programs

💰 MISSED PAYMENT TOOL - Reactive Penalty Information  
├─ Purpose: Inform about consequences AFTER missing (or certain to miss) payments
├─ Focus: Penalties, late fees, repercussions, recovery options
├─ Typical queries: "What penalties?", "What happens if I miss?", "Late fees?"  
├─ Keywords: missed payment, penalties, repercussions, consequences, late fees
└─ Outcome: Penalty calculations and recovery steps

⚖️  OVERLAP SCENARIOS:
When a query contains BOTH hardship indicators AND penalty questions,
the current system prioritizes hardship_tool due to tool ordering.

📋 RECOMMENDATION:  
For penalty-focused queries (like Olivia's), missed_payment_tool may be more
appropriate even if financial distress is mentioned as context.
""")

print("=" * 80)