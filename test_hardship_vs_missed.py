#!/usr/bin/env python3
"""
Test hardship vs missed payment tool selection for similar queries.
"""

import chat_tools

agent = chat_tools.FinancialChatAgent()

print("=" * 80)
print("HARDSHIP vs MISSED PAYMENT TOOL ANALYSIS")
print("=" * 80)

# Query 1: Focus on "struggling financially" and "won't be able to make"
query1 = "Hi, I'm Olivia Harrison, and my SIN is 204-332-181. I've been struggling financially and I won't be able to make my next three mortgage payments of $1,200 each due next month. What kind of penalties or repercussions should I expect if I miss these payments?"

# Query 2: Focus on "financial difficulties" and "will miss"  
query2 = "Hi, I'm Olivia Harrison, and my SIN is 204-332-181. I've been having some financial difficulties and I will miss my next three mortgage payments of $1,200 each due next month. What kind of penalties or repercussions should I expect if I miss these payments?"

print("\n=== QUERY 1: Struggling + Won't be able ===")
print(f"Query: {query1}")
result1 = agent._classify_user_query(query1)
print(f"Result: {result1['tool_name']}")

print("\n=== QUERY 2: Difficulties + Will miss ===")  
print(f"Query: {query2}")
result2 = agent._classify_user_query(query2)
print(f"Result: {result2['tool_name']}")

print(f"\n" + "=" * 80)
print("TOOL COMPARISON ANALYSIS")
print("=" * 80)

print("\n📋 CONCEPTUAL DIFFERENCES:")
print("┌─ HARDSHIP TOOL ─────────────────────────────────────────┐")
print("│ • PROACTIVE assistance for financial difficulties        │")
print("│ • Help BEFORE missing payments                           │") 
print("│ • Focus: deferment, payment plans, assistance programs  │")
print("│ • Keywords: struggling, can't make, financial troubles   │")
print("└─────────────────────────────────────────────────────────┘")

print("\n┌─ MISSED PAYMENT TOOL ───────────────────────────────────┐")
print("│ • REACTIVE consequences for missed payments              │")
print("│ • Help AFTER missing payments (or certain to miss)      │")
print("│ • Focus: penalties, late fees, repercussions            │") 
print("│ • Keywords: missed payment, penalties, consequences      │")
print("└─────────────────────────────────────────────────────────┘")

print(f"\n📊 CLASSIFICATION RESULTS:")
print(f"Query 1 (struggling/won't be able): {result1['tool_name']}")
print(f"Query 2 (difficulties/will miss): {result2['tool_name']}")

if result1['tool_name'] != result2['tool_name']:
    print(f"\n⚡ DIFFERENT TOOLS SELECTED based on keyword emphasis!")
else:
    print(f"\n🎯 SAME TOOL SELECTED despite different wording")

print(f"\n💡 RECOMMENDATION:")
print("Both queries ask about penalties/repercussions, suggesting missed_payment_tool")
print("may be more appropriate, but hardship_tool is also valid for financial distress.")