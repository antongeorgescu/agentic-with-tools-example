#!/usr/bin/env python3
"""
Comprehensive test of the last 8 user queries to show final tool selections
after all improvements made during this conversation.
"""

import chat_tools

agent = chat_tools.FinancialChatAgent()

print("=" * 80)
print("FINAL TOOL SELECTION TEST - LAST 8 USER QUERIES")
print("After all improvements made during this conversation")
print("=" * 80)

queries = [
    {
        "id": 1,
        "query": "Hi, I'm Lisa Thompson, and my SIN is 204-332-181. I have a mortgage of $300,000 at a 3.5% interest rate, and I make monthly payments of $1,500. Can you tell me the current balance and when my final payment will be due?",
        "issue": "Balance vs interest rate conflict",
        "original_problem": "Was using interest_rate_tool instead of balance_tool",
        "expected": "balance_tool"
    },
    {
        "id": 2, 
        "query": "Hi, I'm Sarah Thompson, and my SIN is 204-332-181. I'm in a tough situation and can't make my next three mortgage payments of $1,500 each due next month. What penalties will I face, and what should I do?",
        "issue": "Hardship query falling to general_inquiry", 
        "original_problem": "Was using general_inquiry instead of hardship_tool",
        "expected": "hardship_tool"
    },
    {
        "id": 3,
        "query": "Hi, my name is Sarah Thompson and my SIN is 123-456-789. I'm considering breaking my mortgage early and want to understand how prepayment penalties work, especially regarding Interest Rate Differential (IRD). Are there any situations where these penalties might be waived?",
        "issue": "Prepayment penalty query falling to general_inquiry",
        "original_problem": "Was using general_inquiry instead of refinancing_tool", 
        "expected": "refinancing_tool"
    },
    {
        "id": 4,
        "query": "Hi, I'm Sarah Thompson, and my SIN is 204-332-181. I'm currently making monthly payments of $1,200 on my mortgage of $300,000 at a 3.5% interest rate. I'd like to know how much I can increase my monthly payment by, and could you provide the final payment dates if I increase my payment to $1,500 and $1,800?",
        "issue": "Payment increase vs balance conflict",
        "original_problem": "Was using balance_tool instead of payment_increase_tool",
        "expected": "payment_increase_tool"
    },
    {
        "id": 5,
        "query": "Hi, I'm Olivia Harrison, and my SIN is 204-332-181. I've been struggling financially and I won't be able to make my next three mortgage payments of $1,200 each due next month. What kind of penalties or repercussions should I expect if I miss these payments?",
        "issue": "Hardship vs missed payment (penalty focus)",
        "original_problem": "Complex case - hardship context but penalty question",
        "expected": "hardship_tool or missed_payment_tool"
    },
    {
        "id": 6,
        "query": "Hi, I'm Olivia Harrison, and my SIN is 204-332-181. I've been having some financial difficulties and I will miss my next three mortgage payments of $1,200 each due next month. What kind of penalties or repercussions should I expect if I miss these payments?", 
        "issue": "Hardship vs missed payment variation",
        "original_problem": "Similar to #5 but different wording",
        "expected": "hardship_tool or missed_payment_tool"
    },
    {
        "id": 7,
        "query": "What is my current interest rate?",
        "issue": "Pure interest rate query", 
        "original_problem": "Was falling to general_inquiry",
        "expected": "interest_rate_tool"
    },
    {
        "id": 8,
        "query": "I want to know my rate and balance",
        "issue": "Mixed query prioritization",
        "original_problem": "Should prioritize balance over rate",
        "expected": "balance_tool"
    }
]

results = []
print(f"\n{'#':<3} {'Tool Selected':<20} {'Issue Description':<40}")
print("-" * 80)

for query_data in queries:
    try:
        result = agent._classify_user_query(query_data['query'])
        tool_selected = result.get('tool_name', 'unknown')
        
        # Check if result matches expected
        if isinstance(query_data['expected'], list):
            status = "✅" if tool_selected in query_data['expected'] else "❌"
        else:
            status = "✅" if tool_selected == query_data['expected'] else "❌"
        
        print(f"{query_data['id']:<3} {tool_selected:<20} {query_data['issue']:<40} {status}")
        results.append({
            'query_id': query_data['id'],
            'tool_selected': tool_selected,
            'expected': query_data['expected'],
            'status': status,
            'issue': query_data['issue']
        })
        
    except Exception as e:
        print(f"{query_data['id']:<3} {'ERROR':<20} {str(e):<40} ❌")
        results.append({
            'query_id': query_data['id'], 
            'tool_selected': 'ERROR',
            'expected': query_data['expected'],
            'status': '❌',
            'issue': query_data['issue']
        })

print("\n" + "=" * 80)
print("DETAILED RESULTS")
print("=" * 80)

for i, (query_data, result) in enumerate(zip(queries, results), 1):
    print(f"\n--- Query {i}: {query_data['issue']} ---")
    print(f"Query: {query_data['query'][:100]}{'...' if len(query_data['query']) > 100 else ''}")
    print(f"Expected: {query_data['expected']}")
    print(f"Selected: {result['tool_selected']} {result['status']}")
    print(f"Original Problem: {query_data['original_problem']}")

# Summary
print(f"\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)

passed = sum(1 for r in results if r['status'] == '✅')
total = len(results)
success_rate = (passed / total) * 100

print(f"📊 Overall Results: {passed}/{total} queries correctly classified ({success_rate:.1f}%)")

if success_rate == 100:
    print("🎉 PERFECT! All tool selection issues have been resolved!")
elif success_rate >= 80:
    print("✅ EXCELLENT! Most tool selection issues resolved.")
else:
    print("⚠️  Still some tool selection issues to address.")

print(f"\n🔧 Total improvements made during this conversation:")
print("• Fixed balance vs interest rate tool conflicts")  
print("• Enhanced hardship tool keyword matching")
print("• Added prepayment penalty keywords to refinancing tool")
print("• Improved payment increase tool keyword specificity") 
print("• Clarified hardship vs missed payment tool purposes")