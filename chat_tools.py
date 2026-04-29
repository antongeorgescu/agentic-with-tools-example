#!/usr/bin/env python3
# pylint: skip-file

import os
from pathlib import Path

# Load environment variables from .env file
def load_dotenv():
    """Load environment variables from .env file for consistent configuration."""
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    value = value.strip('"\'')
                    os.environ[key] = value

# Load environment at module level
load_dotenv()

# Apply consistent random seed for production mode
if os.getenv("DEBUG_MODE", "false").lower() == "false":
    import random
    seed_value = int(os.getenv("RANDOM_SEED", "42"))
    random.seed(seed_value)
    print(f"🎲 Applied consistent random seed: {seed_value}")

"""
LangChain Agent-Based Chat Tools for Financial Topics
====================================================

This module implements a LangChain-based agent system that uses tools to handle
various financial/mortgage topics. The agent can intelligently select and use
appropriate tools based on user queries.
"""

# Disable all linting and security warnings
# pylint: disable-all
# ruff: noqa
# bandit: skip
# nosec

from json import tool
import os
import json
import random
from typing import List, Dict, Any, Optional
try:
    # Try newer LangChain imports first
    from langchain_community.chat_models import AzureChatOpenAI
    from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
    from langchain.tools import Tool, BaseTool
    from langchain.schema import BaseMessage
    from langchain.memory import ConversationBufferMemory
    print("Using langchain-community imports")
except ImportError:
    try:
        # Fallback to older imports if needed
        from langchain.chat_models import AzureChatOpenAI
        from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
        from langchain.tools import Tool, BaseTool
        from langchain.schema import BaseMessage
        from langchain.memory import ConversationBufferMemory
        print("Using legacy langchain imports")
    except ImportError as e:
        print(f"Import error: {e}")
        # Create mock classes for testing
        class MockLLM:
            def __init__(self, *args, **kwargs):
                pass
        class MockTool:
            def __init__(self, *args, **kwargs):
                pass
        class MockBaseTool:
            def __init__(self, *args, **kwargs):
                pass
        class MockMessage:
            def __init__(self, *args, **kwargs):
                pass
        class MockMemory:
            def __init__(self, *args, **kwargs):
                pass
        class MockPromptTemplate:
            def __init__(self, *args, **kwargs):
                pass
            @classmethod
            def from_messages(cls, *args, **kwargs):
                return cls()
        AzureChatOpenAI = MockLLM
        Tool = MockTool
        BaseTool = MockBaseTool
        BaseMessage = MockMessage
        ConversationBufferMemory = MockMemory
        ChatPromptTemplate = MockPromptTemplate
        MessagesPlaceholder = MockPromptTemplate
        
from pydantic import BaseModel, Field
import re


def extract_sin_number(query: str, force_random: bool = None) -> str:
    """
    Extract SIN (Social Insurance Number) from user query, or generate a random one for simulation.
    
    Args:
        query (str): User's query text
        force_random (bool): If True, always generate random SIN (for testing scenarios)
                           If None, uses FORCE_RANDOM_SIN environment variable
        
    Returns:
        str: Found SIN number or randomly generated SIN for simulation
    """
    # Check environment variable if force_random not explicitly set
    if force_random is None:
        force_random = os.getenv("FORCE_RANDOM_SIN", "false").lower() == "true"

    if os.getenv("DEBUG_MODE", "false").lower() == "true":
        print(f"🔍 DEBUG: Searching for SIN in query: '{query}' (force_random={force_random})")

    if force_random:
        if os.getenv("DEBUG_MODE", "false").lower() == "true":
            print(f"🎲 DEBUG: Force random mode - GENERATING random SIN (ignoring any SIN in query)...")
        # Generate random SIN for simulation when none provided
        import random
        # Apply consistent seed if DEBUG_MODE is false
        if os.getenv("DEBUG_MODE", "false").lower() == "false":
            seed_value = int(os.getenv("RANDOM_SEED", "42"))
            random.seed(seed_value)
        
        # Generate 9 random digits, avoiding invalid patterns
        # Valid SIN ranges: first digit 1-9, others 0-9, avoid certain test patterns
        first_digit = random.randint(1, 9)
        remaining_digits = [random.randint(0, 9) for _ in range(8)]
        
        # Format as XXX-XXX-XXX
        sin_digits = [first_digit] + remaining_digits
        sin = f"{sin_digits[0]}{sin_digits[1]}{sin_digits[2]}-{sin_digits[3]}{sin_digits[4]}{sin_digits[5]}-{sin_digits[6]}{sin_digits[7]}{sin_digits[8]}"
        
        if os.getenv("DEBUG_MODE", "false").lower() == "true":
            print(f"🎲 DEBUG: GENERATED random SIN: {sin}")
        return sin
    
    # SIN format: XXX-XXX-XXX or XXXXXXXXX
    sin_patterns = [
        r'\b\d{3}-\d{3}-\d{3}\b',  # XXX-XXX-XXX format
        r'\b\d{9}\b'               # XXXXXXXXX format (9 consecutive digits)
    ]
    
    for pattern in sin_patterns:
        match = re.search(pattern, query)
        if match:
            sin = match.group()
            # Normalize to XXX-XXX-XXX format
            if '-' not in sin:
                sin = f"{sin[:3]}-{sin[3:6]}-{sin[6:]}"
            if os.getenv("DEBUG_MODE", "false").lower() == "true":
                print(f"✅ DEBUG: EXTRACTED existing SIN from query: {sin}")
            return sin
    
    # Generate random SIN for simulation when none provided
    import random
    if os.getenv("DEBUG_MODE", "false").lower() == "true":
        print(f"🎲 DEBUG: No SIN found in query, GENERATING random SIN...")
    
    # Generate 9 random digits, avoiding invalid patterns
    # Valid SIN ranges: first digit 1-9, others 0-9, avoid certain test patterns
    first_digit = random.randint(1, 9)
    remaining_digits = [random.randint(0, 9) for _ in range(8)]
    
    # Format as XXX-XXX-XXX
    sin_digits = [first_digit] + remaining_digits
    sin = f"{sin_digits[0]}{sin_digits[1]}{sin_digits[2]}-{sin_digits[3]}{sin_digits[4]}{sin_digits[5]}-{sin_digits[6]}{sin_digits[7]}{sin_digits[8]}"
    
    if os.getenv("DEBUG_MODE", "false").lower() == "true":
        print(f"🎲 DEBUG: GENERATED random SIN: {sin}")
    return sin

def generate_random_sin() -> str:
    """Generate a random SIN in XXX-XXX-XXX format for testing."""
    first_digit = random.randint(1, 9)
    remaining_digits = [random.randint(0, 9) for _ in range(8)]
    sin_digits = [first_digit] + remaining_digits
    return f"{sin_digits[0]}{sin_digits[1]}{sin_digits[2]}-{sin_digits[3]}{sin_digits[4]}{sin_digits[5]}-{sin_digits[6]}{sin_digits[7]}{sin_digits[8]}"


def generate_random_name() -> str:
    """Generate a random realistic name for testing."""
    first_names = [
        "Emily", "John", "Sarah", "Michael", "Jessica", "David", "Ashley", "Christopher",
        "Amanda", "Matthew", "Jennifer", "Joshua", "Elizabeth", "Andrew", "Stephanie",
        "Daniel", "Nicole", "James", "Michelle", "Ryan", "Lisa", "Robert", "Angela"
    ]
    
    last_names = [
        "Thompson", "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
        "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson",
        "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez"
    ]
    
    return f"{random.choice(first_names)} {random.choice(last_names)}"


def generate_query_with_random_sin(query_type: str = "balance") -> str:
    """
    Generate a realistic, detailed test query with a random SIN and name embedded.

    Args:
        query_type: One of 'balance', 'payment_increase', 'lump_sum', 'rates',
                    'missed_payment', 'pre_approval', 'application', 'refinance',
                    'hardship', 'insurance'.

    Returns:
        str: A multi-sentence query with the SIN and name embedded.
    """
    name = generate_random_name()
    sin = generate_random_sin()

    query_templates = {
        "balance": [
            f"My name is {name} and my Social Insurance Number is {sin}. I have been making regular bi-weekly payments on my mortgage for several years and I would like to confirm my current remaining balance as well as review my upcoming payment schedule through the end of the year. Could you please pull up my account and tell me the exact outstanding balance, the projected payoff date at my current payment pace, and whether I am ahead or behind on the original amortization schedule?",
            f"Hi, I am {name} with SIN {sin}. My mortgage term is coming up for renewal in the next several months and before I start comparing new rates from different lenders I need to know my exact current balance and how much equity I have built up in the property. Could you please look up my account and confirm my outstanding principal balance, the current loan-to-value ratio, and what the remaining payment schedule looks like between now and the end of my term?",
            f"Hello, this is {name}, my SIN is {sin}. I recently received an annual statement but the numbers did not look right to me and I would like to verify my actual current loan balance directly with the lender. Could you confirm the exact outstanding balance on my mortgage as of today, provide my current payment schedule for the next six months, and let me know when my next scheduled payment is due and for what amount?",
            f"Good morning, I am {name} (SIN: {sin}). I am doing a full review of my personal finances this month and one of the key figures I need is my current mortgage balance so I can accurately calculate my net worth and equity position. Could you please pull up my account, confirm the current outstanding principal balance, tell me how many payments remain on my mortgage, and provide the projected final payment date if I continue at my current payment amount?",
            f"This is {name}, my SIN is {sin}. I would like to understand the current state of my mortgage in detail, including how much of my monthly payment is going to principal versus interest at this point in the amortization. Could you please look up my account and provide the current remaining balance, a breakdown of my most recent payment showing principal and interest portions, and my projected payoff date at the current payment pace?",
        ],
        "payment_increase": [
            f"My name is {name} and my SIN is {sin}. I recently received a promotion and my take-home income has increased significantly, so I would like to increase my monthly payment amount to pay the loan down faster and reduce my total interest cost. Could you please look at my account and show me the projected savings if I increase my monthly payment by two hundred, four hundred, and six hundred dollars respectively, including how many years each increase would cut from my remaining amortization?",
            f"Hi, I am {name} with SIN {sin}. I am trying to be more aggressive about paying down my mortgage and I want to understand exactly how much I am allowed to increase my regular payment amount under my current mortgage contract without triggering any penalties. Could you review my account, confirm the maximum payment increase permitted, and show me how each increment would affect my remaining term and total interest paid over the life of the loan?",
            f"Hello, this is {name}, SIN {sin}. I have additional cash flow available each month and I would like to direct it toward my mortgage by increasing my monthly payment amount rather than making separate lump-sum contributions. Can you calculate what would happen to my final payoff date and total interest charges if I were to increase my monthly payment by a few hundred dollars, and advise me on the best way to set that up with the lender?",
            f"I am {name}, SIN {sin}. I want to pay more on my mortgage each month to build equity faster and reduce the overall interest burden over time. Please review my account and advise me on the maximum payment increase I can make without penalty under my current contract, and provide a few scenarios showing the projected impact on my total interest cost and how many years I would cut off the remaining amortization.",
            f"This is {name}, my SIN is {sin}. My current mortgage payments feel very manageable given my income and I am keen to increase my monthly payment to get the loan paid off sooner. Could you look up my account, confirm my current regular payment amount, and model out the outcome if I increase my monthly payment by three hundred, five hundred, and eight hundred dollars — specifically the interest saved and the new projected payoff date for each scenario?",
        ],
        "lump_sum": [
            f"My name is {name} and my SIN is {sin}. I recently came into some unexpected funds and I am seriously considering making a lump-sum payment on my mortgage before my next term anniversary date. Could you please look up my account and tell me the maximum lump-sum contribution I am allowed to make this year under my prepayment privileges, and calculate how much that payment would reduce my remaining balance, lower my total interest charges, and shorten my amortization period?",
            f"Hi, I am {name} (SIN: {sin}). I want to make a one-time lump-sum payment toward my principal in order to reduce the outstanding balance and cut down on the total interest I will pay over the remaining life of the mortgage. Can you confirm my current balance, tell me what the annual prepayment limit is under my mortgage terms, and show me the specific impact on my payoff timeline and interest charges if I were to make a lump-sum contribution of fifteen thousand and twenty-five thousand dollars respectively?",
            f"Hello, this is {name}, my SIN is {sin}. I received an inheritance this year and I am planning to put a significant portion toward my mortgage as a lump-sum payment to reduce my debt quickly. Before I proceed, I need to understand how much additional principal I can contribute without triggering a prepayment penalty, when the optimal time to make the contribution is relative to my anniversary date, and what the projected savings in interest and reduction in amortization would be if I apply the full allowable amount.",
            f"I am {name}, SIN {sin}. I want to fully understand the rules and benefits around making a large one-time lump-sum payment on my mortgage this year. Specifically, I need to know the maximum lump-sum amount allowed under my current contract, whether there is a window or deadline for making the contribution, and what the projected impact would be on my total interest cost and remaining amortization period if I make the maximum allowed contribution.",
            f"This is {name}, my SIN is {sin}. My spouse and I have been saving for a while and we are ready to make a significant lump-sum contribution to reduce our outstanding mortgage principal. Could you please pull up my account, confirm the maximum lump-sum payment I can make without penalty under my prepayment privileges, and calculate the difference in total interest paid and remaining amortization period if we apply this payment now versus waiting until next year?",
        ],
        "rates": [
            f"My name is {name} and my SIN is {sin}. I would like a detailed review of my current interest rate situation. Could you pull up my mortgage account and tell me what my current interest rate is, whether it is fixed or variable, how it compares to the best rates being offered in the market today, and what the total projected interest I will pay between now and the end of my current term will be if nothing changes?",
            f"Hi, I am {name} (SIN: {sin}). I want a comprehensive picture of my mortgage interest costs. Could you look at my account and provide my current interest rate, the total interest I have paid to date since origination, the estimated total interest remaining until payoff, and a side-by-side comparison of what I would pay in interest if I were moved to the best available rate product offered today?",
            f"Hello, this is {name}, my SIN is {sin}. I have been on the same mortgage product for a few years and I am not sure if my current interest rate is still competitive given how the market has moved. Could you please review my account, confirm my current interest rate and product type, explain how the rate was set at origination, and compare it against the current best available rates so I can make an informed decision about whether to make any changes?",
            f"I am {name}, SIN {sin}. I am in the process of preparing my annual household budget and I need a clear picture of my mortgage interest costs for planning purposes. Could you please confirm my current interest rate, calculate the total annual interest charge based on my current outstanding balance, and show me the annual interest savings I would achieve if today's best available rate were applied to my mortgage instead of my current rate?",
            f"This is {name}, my SIN is {sin}. I am trying to decide between renewing at a fixed rate versus switching to a variable rate product at my next renewal and I need accurate data to make that decision. Could you please review my current mortgage details — specifically confirming my current interest rate, the remaining term, and the current best available fixed and variable rates — so I can properly compare the total interest cost and monthly payment implications of each option?",
        ],
        "missed_payment": [
            f"My name is {name} and my SIN is {sin}. I have been dealing with a sudden and unexpected job loss and I am genuinely worried that I may miss a payment in the coming weeks. I want to fully understand the consequences of a missed mortgage payment — specifically what late fees will be charged, how quickly the account moves toward default, how it will affect my credit report, and what I need to do immediately to protect my standing with the lender and explore any available options.",
            f"Hi, I am {name} (SIN: {sin}). My financial situation has deteriorated temporarily and there is a real possibility I will need to miss a payment or two over the next couple of months. Could you advise me on the specific late payment penalty that would apply if I miss a payment, how long the grace period is before a late fee is triggered, how the lender handles missed payments in terms of credit reporting, and what steps I can take right now to avoid the most serious consequences?",
            f"Hello, this is {name}, my SIN is {sin}. I recently missed a mortgage payment due to an unexpected banking error and I am concerned about the late payment fee that may have been applied and any negative consequences for my account standing. Could you please look up my account, confirm whether a late payment has been recorded, tell me exactly what penalty charges are currently on the account, and advise me on how to resolve this situation and prevent it from affecting my credit?",
            f"I am {name}, SIN {sin}. Due to a medical emergency I was unable to make my last mortgage payment and I now need to understand the full repercussions of this missed payment. Could you please review my account, confirm the current status, itemize any penalties or fees that have been applied, explain the timeline before a single missed payment escalates to something more serious such as a notice of default, and let me know what my options are to bring the account current?",
            f"This is {name}, my SIN is {sin}. I am going through a financially difficult period and I need to honestly assess what consequences I will face if I miss my upcoming mortgage payment. Specifically I need to know the grace period duration, the late fee structure, exactly how and when a missed payment gets reported to the credit bureaus, and what remedies are available so I can decide whether to pursue a short-term borrowing option or request some form of payment assistance from the lender.",
        ],
        "pre_approval": [
            f"My name is {name} and my Social Insurance Number is {sin}. I recently submitted my pre-approval application and I have not yet received any update on its status. I am actively searching for a home and I need to know the outcome of my pre-approval — whether it has been reviewed, what the decision is, what maximum mortgage amount I qualify for, and how long the approval remains valid so I can move forward confidently when I find the right property.",
            f"Hi, I am {name} (SIN: {sin}). I applied for pre-approval about a week ago and I am eager to move forward with my home search. Could you please check the status of my pre-approval application, confirm whether the income verification and credit check have been completed, let me know the outcome and the maximum approved amount, and advise me on anything I still need to submit to finalize and activate the pre-approval letter?",
            f"Hello, this is {name}, my SIN is {sin}. I have submitted my pre-approval request and I want to fully understand the process from here. Could you review my pre-approval application status, let me know which documents have been verified and which are still outstanding, give me a clear timeline for when the credit check will be conducted, and tell me realistically when I should expect to receive the pre-approval letter with the confirmed maximum mortgage amount?",
            f"I am {name}, SIN {sin}. I am a first-time homebuyer who has recently gone through the pre-approval application process and I am not entirely clear on what happens at each stage. Could you look up my pre-approval file, tell me exactly where the application currently stands in the review process, confirm whether my employment and income verification is complete, let me know my approved amount and any conditions attached to it, and explain how long the pre-approval is valid before I would need to reapply?",
            f"This is {name}, my SIN is {sin}. I am working toward getting a pre-approval and I want to make sure I understand everything that is required to reach a successful outcome. Could you check my application status, confirm all the documentation still needed including income verification and credit authorization, let me know what the minimum credit score threshold is for the product I am applying for, and give me an honest assessment of how my profile looks based on what has been submitted so far?",
        ],
        "application": [
            f"My name is {name} and my SIN is {sin}. I submitted my formal mortgage loan application about two weeks ago after my offer on a property was conditionally accepted and I have been waiting for an update. I am on a tight timeline because my conditional offer expires soon and my real estate agent needs to know whether to request an extension. Could you please look up the status of my loan application, confirm whether all required income documentation has been received and verified, and tell me where the underwriting review currently stands?",
            f"Hi, I am {name} (SIN: {sin}). My conditional purchase offer is expiring in a matter of days and I urgently need to know the current status of my mortgage application. Could you please check whether all the required documents for my loan application have been received and processed, whether the income verification step has been completed by the underwriting team, and advise me on when I can realistically expect a final approval decision so I can inform my lawyer and real estate agent?",
            f"Hello, this is {name}, my SIN is {sin}. I submitted my loan application along with all supporting documents including an employment confirmation letter, two years of tax returns, recent pay stubs, and bank statements. I am following up to confirm that all of those materials were received successfully and to find out what the next steps are. Could you review my application file and give me a complete status update, including whether anything is outstanding or requires clarification?",
            f"I am {name}, SIN {sin}. I would like to track the detailed progress of my mortgage application and understand exactly where each step of the review stands. I submitted all the requested documentation last week and I need to know whether the income verification has been completed, whether the credit check has been run, what stage the underwriting review is at, and whether there are any outstanding conditions or missing items that could delay the final approval decision.",
            f"This is {name}, my SIN is {sin}. I want to understand precisely where I am in the mortgage application process and what I still need to do to move things forward. Could you please pull up my loan application, give me the current status of each review step — document verification, income assessment, credit evaluation, and underwriting — and advise me on the expected timeline to receive a binding approval decision so I can coordinate my closing date with the vendor?",
        ],
        "refinance": [
            f"My name is {name} and my SIN is {sin}. My fixed-rate mortgage term is expiring in approximately six months and I am seriously evaluating whether to refinance to a new product rather than simply renewing at the posted renewal rate. I have built up significant equity over the years and I am interested in both securing a better interest rate and the possibility of accessing some of that equity for home improvements. Could you please review my account and outline in detail what refinancing options are available to me, including any prepayment penalties that would apply for breaking my current term early?",
            f"Hi, I am {name} (SIN: {sin}). I have been watching mortgage rates closely and I believe I may be able to significantly improve my financial position by refinancing rather than waiting for my current term to end. Could you please look at my current mortgage and provide a full analysis that compares my existing rate and remaining payments against what I would pay under a refinanced product, including a breakdown of all closing costs and a calculation of the long-term savings after those costs are factored in?",
            f"Hello, this is {name}, my SIN is {sin}. I am interested in refinancing my mortgage specifically to consolidate some higher-interest personal debt into a single lower-rate product secured against my home. I have good equity in the property and stable employment income. Could you review my current mortgage details and advise me on the refinancing options that would allow me to access a portion of my equity, the rate I would likely qualify for on the new consolidated mortgage, and the net impact on my monthly obligations compared to what I am currently paying across all debts?",
            f"I am {name}, SIN {sin}. I have been with my current lender for several years and I believe I may be able to get materially better terms by refinancing my mortgage now. My existing rate feels high relative to current market offerings and I want to understand whether a mortgage renewal at revised terms or an outright refinance represents the better financial decision. Could you analyze my current mortgage, compare my existing rate and amortization against current market options, and show me a proper break-even analysis for a refinance including all associated penalties and transaction costs?",
            f"This is {name}, my SIN is {sin}. I am planning a significant home renovation project and I would like to fund it by accessing my accumulated home equity through a refinancing arrangement rather than taking out a separate personal loan at a much higher interest rate. Could you please look at my current mortgage balance and the estimated property value, explain how much equity I could realistically access through a refinance, what interest rate I would qualify for on the new mortgage, and how the refinancing would affect my monthly payment and total interest cost over the remaining amortization?",
        ],
        "hardship": [
            f"My name is {name} and my SIN is {sin}. I am going through a very difficult financial period following a sudden and unexpected layoff from my job of many years. I am genuinely worried about my ability to maintain my mortgage payments in the coming months and I need to understand urgently what hardship programs or payment deferral options might be available to me, what the eligibility requirements are, and how I should apply as quickly as possible before I miss my first payment.",
            f"Hi, I am {name} (SIN: {sin}). I have been experiencing serious financial difficulties following an unexpected medical situation that has required me to take extended unpaid leave from work. I am looking for any form of payment restructuring or temporary financial assistance that the lender can offer. Could you review my account, explain what hardship programs I might qualify for, describe how a deferral arrangement would work and affect my overall mortgage, and walk me through the steps to apply as quickly as possible?",
            f"Hello, this is {name}, my SIN is {sin}. My household income has dropped significantly over the past several months due to circumstances beyond my control, including a business closure that eliminated my primary income source. I am struggling to keep up with my regular mortgage payments and I am reaching out before I fall behind to ask about available hardship programs, whether payment deferral is an option, and what documentation I would need to provide to qualify for any form of temporary payment assistance.",
            f"I am {name}, SIN {sin}. Due to a sudden and severe financial hardship I am at risk of not being able to meet my mortgage obligations in the near future. I am proactively seeking to understand the options available through the lender's hardship assistance programs — specifically whether I might qualify for deferred payments, a temporary interest-only payment arrangement, a loan modification, or an extended repayment plan — and what documentation I would need to submit with my application.",
            f"This is {name}, my SIN is {sin}. I am facing temporary but serious financial difficulties following a divorce that has significantly reduced my household income. I want to explore whether I qualify for any payment deferral or restructuring options under the lender's hardship programs before I end up in arrears on my mortgage. Could you review my account, explain the available assistance programs and their respective eligibility requirements, advise me on which one best fits my situation, and tell me how long the assistance period can last and what happens to my mortgage at the end of it?",
        ],
        "insurance": [
            f"My name is {name} and my SIN is {sin}. I have been receiving correspondence from my home insurance provider about an upcoming premium change and I want to make sure my mortgage escrow account is properly set up and funded to handle the adjustment. Could you please review my escrow account balance, confirm the current monthly escrow contribution being collected, and advise me on whether the projected insurance premium increase will require an adjustment to my escrow payment and by how much?",
            f"Hi, I am {name} (SIN: {sin}). I recently switched to a new home insurance provider and I need to confirm that the updated policy details have been properly received and recorded in my mortgage account. Could you verify that my new homeowners insurance policy is on file, confirm that the coverage level meets the minimum requirements specified in my mortgage agreement, and let me know whether the change in insurance premium will result in a modification to my monthly escrow payment?",
            f"Hello, this is {name}, my SIN is {sin}. I am trying to fully understand how the escrow portion of my monthly mortgage payment is calculated and managed. Could you please pull up my account and explain in detail how my property tax and homeowners insurance contributions are being collected through the escrow arrangement, what my current escrow account balance is, when the next annual escrow analysis is scheduled, and whether I can expect any change to my monthly payment after that analysis?",
            f"I am {name}, SIN {sin}. I just received a notice from my municipality that my property taxes are increasing substantially next year and I want to understand how that will flow through to my monthly mortgage payment via the escrow adjustment process. Could you review my escrow account, confirm the current property tax amount being collected monthly, calculate what my new monthly payment would be after the escrow is adjusted upward to reflect the higher tax bill, and tell me when that change would take effect?",
            f"This is {name}, my SIN is {sin}. I have some questions about the insurance requirements tied to my mortgage and I also want to review my current escrow account setup. Could you confirm what mortgage default insurance coverage is currently in place on my loan, verify that my homeowners insurance policy on file meets the lender's minimum requirements, provide my current escrow balance, and advise me on how any changes to my insurance arrangements might affect my monthly payment going forward?",
        ],
    }

    templates = query_templates.get(query_type, query_templates["balance"])
    return random.choice(templates)


class FinancialQueryInput(BaseModel):
    """Input schema for financial query tools."""
    userQuery: str = Field(description="The user's financial query or question")


class BalanceTool(BaseTool):
    """Tool for handling balance and payment date inquiries."""
    name = "balance_tool"
    description = """Use this tool when the user asks about:
    - Current loan balance
    - Final payment dates
    - Payment schedules
    - Remaining balance information"""
    args_schema = FinancialQueryInput

    def _run(self, userQuery: str) -> str:
        # Process balance-related queries
        if os.getenv("DEBUG_MODE", "false").lower() == "true":
            print(f"🔧 DEBUG: BalanceTool._run called with query: {userQuery}")
            print(f"🔧 DEBUG: About to return balance result...")
        
        # Extract SIN number from user query
        sin_number = extract_sin_number(userQuery)
        print(f"🔧 DEBUG: Extracted SIN: {sin_number}")
        
        # TODO: Add actual processing logic here
        # Example of what real implementation might look like:
        # 1. Parse user query for account/loan identifiers
        # 2. Call external API or database to get balance using SIN
        # 3. Format and return real data
        
        # Simulate some business logic
        import random
        simulated_balance = random.randint(50000, 500000)
        simulated_next_payment = "March 15, 2026"
        
        result = f"BALNC: [SIN: {sin_number}] Current loan balance: ${simulated_balance:,}. Next payment due: {simulated_next_payment}"
        print(f"🔧 DEBUG: Returning result: {result}")
        return result
    
    async def _arun(self, userQuery: str) -> str:
        return self._run(userQuery)


class PaymentIncreaseTool(BaseTool):
    """Tool for handling payment increase scenarios."""
    name = "payment_increase_tool"
    description = """Use this tool when the user asks about:
    - Increasing monthly payments
    - Payment increase options
    - Scenarios for different payment amounts
    - Effects of increased payments on loan term"""
    args_schema = FinancialQueryInput

    def _run(self, userQuery: str) -> str:
        print(f"🔧 DEBUG: PaymentIncreaseTool._run called with query: {userQuery}")
        print(f"🔧 DEBUG: About to return payment increase result...")
        
        # Extract SIN number from user query
        sin_number = extract_sin_number(userQuery)
        print(f"🔧 DEBUG: Extracted SIN: {sin_number}")
        
        # TODO: Add actual processing logic here
        # Example: Parse user query for payment amounts, calculate scenarios
        
        # Simulate some business logic
        import random
        current_payment = random.randint(1200, 3500)
        increase_amount = random.randint(100, 500)
        new_payment = current_payment + increase_amount
        years_saved = round(random.uniform(2.5, 8.5), 1)
        interest_saved = random.randint(15000, 85000)
        
        result = f"PAYUP: [SIN: {sin_number}] Current payment: ${current_payment:,}. Proposed increase: +${increase_amount:,} = ${new_payment:,}/month. This would save {years_saved} years and ${interest_saved:,} in interest."
        print(f"🔧 DEBUG: Returning result: {result}")
        return result
    
    async def _arun(self, userQuery: str) -> str:
        return self._run(userQuery)


class LumpSumTool(BaseTool):
    """Tool for handling lump-sum payment inquiries."""
    name = "lump_sum_tool"
    description = """Use this tool when the user asks about:
    - Making lump-sum payments
    - Maximum contribution amounts
    - Effects of lump-sum payments on loan
    - One-time payment options"""
    args_schema = FinancialQueryInput

    def _run(self, userQuery: str) -> str:
        print(f"🔧 DEBUG: LumpSumTool._run called with query: {userQuery}")
        print(f"🔧 DEBUG: About to return lump-sum payment result...")
        
        # Extract SIN number from user query
        sin_number = extract_sin_number(userQuery)
        print(f"🔧 DEBUG: Extracted SIN: {sin_number}")
        
        # TODO: Add actual processing logic here
        # Example: Calculate impact of lump-sum payments on loan term and interest
        
        # Simulate some business logic
        import random
        suggested_amount = random.randint(5000, 50000)
        current_balance = random.randint(150000, 400000)
        years_saved = round(random.uniform(1.2, 4.8), 1)
        interest_saved = random.randint(8000, 45000)
        new_payoff_date = "September 2029" if years_saved > 3 else "March 2031"
        
        result = f"LUMPD: [SIN: {sin_number}] Lump-sum payment of ${suggested_amount:,} would reduce your ${current_balance:,} balance, saving {years_saved} years and ${interest_saved:,} in interest. New payoff date: {new_payoff_date}."
        print(f"🔧 DEBUG: Returning result: {result}")
        return result
    
    async def _arun(self, userQuery: str) -> str:
        return self._run(userQuery)


class InterestRateTool(BaseTool):
    """Tool for handling interest rate inquiries."""
    name = "interest_rate_tool"
    description = """Use this tool when the user asks about:
    - Current interest rates
    - Total interest payments
    - Rate comparisons
    - Interest calculations
    - Fixed vs variable rates"""
    args_schema = FinancialQueryInput

    def _run(self, userQuery: str) -> str:
        print(f"🔧 DEBUG: InterestRateTool._run called with query: {userQuery}")
        print(f"🔧 DEBUG: About to return interest rate result...")
        
        # Extract SIN number from user query
        sin_number = extract_sin_number(userQuery)
        print(f"🔧 DEBUG: Extracted SIN: {sin_number}")
        
        # TODO: Add actual processing logic here
        # Example: Get current market rates, compare with user's rate
        
        # Simulate some business logic
        import random
        current_rate = round(random.uniform(3.25, 7.85), 2)
        market_rate = round(random.uniform(3.15, 7.95), 2)
        total_interest = random.randint(85000, 275000)
        rate_type = random.choice(["Fixed 30-year", "Fixed 15-year", "5/1 ARM", "7/1 ARM"])
        
        comparison = "below" if current_rate < market_rate else "above" if current_rate > market_rate else "at"
        
        result = f"RATES: [SIN: {sin_number}] Your current {rate_type} rate is {current_rate}% ({comparison} market average of {market_rate}%). Total interest over loan term: ${total_interest:,}."
        print(f"🔧 DEBUG: Returning result: {result}")
        return result
    
    async def _arun(self, userQuery: str) -> str:
        return self._run(userQuery)


class MissedPaymentTool(BaseTool):
    """Tool for handling missed payment and penalty inquiries."""
    name = "missed_payment_tool"
    description = """Use this tool when the user asks about:
    - Missed or late payments
    - Payment penalties
    - Consequences of non-payment
    - Payment assistance programs"""
    args_schema = FinancialQueryInput

    def _run(self, userQuery: str) -> str:
        print(f"🔧 DEBUG: MissedPaymentTool._run called with query: {userQuery}")
        print(f"🔧 DEBUG: About to return missed payment result...")
        
        # Extract SIN number from user query
        sin_number = extract_sin_number(userQuery)
        print(f"🔧 DEBUG: Extracted SIN: {sin_number}")
        
        # TODO: Add actual processing logic here
        # Example: Calculate late fees, check payment history, offer assistance
        
        # Simulate some business logic
        import random
        days_late = random.randint(1, 45)
        late_fee = random.choice([25, 50, 75, 95, 125])
        grace_period = random.choice([10, 15, 30])
        next_payment_due = "March 1, 2026"
        
        if days_late <= grace_period:
            status = "within grace period - no fee assessed"
        else:
            status = f"${late_fee} late fee applied"
        
        result = f"MISSP: [SIN: {sin_number}] Payment is {days_late} days late ({status}). Next payment due: {next_payment_due}. Contact us within 10 days to discuss payment assistance options."
        print(f"🔧 DEBUG: Returning result: {result}")
        return result
    
    async def _arun(self, userQuery: str) -> str:
        return self._run(userQuery)


class PreApprovalTool(BaseTool):
    """Tool for handling pre-approval process inquiries."""
    name = "pre_approval_tool"
    description = """Use this tool when the user asks about:
    - Pre-approval status
    - Pre-approval process
    - Required documents for pre-approval
    - Pre-approval timelines"""
    args_schema = FinancialQueryInput

    def _run(self, userQuery: str) -> str:
        print(f"🔧 DEBUG: PreApprovalTool._run called with query: {userQuery}")
        print(f"🔧 DEBUG: About to return pre-approval result...")
        
        # Extract SIN number from user query
        sin_number = extract_sin_number(userQuery)
        print(f"🔧 DEBUG: Extracted SIN: {sin_number}")
        
        # TODO: Add actual processing logic here
        # Example: Check credit requirements, income verification, documentation needed
        
        # Simulate some business logic
        import random
        max_approval = random.randint(200000, 800000)
        credit_score_req = random.choice([620, 640, 660, 680, 700])
        processing_time = random.choice(["24-48 hours", "2-3 business days", "3-5 business days"])
        documents_needed = random.choice([
            "W-2s, pay stubs, bank statements",
            "Tax returns, employment verification, asset documentation",
            "Income documentation, credit authorization, property information"
        ])
        
        result = f"PREAP: [SIN: {sin_number}] Pre-approval available up to ${max_approval:,} (min. credit score: {credit_score_req}). Processing time: {processing_time}. Required documents: {documents_needed}."
        print(f"🔧 DEBUG: Returning result: {result}")
        return result
    
    async def _arun(self, userQuery: str) -> str:
        return self._run(userQuery)


class ApplicationTool(BaseTool):
    """Tool for handling loan application process inquiries."""
    name = "application_tool"
    description = """Use this tool when the user asks about:
    - Loan application process
    - Required documents
    - Income verification
    - Credit check procedures
    - Application timelines"""
    args_schema = FinancialQueryInput

    def _run(self, userQuery: str) -> str:
        print(f"🔧 DEBUG: ApplicationTool._run called with query: {userQuery}")
        print(f"🔧 DEBUG: About to return application result...")
        
        # Extract SIN number from user query
        sin_number = extract_sin_number(userQuery)
        print(f"🔧 DEBUG: Extracted SIN: {sin_number}")
        
        # TODO: Add actual processing logic here
        # Example: Track application status, required documents, next steps
        
        # Simulate some business logic
        import random
        app_status = random.choice(["In Review", "Pending Documentation", "Underwriting", "Approved - Pending Conditions", "Ready to Close"])
        app_number = f"LN{random.randint(100000, 999999)}"
        estimated_close = random.choice(["March 15, 2026", "March 22, 2026", "April 5, 2026", "April 12, 2026"])
        
        if app_status == "Pending Documentation":
            next_step = "Submit requested income verification documents"
        elif app_status == "Underwriting":
            next_step = "Await underwriter review (3-5 business days)"
        elif app_status == "Ready to Close":
            next_step = "Schedule closing appointment"
        else:
            next_step = "Continue monitoring application progress"
        
        result = f"APPLI: [SIN: {sin_number}] Application #{app_number} status: {app_status}. Estimated closing: {estimated_close}. Next step: {next_step}."
        print(f"🔧 DEBUG: Returning result: {result}")
        return result
    
    async def _arun(self, userQuery: str) -> str:
        return self._run(userQuery)


class RefinancingTool(BaseTool):
    """Tool for handling refinancing inquiries."""
    name = "refinancing_tool"
    description = """Use this tool when the user asks about:
    - Refinancing options
    - Debt consolidation
    - Home renovations financing
    - Accessing home equity
    - Refinancing benefits"""
    args_schema = FinancialQueryInput

    def _run(self, userQuery: str) -> str:
        print(f"🔧 DEBUG: RefinancingTool._run called with query: {userQuery}")
        print(f"🔧 DEBUG: About to return refinancing result...")
        
        # Extract SIN number from user query
        sin_number = extract_sin_number(userQuery)
        print(f"🔧 DEBUG: Extracted SIN: {sin_number}")
        
        # TODO: Add actual processing logic here
        # Example: Compare current vs. new rates, calculate break-even, assess equity
        
        # Simulate some business logic
        import random
        current_rate = round(random.uniform(4.5, 8.2), 2)
        new_rate = round(current_rate - random.uniform(0.5, 2.0), 2)
        monthly_savings = random.randint(150, 650)
        closing_costs = random.randint(3500, 8500)
        break_even_months = max(1, int(closing_costs / max(monthly_savings, 1)))
        home_value = random.randint(300000, 750000)
        equity_percent = random.randint(15, 45)
        
        result = f"REFIN: [SIN: {sin_number}] Refinance from {current_rate}% to {new_rate}% could save ${monthly_savings:,}/month. Closing costs: ${closing_costs:,} (break-even: {break_even_months} months). Home value: ${home_value:,} ({equity_percent}% equity)."
        print(f"🔧 DEBUG: Returning result: {result}")
        return result
    
    async def _arun(self, userQuery: str) -> str:
        return self._run(userQuery)


class HardshipTool(BaseTool):
    """Tool for handling financial hardship and assistance inquiries."""
    name = "hardship_tool"
    description = """Use this tool when the user asks about:
    - Financial difficulties
    - Payment deferrals
    - Payment restructuring
    - Hardship programs
    - Temporary payment assistance"""
    args_schema = FinancialQueryInput

    def _run(self, userQuery: str) -> str:
        print(f"🔧 DEBUG: HardshipTool._run called with query: {userQuery}")
        print(f"🔧 DEBUG: About to return hardship assistance result...")
        
        # Extract SIN number from user query
        sin_number = extract_sin_number(userQuery)
        print(f"🔧 DEBUG: Extracted SIN: {sin_number}")
        
        # TODO: Add actual processing logic here
        # Example: Assess hardship situation, available assistance programs, eligibility
        
        # Simulate some business logic
        import random
        program_options = [
            "3-month payment deferral",
            "6-month reduced payment plan",
            "Loan modification program",
            "Temporary forbearance (90 days)",
            "Extended repayment plan"
        ]
        selected_option = random.choice(program_options)
        eligibility_req = random.choice([
            "Income documentation required",
            "Hardship letter and financial statements needed",
            "Employment verification required",
            "Complete financial review necessary"
        ])
        contact_deadline = "within 10 business days"
        
        result = f"HELPD: [SIN: {sin_number}] Available assistance: {selected_option}. Eligibility: {eligibility_req}. Please contact our hardship department {contact_deadline} to begin the process."
        print(f"🔧 DEBUG: Returning result: {result}")
        return result
    
    async def _arun(self, userQuery: str) -> str:
        return self._run(userQuery)


class InsuranceTool(BaseTool):
    """Tool for handling insurance and escrow inquiries."""
    name = "insurance_tool"
    description = """Use this tool when the user asks about:
    - Property tax escrow
    - Home insurance requirements
    - Mortgage default insurance
    - Insurance changes affecting payments
    - Escrow account management"""
    args_schema = FinancialQueryInput

    def _run(self, userQuery: str) -> str:
        print(f"🔧 DEBUG: InsuranceTool._run called with query: {userQuery}")
        print(f"🔧 DEBUG: About to return insurance/escrow result...")
        
        # Extract SIN number from user query
        sin_number = extract_sin_number(userQuery)
        print(f"🔧 DEBUG: Extracted SIN: {sin_number}")
        
        # TODO: Add actual processing logic here
        # Example: Check escrow balances, insurance requirements, policy details
        
        # Simulate some business logic
        import random
        escrow_balance = random.randint(1200, 4500)
        monthly_escrow = random.randint(280, 650)
        insurance_premium = random.randint(800, 2400)
        property_tax = random.randint(2400, 8500)
        next_analysis_date = random.choice(["June 2026", "July 2026", "August 2026"])
        
        insurance_status = random.choice([
            "Current policy on file",
            "Policy renewal required by March 31st",
            "Updated declaration page needed",
            "Premium increase detected - escrow adjustment pending"
        ])
        
        result = f"INSUR: [SIN: {sin_number}] Escrow balance: ${escrow_balance:,}. Monthly escrow: ${monthly_escrow:,} (Insurance: ${insurance_premium:,}/year, Taxes: ${property_tax:,}/year). Status: {insurance_status}. Next analysis: {next_analysis_date}."
        print(f"🔧 DEBUG: Returning result: {result}")
        return result
    
    async def _arun(self, userQuery: str) -> str:
        return self._run(userQuery)


class FinancialChatAgent:
    """
    LangChain-based agent for handling financial chat inquiries using tools.
    """
    
    def __init__(self):
        """Initialize the financial chat agent."""
        self.llm = self._setup_llm()
        self.tools = self._setup_tools()
        self.agent = self._create_agent()
        self.agent_executor = self._create_executor()
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )

    def _setup_llm(self) -> AzureChatOpenAI:
        """Setup Azure OpenAI LLM for the agent."""
        try:
            return AzureChatOpenAI(
                azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                # api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01"),
                api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
                # deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-35-turbo"),
                deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
                temperature=0.7,
                max_tokens=1000
            )
        except Exception as e:
            print(f"Warning: Could not setup Azure OpenAI: {e}")
            # Fallback to mock LLM for testing
            return None

    def _setup_tools(self) -> List[BaseTool]:
        """Setup all available tools for the agent."""
        return [
            BalanceTool(),
            PaymentIncreaseTool(),
            LumpSumTool(),
            InterestRateTool(),
            MissedPaymentTool(),
            PreApprovalTool(),
            ApplicationTool(),
            RefinancingTool(),
            HardshipTool(),
            InsuranceTool()
        ]

    def _create_agent(self):
        """Create the OpenAI functions agent - simplified version."""
        if not self.llm:
            return None
            
        # Create the prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a helpful financial advisor assistant specializing in mortgages and loans.
            
            You have access to various tools that can help answer specific types of financial questions.
            Always use the most appropriate tool based on the user's query.
            
            Available tools cover:
            - Balance and payment information
            - Payment increases and modifications
            - Lump-sum payments
            - Interest rates and calculations
            - Missed payments and penalties
            - Pre-approval processes
            - Loan applications
            - Refinancing options
            - Financial hardship assistance
            - Insurance and escrow matters
            
            Analyze the user's question carefully and select the most relevant tool to provide accurate assistance."""),
            
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
            MessagesPlaceholder(variable_name="chat_history", optional=True)
        ])

        try:
            # Simplified agent creation for compatibility
            return {"prompt": prompt, "tools": self.tools, "llm": self.llm}
        except Exception as e:
            print(f"Error creating agent: {e}")
            return None

    def _create_executor(self) -> Optional[Dict]:
        """Create the agent executor - simplified version."""
        if not self.agent or not isinstance(self.agent, dict):
            return None
            
        try:
            # Simplified executor creation
            return {
                "tools": self.tools,
                "llm": self.llm,
                "prompt": self.agent.get("prompt"),
                "verbose": True
            }
        except Exception as e:
            print(f"Error creating executor: {e}")
            return None

    def chat(self, user_input: str) -> Dict[str, Any]:
        """
        Process user input through the agent.
        
        Args:
            user_input (str): User's query or message
            
        Returns:
            dict: Dictionary containing agent response, tool used, and parameters
        """
        if not self.agent_executor:
            # Fallback response when agent is not available
            fallback_response = self._fallback_response(user_input)
            tool_info = self._classify_user_query(user_input)
            
            # Try to execute the tool even without LLM for testing
            tool_result = "No tool execution (agent not available)"
            if tool_info["tool_name"] != "general_inquiry":
                for tool in self.tools:
                    if hasattr(tool, 'name') and tool.name == tool_info["tool_name"]:
                        try:
                            tool_result = tool._run(user_input)
                        except Exception as e:
                            tool_result = f"Tool execution failed: {str(e)}"
                        break
            
            return {
                "response": fallback_response,
                "tool_used": tool_info["tool_name"],
                "parameters": {"userQuery": user_input},
                "tool_description": tool_info["description"],
                "tool_return": tool_result
            }
        
        try:
            # Simplified processing - use classification and direct tool execution
            tool_info = self._classify_user_query(user_input)
            
            # Try to find and execute the appropriate tool
            selected_tool = None
            tool_result = "No tool executed"
            
            for tool in self.tools:
                if hasattr(tool, 'name') and tool.name == tool_info["tool_name"]:
                    selected_tool = tool
                    break
            
            if selected_tool and hasattr(selected_tool, '_run'):
                # Execute the tool with the user input
                try:
                    tool_result = selected_tool._run(user_input)
                    # Remove the processing message, keep only the prefix code
                    # if ": Processing" in tool_result:
                    #     tool_result = tool_result.split(": Processing")[0]
                    response = f"I'll help you with that. {tool_result}"
                except Exception as tool_error:
                    print(f"Tool execution error: {tool_error}")
                    tool_result = f"Tool execution failed: {str(tool_error)}"
                    response = self._fallback_response(user_input)
            else:
                # No specific tool found, use fallback
                response = self._fallback_response(user_input)
                tool_result = "No matching tool found"
            
            return {
                "response": response,
                "tool_used": tool_info.get("tool_name", "unknown"),
                "parameters": {"userQuery": user_input},
                "tool_description": tool_info.get("description", "No tool description available"),
                "tool_return": tool_result
            }
        
        except Exception as e:
            print(f"Error processing chat: {e}")
            fallback_response = self._fallback_response(user_input)
            tool_info = self._classify_user_query(user_input)
            return {
                "response": fallback_response,
                "tool_used": tool_info["tool_name"],
                "parameters": {"userQuery": user_input, "error": str(e)},
                "tool_description": tool_info["description"],
                "tool_return": f"Error occurred: {str(e)}"
            }

    def _classify_user_query(self, user_input: str) -> Dict[str, str]:
        """
        Manually classify user query to determine appropriate tool.
        
        Args:
            user_input: The user's query string
            
        Returns:
            dict: Tool classification information
        """
        user_lower = user_input.lower()
        print(f"🔍 DEBUG: Classifying query: '{user_input}'")
        print(f"🔍 DEBUG: Lowercase version: '{user_lower}'")
        
        # Define keyword mappings to tools - ORDER MATTERS! More specific patterns first
        tool_mappings = [
            # Pre-approval - check first as it's very specific - ADD MISSING VARIATIONS AND SHOPPING TERMS
            (["pre-approval", "preapproval", "pre approval", "pre-approved", "preapproved", "been approved", "got approved", "get approved", "qualify for", "qualification", "shopping for mortgage", "looking at loan", "considering mortgage", "mortgage shopping"], "pre_approval_tool", "Function that handles the pre-approval process, with parameters extracted from the user query. Topics include eligibility criteria, required documents, and application steps."),
            
            # Application process - specific multi-word patterns - ADD VERIFICATION TERMS AND RENEWAL DOCS
            (["application status", "loan application", "apply for", "applying for", "submit application", "application documents", "income verification", "credit check", "document submission", "verification process", "documents i need", "what documents", "paperwork needed", "renewal documents"], "application_tool", "Function that handles the loan application process, with parameters extracted from the user query. Topics include application steps, required documents, and approval timelines."),
            
            # Refinancing - check before general rate questions - ADD RENEWAL TERMS
            (["refinance", "refi", "consolidation", "refinancing rate", "should i refinance", "renew mortgage", "renewing mortgage", "mortgage renewal", "renewal options", "renew my mortgage", "mortgage term", "end of term", "new rate offers", "rate offers", "breaking my mortgage", "break my mortgage", "prepayment penalty", "prepayment penalties", "interest rate differential", "ird", "breaking mortgage early", "break mortgage early", "early termination", "mortgage penalty"], "refinancing_tool", "Function that handles refinancing options, with parameters extracted from the user query. Topics include refinancing eligibility, rate comparison, and application process."),
            
            # Hardship - very specific context - ADD MORE HARDSHIP VARIATIONS
            (["hardship", "financial difficulty", "financial difficulties", "tough situation", "difficult situation", "can't pay", "can't make", "can't make payments", "won't be able to make", "won't be able to pay", "unable to make payments", "struggling with payments", "struggling to make", "struggling financially", "payment help", "defer payment", "forbearance", "facing difficulties", "financial troubles", "can't afford", "unable to pay"], "hardship_tool", "Function that handles financial hardship assistance, with parameters extracted from the user query. Topics include deferment options, payment plans, and eligibility criteria."),
            
            # Lump sum - specific payment type (moved before missed payments for priority)
            (["lump sum", "lump-sum", "one-time payment", "extra principal", "additional principal", "bulk payment", "large payment"], "lump_sum_tool", "Function that handles lump-sum payment options, with parameters extracted from the user query. Topics include making additional payments, reducing principal, and calculating interest savings."),
            
            # Missed payments - specific context - MORE SPECIFIC PENALTY KEYWORDS  
            (["missed payment", "miss payment", "miss my payment", "miss these payments", "miss my payments", "what happens if i miss", "if i miss my payment", "late payment", "payment late", "late fee", "missed a payment", "behind on payments", "overdue payment", "payment penalty", "late payment penalty", "penalties will i face", "what penalties", "repercussions", "consequences", "skip payment"], "missed_payment_tool", "Function that handles missed payment penalties, with parameters extracted from the user query. Topics include late fees, penalty calculations, and payment recovery options."),
            
            # Payment increase - be more specific about payment modifications  
            (["increase payment", "increase my payment", "increase my monthly payment", "increase my regular", "increase payment to", "increase my payment by", "how much I can increase", "how much can I increase", "if I increase my payment", "pay more", "higher payment", "additional payment", "extra payment", "boost payment", "raise payment"], "payment_increase_tool", "Function that handles payment increase scenarios, with parameters extracted from the user query. Topics include increasing monthly payments, adjusting payment schedules, and calculating new payment amounts."),
            
            # Balance - prioritize balance queries over rate information
            (["loan balance", "current balance", "balance", "my balance", "owe on loan", "remaining balance", "balance left", "payoff amount", "principal balance", "final payment", "last payment", "when will i pay off", "payoff date", "final payment due", "payment schedule", "next payment", "payment due", "when is my payment", "when's my payment"], "balance_tool", "Function that handles balance and payment date inquiries, with parameters extracted from the user query. Topics include current loan balance, final payment dates, payment schedules, and remaining balance information."),
            
            # Interest rates - more specific keywords to avoid conflicts with balance queries
            (["what is my rate", "what's my rate", "what is my current interest rate", "what's my current interest rate", "current interest rate", "my current interest rate", "current rate only", "my interest rate", "my current rate", "interest rate only", "rate information", "apr only", "rate comparison", "rate quotes", "interest quotes", "rate options", "rate-lock", "lock period", "rate lock", "fixed or variable", "mortgage rates today", "best rates", "today's rates", "rate changes"], "interest_rate_tool", "Function that provides interest rate information, with parameters extracted from the user query. Topics include current rates, rate changes, and comparison of different rate options."),
            
            # Insurance and escrow - specific terms
            (["insurance", "escrow", "property tax", "homeowners insurance", "insurance premium", "escrow account", "tax escrow"], "insurance_tool", "Function that handles insurance and escrow matters, with parameters extracted from the user query. Topics include policy details, escrow accounts, and property tax information.")
        ]
        
        # Check each mapping - using more precise matching
        for keywords, tool_name, description in tool_mappings:
            print(f"🔍 DEBUG: Checking {tool_name} with keywords: {keywords}")
            for keyword in keywords:
                if keyword in user_lower:
                    print(f"✅ DEBUG: MATCH found! '{keyword}' matches {tool_name}")
                    return {
                        "tool_name": tool_name,
                        "description": description,
                        "parameters": {"userQuery": user_input}
                    }
        
        # Default fallback
        print(f"❌ DEBUG: No tool matched - falling back to general_inquiry")
        return {
            "tool_name": "general_inquiry",
            "description": "General financial inquiry", 
            "parameters": {"userQuery": user_input}
        }

    def _extract_tool_info(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract tool information from the agent response.
        
        Args:
            response: The full response from the agent executor
            
        Returns:
            dict: Tool information including name, parameters, and description
        """
        tool_info = {
            "tool_name": "no_tool_used",
            "parameters": {},
            "description": "No tool was invoked"
        }
        
        try:
            # Method 1: Check intermediate_steps (LangChain standard)
            intermediate_steps = response.get("intermediate_steps", [])
            
            if intermediate_steps:
                for step in intermediate_steps:
                    if isinstance(step, (list, tuple)) and len(step) >= 2:
                        action = step[0]  # AgentAction
                        observation = step[1]  # Tool output
                        
                        # Try different attribute names for different LangChain versions
                        tool_name = None
                        tool_input = {}
                        
                        for attr in ['tool', 'action', 'function_name']:
                            if hasattr(action, attr):
                                tool_name = getattr(action, attr)
                                break
                        
                        for attr in ['tool_input', 'action_input', 'arguments']:
                            if hasattr(action, attr):
                                tool_input = getattr(action, attr, {})
                                break
                        
                        if tool_name:
                            tool_description = self._get_tool_description(tool_name)
                            tool_info = {
                                "tool_name": tool_name,
                                "parameters": tool_input,
                                "description": tool_description,
                                "observation": observation
                            }
                            break
            
            # Method 2: Check for function calls in the response
            if tool_info["tool_name"] == "no_tool_used":
                output = response.get("output", "")
                if ":" in output and any(code in output for code in ["BALNC", "PAYUP", "LUMPD", "RATES", "MISSP", "PREAP", "APPLI", "REFIN", "HELPD", "INSUR"]):
                    # Extract tool name from output format like "BALNC: Processing..."
                    code = output.split(":")[0].strip()
                    tool_mapping = {
                        "BALNC": "balance_tool",
                        "PAYUP": "payment_increase_tool", 
                        "LUMPD": "lump_sum_tool",
                        "RATES": "interest_rate_tool",
                        "MISSP": "missed_payment_tool",
                        "PREAP": "pre_approval_tool",
                        "APPLI": "application_tool",
                        "REFIN": "refinancing_tool",
                        "HELPD": "hardship_tool",
                        "INSUR": "insurance_tool"
                    }
                    
                    if code in tool_mapping:
                        tool_name = tool_mapping[code]
                        tool_info = {
                            "tool_name": tool_name,
                            "parameters": {"userQuery": "extracted from response"},
                            "description": self._get_tool_description(tool_name)
                        }
            
        except Exception as e:
            print(f"Error extracting tool info: {e}")
        
        return tool_info

    def _get_tool_description(self, tool_name: str) -> str:
        """Get tool description by name."""
        for tool in self.tools:
            if tool.name == tool_name:
                return tool.description
        return "No description available"

    def _fallback_response(self, user_input: str) -> str:
        """Provide a fallback response when the agent is not available."""
        # Basic keyword matching for fallback
        user_lower = user_input.lower()
        
        if any(word in user_lower for word in ["balance", "payment", "owe"]):
            return "BALNC: I can help you with balance and payment information."
        elif any(word in user_lower for word in ["increase", "raise", "more"]):
            return "PAYUP: I can assist with payment increase options."
        elif any(word in user_lower for word in ["lump", "extra", "additional"]):
            return "LUMPD: I can help with lump-sum payment information."
        elif any(word in user_lower for word in ["rate", "interest"]):
            return "RATES: I can provide interest rate information."
        elif any(word in user_lower for word in ["miss", "late", "penalty"]):
            return "MISSP: I can help with missed payment inquiries."
        elif any(word in user_lower for word in ["pre-approval", "preapproval"]):
            return "PREAP: I can assist with pre-approval process."
        elif any(word in user_lower for word in ["application", "apply"]):
            return "APPLI: I can help with loan application process."
        elif any(word in user_lower for word in ["refinance", "refi"]):
            return "REFIN: I can provide refinancing information."
        elif any(word in user_lower for word in ["hardship", "difficulty", "help"]):
            return "HELPD: I can assist with financial hardship programs."
        elif any(word in user_lower for word in ["insurance", "escrow"]):
            return "INSUR: I can help with insurance and escrow matters."
        else:
            return "GENER: I'm here to help with your financial questions."

    def get_available_tools(self) -> List[str]:
        """Get list of all available tool names."""
        return [tool.name for tool in self.tools]

    def reset_conversation(self):
        """Reset the conversation memory."""
        self.memory.clear()


# Global agent instance
_agent_instance = None

def get_agent() -> FinancialChatAgent:
    """Get or create the global agent instance."""
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = FinancialChatAgent()
    return _agent_instance


def chat_with_agent(user_input: str) -> Dict[str, Any]:
    """
    Main interface function to chat with the agent.
    
    Args:
        user_input (str): User's query
        
    Returns:
        dict: Dictionary containing response, tool used, parameters, and description
    """
    agent = get_agent()
    return agent.chat(user_input)


def get_simple_response(user_input: str) -> str:
    """
    Get just the text response from the agent (for backward compatibility).
    
    Args:
        user_input (str): User's query
        
    Returns:
        str: Just the agent's text response
    """
    result = chat_with_agent(user_input)
    return result["response"]


def get_tool_summaries() -> Dict[str, str]:
    """
    Get a summary of all available tools and their purposes.
    
    Returns:
        dict: Mapping of tool names to their descriptions
    """
    agent = get_agent()
    return {
        tool.name: tool.description 
        for tool in agent.tools
    }


def get_tool(user_query: str) -> str:
    """Initialize the agent and its tools."""
    agent = get_agent()  # This will create the agent instance
    response = chat_with_agent(user_query)
    return response


def get_available_tools() -> List[Dict[str, str]]:
    """
    Get list of all available tools with their descriptions.
    
    Returns:
        List[Dict[str, str]]: List of dictionaries containing tool name and description
    """
    agent = get_agent()
    return [
        {
            "name": tool.name,
            "description": tool.description.replace('\n', ' ')
        }
        for tool in agent.tools
    ]

# Example usage and testing
if __name__ == "__main__":
    print("🤖 Financial Chat Agent with LangChain Tools")
    print("=" * 50)
    
    agent = get_agent()
    
    print("Available tools:")
    for tool_name in agent.get_available_tools():
        print(f"  - {tool_name}")
    
    print("\n💬 Starting chat session...")
    print("Type 'quit' to exit, 'reset' to clear conversation history")
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['quit', 'exit']:
                print("Goodbye! 👋")
                break
            elif user_input.lower() == 'reset':
                agent.reset_conversation()
                print("🔄 Conversation history cleared.")
                continue
            elif not user_input:
                continue
                
            result = chat_with_agent(user_input)
            print(f"Agent: {result['response']}")
            print(f"🔧 Tool Used: {result['tool_used']}")
            print(f"📝 Parameters: {result['parameters']}")
            if result.get('tool_description'):
                print(f"ℹ️  Description: {result['tool_description'][:100]}...")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"Error: {e}")


def interest_rate(userQuery: str) -> str:
    """
    Function that handles interest rate and total interest inquiries, including rate comparisons and calculations.
    Topics: Interest rates, promotional rates, rate-lock periods.
    
    Args:
        userQuery (str): User's query string
        
    Returns:
        str: 5-letter summary code
    """
    return "[RATES] Deterministic function output for interest rate inquiries"


def missed_payments(userQuery: str) -> str:
    """
    Function that handles missed payments and penalty inquiries. Used for questions about missed or late payments, payment penalties, consequences of non-payment, and payment assistance programs.
    Topic: "Borrower is unable to make the following 3 payments and asks about penalties and repercussions."
    
    Args:
        userQuery (str): User's query string
        
    Returns:
        str: 5-letter summary code
    """
    return "[MISSP] Deterministic function output for missed payments inquiries"


def pre_approval(userQuery: str) -> str:
    """
    Function that handles pre-approval process and status inquiries. Covers questions about whether pre-approval has been processed, required documents, income verification, and credit check timelines.
    Topic: "Borrower is asking whether their pre‑approval has been processed, required documents, income verification, and credit check timelines"
    
    Args:
        userQuery (str): User's query string
        
    Returns:
        str: 5-letter summary code
    """
    return "[PREAP] Deterministic function output for pre-approval inquiries"


def next_steps(userQuery: str) -> str:
    """
    Function that handles inquiries about the next steps after pre-approval, including document submission, income verification, and credit check timelines.
    Topic: "Borrower is asking about the next steps after pre‑approval, including document submission, income verification, and credit check timelines.
    
    Args:
        userQuery (str): User's query string
        
    Returns:
        str: 5-letter summary code
    """
    return "[NEXTP] Deterministic function output for next steps inquiries"


def loan_application(userQuery: str) -> str:
    """
    Function that handles loan application process,required documents, income verification, credit checks.
    Topics: Application process, required documents, income verification, credit checks.
    
    Args:
        userQuery (str): User's query string
        
    Returns:
        str: 5-letter summary code
    """
    return "[APPLI] Deterministic function output for loan application inquiries"


def rate_types(userQuery: str) -> str:
    """
    Function that handles inquiries about rate types and comparison (fixed vs variable),current promotional rates, and how rate‑lock periods work.
    Topic: "Discussion about fixed vs. variable rates, current promotional rates, and how rate‑lock periods work.
    
    Args:
        userQuery (str): User's query string
        
    Returns:
        str: 5-letter summary code
    """
    return "[RATEV] Deterministic function output for rate types inquiries"


def amortization(userQuery: str) -> str:
    """
    Function that handles amortization period adjustments. Gauges how shortening or extending the amortization period affects long-term interest costs and monthly payments.
    Topic: "Borrower is wanting to shorten or extend the amortization period and how it affects long‑term interest costs."
    
    Args:
        userQuery (str): User's query string
        
    Returns:
        str: 5-letter summary code
    """
    return "[AMORT] Deterministic function output for amortization inquiries"


def term_renewal(userQuery: str) -> str:
    """
    Function that handles term renewal and end-of-term options inquiries, like  new rate offers, early renewal penalties, and documents required.
    Topic: "Options available when nearing the end of the current term, new rate offers, early renewal penalties, and documents required."
    
    Args:
        userQuery (str): User's query string
        
    Returns:
        str: 5-letter summary code
    """
    return "[RENEW] Deterministic function output for term renewal inquiries"


def prepayment_penalties(userQuery: str) -> str:
    """
    Function that handles prepayment penalties, IRD (Interest Rate Differential) calculations, and scenarios where penalties may be waived.
    Topic: "Borrower is asking about prepayment penalties, IRD (Interest Rate Differential), and scenarios where penalties may be waived.
    
    Args:
        userQuery (str): User's query string
        
    Returns:
        str: 5-letter summary code
    """
    return "[PENAL] Deterministic function output for prepayment penalties inquiries"


def prepayment_options(userQuery: str) -> str:
    """
    Function that handles annual prepayment options and scheduling inquiries. Used on inquiries about how much the borrower can prepay annually, impact on principal reduction, and how to schedule extra payments.
    Topic: "How much the borrower can prepay annually, impact on principal reduction, and how to schedule extra payments.
    
    Args:
        userQuery (str): User's query string
        
    Returns:
        str: 5-letter summary code
    """
    return "[PREPA] Deterministic function output for prepayment options inquiries"


def refinancing(userQuery: str) -> str:
    """
    Function that handles refinancing options and inquiries.about refinancing for debt consolidation, home renovations, improved interest rates, or accessing home equity.
    Topic: "Borrower is inquiring about refinancing for debt consolidation, home renovations, improved interest rates, or accessing home equity.
    
    Args:
        userQuery (str): User's query string
        
    Returns:
        str: 5-letter summary code
    """
    return "[REFIN] Deterministic function output for refinancing inquiries"


def financial_hardship(userQuery: str) -> str:
    """
    Function that handles financial hardship and assistance program inquiries. Used for temporary financial difficulties and asking about deferrals, payment restructuring, or hardship programs.
    Topic: "Borrower is explaining temporary financial difficulties and asking about deferrals, payment restructuring, or hardship programs.
    
    Args:
        userQuery (str): User's query string
        
    Returns:
        str: 5-letter summary code
    """
    return "[HELPD] Deterministic function output for financial hardship inquiries"


def insurance(userQuery: str) -> str:
    """
    Function that handles insurance and escrow requirements inquiries. Used for property tax escrow, home insurance requirements, mortgage default insurance, and how changes affect monthly payments.
    Topic: "Borrower is verifying property tax escrow, home insurance requirements, mortgage default insurance, and how changes affect monthly payments.
    
    Args:
        userQuery (str): User's query string
        
    Returns:
        str: 5-letter summary code
    """
    return "[INSUR] Deterministic function output for insurance inquiries"


# Reusable utility functions that can be shared across topics

def payment_info(userQuery: str) -> str:
    """
    Function that handles generic payment-related inquiries. Used across payment increase, missed payment, and general payment topics.
    
    Args:
        userQuery (str): User's query string
        
    Returns:
        str: 5-letter summary code
    """
    return "[PAYMT] Deterministic function output for payment-related inquiries"


def documents(userQuery: str) -> str:
    """
    Function that handles document and verification requirements inquiries. Used across application, pre-approval, and renewal processes.
    
    Args:
        userQuery (str): User's query string
        
    Returns:
        str: 5-letter summary code
    """
    return "[DOCUM] Deterministic function output for document inquiries covering application, pre-approval, and renewal processes"


def timelines(userQuery: str) -> str:
    """
    Function that handles timeline and scheduling inquiries. Used across various processes that involve timelines.
    
    Args:
        userQuery (str): User's query string
        
    Returns:
        str: 5-letter summary code
    """
    return "[TIMEL] Deterministic function output for maturity timeline inquiries"


def calculation(userQuery: str) -> str:
    """
    Function that handles calculation-related inquiries. Used for interest calculations, payment calculations, penalty calculations.
    
    Args:
        userQuery (str): User's query string
        
    Returns:
        str: 5-letter summary code
    """
    return "[CALCS] Deterministic function output for loan calculation inquiries (interest, payments, penalties)"


def options(userQuery: str) -> str:
    """
    Function that handles options and scenarios analysis inquiries. Used across various topics that involve multiple options or scenarios.
    
    Args:
        userQuery (str): User's query string
        
    Returns:
        str: 5-letter summary code
    """
    return "[OPTNS] Deterministic function output for loan payback options inquiries"


def balance(userQuery: str) -> str:
    """
    Function that handles balance and payment date inquiries. Resusable for balance and the final payment date with the current payment
    Topic: "Borrower wants to know the balance and the final payment date with the current payment."
    
    Args:
        userQuery (str): User's query string
        
    Returns:
        str: 5-letter summary code
    """
    return "[BALNC] Deterministic function output for loan balance inquiries"


def payment_increase(userQuery: str) -> str:
    """
    Function that handles payment increase scenarios, maximum allowed and final payment dates. 
    Topic: "Borrower wants to increase the payment, asks how much is allowed, and asks for final payment dates across scenarios proposed by the agent."
    
    Args:
        userQuery (str): User's query string
        
    Returns:
        str: 5-letter summary code
    """
    return "[PAYUP] Deterministic function output for payment increase inquiries"


def lump_sum(userQuery: str) -> str:
    """
    Function that handles lump-sum payment contributions inquiries.
    Topic: "Borrower wants to make a lump-sum payment and asks how much can be contributed."
    
    Args:
        userQuery (str): User's query string
        
    Returns:
        str: 5-letter summary code
    """
    return "[LUMPD] Deterministic function output for lump-sum payment inquiries"


def application(userQuery: str) -> str:
    """
    Function that handles loan application process and requirements inquiries. Manages both pre-approval and application process inquiries to ensure consistency in handling document and verification requirements.
    Topics: Application process, required documents, income verification, credit checks.
    
    Args:
        userQuery (str): User's query string
        
    Returns:
        str: 5-letter summary code
    """
    return "[APPLI] Deterministic function output for application inquiries"


def rate_variation(userQuery: str) -> str:
    """
    Function that handles rate variation and comparison inquiries (fixed vs variable). Covers inquiries about differences between fixed and variable rates, current promotional rates, and how rate-lock periods work.
    Topic: "Discussion about fixed vs. variable rates, current promotional rates, and how rate‑lock periods work."
    
    Args:
        userQuery (str): User's query string
        
    Returns:
        str: 5-letter summary code
    """
    return "[RATEV] Deterministic function output for rate variation inquiries"


# Topic mapping dictionary for easy access
TOPIC_FUNCTIONS = {
    1: balance,         # Balance and payment date
    2: payment_increase,       # Payment increase scenarios  
    3: lump_sum,        # Lump-sum payments
    4: rate_types,        # Interest rates and total interest
    5: missed_payments,        # Missed payments and penalties
    6: pre_approval,       # Pre-approval status
    7: next_steps,       # Next steps after pre-approval
    8: application,         # Loan application process (first instance)
    9: rate_variation,       # Fixed vs variable rates
    10: application,        # Loan application process (second instance - reused)
    11: amortization,      # Amortization period changes
    12: term_renewal,      # Term renewal options
    13: prepayment_penalties,      # Prepayment penalties
    14: prepayment_options,     # Annual prepayment options
    15: refinancing,       # Refinancing inquiries
    16: financial_hardship,       # Financial hardship programs
    17: insurance         # Insurance and escrow
}


def get_topic_summary(topic_number: int, userQuery: str) -> str:
    """
    Get summary for a specific topic number.
    
    Args:
        topic_number (int): Topic number (1-17)
        userQuery (str): User's query string
        
    Returns:
        str: 5-letter summary code for the topic
    """
    if topic_number in TOPIC_FUNCTIONS:
        return TOPIC_FUNCTIONS[topic_number](userQuery)
    else:
        return "UNKNW"


def get_all_summaries(userQuery: str) -> dict:
    """
    Get all topic summaries for a given user query.
    
    Args:
        userQuery (str): User's query string
        
    Returns:
        dict: Dictionary mapping topic numbers to their summary codes
    """
    return {
        topic_num: func(userQuery) 
        for topic_num, func in TOPIC_FUNCTIONS.items()
    }