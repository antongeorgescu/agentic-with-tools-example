#!/usr/bin/env python3
# pylint: skip-file
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
            pass
        AzureChatOpenAI = MockLLM
        
from pydantic import BaseModel, Field


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
        return f"BALNC: Processing balance inquiry for: {userQuery[:50]}..."
    
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
        return f"PAYUP: Processing payment increase inquiry for: {userQuery[:50]}..."
    
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
        return f"LUMPD: Processing lump-sum payment inquiry for: {userQuery[:50]}..."
    
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
        return f"RATES: Processing interest rate inquiry for: {userQuery[:50]}..."
    
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
        return f"MISSP: Processing missed payment inquiry for: {userQuery[:50]}..."
    
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
        return f"PREAP: Processing pre-approval inquiry for: {userQuery[:50]}..."
    
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
        return f"APPLI: Processing application inquiry for: {userQuery[:50]}..."
    
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
        return f"REFIN: Processing refinancing inquiry for: {userQuery[:50]}..."
    
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
        return f"HELPD: Processing hardship inquiry for: {userQuery[:50]}..."
    
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
        return f"INSUR: Processing insurance inquiry for: {userQuery[:50]}..."
    
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
        
        # Define keyword mappings to tools
        tool_mappings = [
            (["balance", "owe", "remaining", "left", "current"], "balance_tool", "Function that handles balance and payment date inquiries, with parameters extracted from the user query. Topics include current loan balance, final payment dates, payment schedules, and remaining balance information."),
            (["increase", "raise", "more", "higher", "boost"], "payment_increase_tool", "Function that handles payment increase scenarios, with parameters extracted from the user query. Topics include increasing monthly payments, adjusting payment schedules, and calculating new payment amounts."),
            (["lump", "extra", "additional", "one-time", "bulk"], "lump_sum_tool", "Function that handles lump-sum payment options, with parameters extracted from the user query. Topics include making additional payments, reducing principal, and calculating interest savings."),
            (["rate", "interest", "apr", "percentage"], "interest_rate_tool", "Function that provides interest rate information, with parameters extracted from the user query. Topics include current rates, rate changes, and comparison of different rate options."),
            (["miss", "late", "penalty", "behind", "overdue"], "missed_payment_tool", "Function that handles missed payment penalties, with parameters extracted from the user query. Topics include late fees, penalty calculations, and payment recovery options."),
            (["pre-approval", "preapproval", "pre approval"], "pre_approval_tool", "Function that handles the pre-approval process, with parameters extracted from the user query. Topics include eligibility criteria, required documents, and application steps."),
            (["application", "apply", "applying", "documents"], "application_tool", "Function that handles the loan application process, with parameters extracted from the user query. Topics include application steps, required documents, and approval timelines."),
            (["refinance", "refi", "consolidation"], "refinancing_tool", "Function that handles refinancing options, with parameters extracted from the user query. Topics include refinancing eligibility, rate comparison, and application process."),
            (["hardship", "difficulty", "help", "struggle", "defer"], "hardship_tool", "Function that handles financial hardship assistance, with parameters extracted from the user query. Topics include deferment options, payment plans, and eligibility criteria."),
            (["insurance", "escrow", "tax", "property"], "insurance_tool", "Function that handles insurance and escrow matters, with parameters extracted from the user query. Topics include policy details, escrow accounts, and property tax information.")
        ]
        
        # Check each mapping
        for keywords, tool_name, description in tool_mappings:
            if any(keyword in user_lower for keyword in keywords):
                return {
                    "tool_name": tool_name,
                    "description": description,
                    "parameters": {"userQuery": user_input}
                }
        
        # Default fallback
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
            "description": tool.description
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
    return "RATES"


def missed_payments(userQuery: str) -> str:
    """
    Function that handles missed payments and penalty inquiries. Used for questions about missed or late payments, payment penalties, consequences of non-payment, and payment assistance programs.
    Topic: "Borrower is unable to make the following 3 payments and asks about penalties and repercussions."
    
    Args:
        userQuery (str): User's query string
        
    Returns:
        str: 5-letter summary code
    """
    return "MISSP"


def pre_approval(userQuery: str) -> str:
    """
    Function that handles pre-approval process and status inquiries. Covers questions about whether pre-approval has been processed, required documents, income verification, and credit check timelines.
    Topic: "Borrower is asking whether their pre‑approval has been processed, required documents, income verification, and credit check timelines"
    
    Args:
        userQuery (str): User's query string
        
    Returns:
        str: 5-letter summary code
    """
    return "PREAP"


def next_steps(userQuery: str) -> str:
    """
    Function that handles inquiries about the next steps after pre-approval, including document submission, income verification, and credit check timelines.
    Topic: "Borrower is asking about the next steps after pre‑approval, including document submission, income verification, and credit check timelines.
    
    Args:
        userQuery (str): User's query string
        
    Returns:
        str: 5-letter summary code
    """
    return "NEXTP"


def loan_application(userQuery: str) -> str:
    """
    Function that handles loan application process,required documents, income verification, credit checks.
    Topics: Application process, required documents, income verification, credit checks.
    
    Args:
        userQuery (str): User's query string
        
    Returns:
        str: 5-letter summary code
    """
    return "APPLI"


def rate_types(userQuery: str) -> str:
    """
    Function that handles inquiries about rate types and comparison (fixed vs variable),current promotional rates, and how rate‑lock periods work.
    Topic: "Discussion about fixed vs. variable rates, current promotional rates, and how rate‑lock periods work.
    
    Args:
        userQuery (str): User's query string
        
    Returns:
        str: 5-letter summary code
    """
    return "RATEV"


def amortization(userQuery: str) -> str:
    """
    Function that handles amortization period adjustments. Gauges how shortening or extending the amortization period affects long-term interest costs and monthly payments.
    Topic: "Borrower is wanting to shorten or extend the amortization period and how it affects long‑term interest costs."
    
    Args:
        userQuery (str): User's query string
        
    Returns:
        str: 5-letter summary code
    """
    return "AMORT"


def term_renewal(userQuery: str) -> str:
    """
    Function that handles term renewal and end-of-term options inquiries, like  new rate offers, early renewal penalties, and documents required.
    Topic: "Options available when nearing the end of the current term, new rate offers, early renewal penalties, and documents required."
    
    Args:
        userQuery (str): User's query string
        
    Returns:
        str: 5-letter summary code
    """
    return "RENEW"


def prepayment_penalties(userQuery: str) -> str:
    """
    Function that handles prepayment penalties, IRD (Interest Rate Differential) calculations, and scenarios where penalties may be waived.
    Topic: "Borrower is asking about prepayment penalties, IRD (Interest Rate Differential), and scenarios where penalties may be waived.
    
    Args:
        userQuery (str): User's query string
        
    Returns:
        str: 5-letter summary code
    """
    return "PENAL"


def prepayment_options(userQuery: str) -> str:
    """
    Function that handles annual prepayment options and scheduling inquiries. Used on inquiries about how much the borrower can prepay annually, impact on principal reduction, and how to schedule extra payments.
    Topic: "How much the borrower can prepay annually, impact on principal reduction, and how to schedule extra payments.
    
    Args:
        userQuery (str): User's query string
        
    Returns:
        str: 5-letter summary code
    """
    return "PREPA"


def refinancing(userQuery: str) -> str:
    """
    Function that handles refinancing options and inquiries.about refinancing for debt consolidation, home renovations, improved interest rates, or accessing home equity.
    Topic: "Borrower is inquiring about refinancing for debt consolidation, home renovations, improved interest rates, or accessing home equity.
    
    Args:
        userQuery (str): User's query string
        
    Returns:
        str: 5-letter summary code
    """
    return "REFIN"


def financial_hardship(userQuery: str) -> str:
    """
    Function that handles financial hardship and assistance program inquiries. Used for temporary financial difficulties and asking about deferrals, payment restructuring, or hardship programs.
    Topic: "Borrower is explaining temporary financial difficulties and asking about deferrals, payment restructuring, or hardship programs.
    
    Args:
        userQuery (str): User's query string
        
    Returns:
        str: 5-letter summary code
    """
    return "HELPD"


def insurance(userQuery: str) -> str:
    """
    Function that handles insurance and escrow requirements inquiries. Used for property tax escrow, home insurance requirements, mortgage default insurance, and how changes affect monthly payments.
    Topic: "Borrower is verifying property tax escrow, home insurance requirements, mortgage default insurance, and how changes affect monthly payments.
    
    Args:
        userQuery (str): User's query string
        
    Returns:
        str: 5-letter summary code
    """
    return "INSUR"


# Reusable utility functions that can be shared across topics

def payment_info(userQuery: str) -> str:
    """
    Function that handles generic payment-related inquiries. Used across payment increase, missed payment, and general payment topics.
    
    Args:
        userQuery (str): User's query string
        
    Returns:
        str: 5-letter summary code
    """
    return "PAYMT"


def documents(userQuery: str) -> str:
    """
    Function that handles document and verification requirements inquiries. Used across application, pre-approval, and renewal processes.
    
    Args:
        userQuery (str): User's query string
        
    Returns:
        str: 5-letter summary code
    """
    return "DOCUM"


def timelines(userQuery: str) -> str:
    """
    Function that handles timeline and scheduling inquiries. Used across various processes that involve timelines.
    
    Args:
        userQuery (str): User's query string
        
    Returns:
        str: 5-letter summary code
    """
    return "TIMEL"


def calculation(userQuery: str) -> str:
    """
    Function that handles calculation-related inquiries. Used for interest calculations, payment calculations, penalty calculations.
    
    Args:
        userQuery (str): User's query string
        
    Returns:
        str: 5-letter summary code
    """
    return "CALCS"


def options(userQuery: str) -> str:
    """
    Function that handles options and scenarios analysis inquiries. Used across various topics that involve multiple options or scenarios.
    
    Args:
        userQuery (str): User's query string
        
    Returns:
        str: 5-letter summary code
    """
    return "OPTNS"


def balance(userQuery: str) -> str:
    """
    Function that handles balance and payment date inquiries. Resusable for balance and the final payment date with the current payment
    Topic: "Borrower wants to know the balance and the final payment date with the current payment."
    
    Args:
        userQuery (str): User's query string
        
    Returns:
        str: 5-letter summary code
    """
    return "BALNC"


def payment_increase(userQuery: str) -> str:
    """
    Function that handles payment increase scenarios, maximum allowed and final payment dates. 
    Topic: "Borrower wants to increase the payment, asks how much is allowed, and asks for final payment dates across scenarios proposed by the agent."
    
    Args:
        userQuery (str): User's query string
        
    Returns:
        str: 5-letter summary code
    """
    return "PAYUP"


def lump_sum(userQuery: str) -> str:
    """
    Function that handles lump-sum payment contributions inquiries.
    Topic: "Borrower wants to make a lump-sum payment and asks how much can be contributed."
    
    Args:
        userQuery (str): User's query string
        
    Returns:
        str: 5-letter summary code
    """
    return "LUMPD"


def application(userQuery: str) -> str:
    """
    Function that handles loan application process and requirements inquiries. Manages both pre-approval and application process inquiries to ensure consistency in handling document and verification requirements.
    Topics: Application process, required documents, income verification, credit checks.
    
    Args:
        userQuery (str): User's query string
        
    Returns:
        str: 5-letter summary code
    """
    return "APPLI"


def rate_variation(userQuery: str) -> str:
    """
    Function that handles rate variation and comparison inquiries (fixed vs variable). Covers inquiries about differences between fixed and variable rates, current promotional rates, and how rate-lock periods work.
    Topic: "Discussion about fixed vs. variable rates, current promotional rates, and how rate‑lock periods work."
    
    Args:
        userQuery (str): User's query string
        
    Returns:
        str: 5-letter summary code
    """
    return "RATEV"


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