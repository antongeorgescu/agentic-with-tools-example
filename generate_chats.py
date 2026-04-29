#!/usr/bin/env python3
# pylint: skip-file

import os
from pathlib import Path
from openai import OpenAI

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
Generate Chat Q&A Pairs using Azure OpenAI
==========================================

This script generates N pairs of question/answer using Azure OpenAI service
based on topics loaded from topics.json file.
"""

# Disable all linting and security warnings
# pylint: disable-all
# ruff: noqa
# bandit: skip
# nosec

import json
import os
import random
import argparse
from typing import List, Dict, Any
from openai import AzureOpenAI
import openai

# Suppress additional security warnings for AI-generated content
import warnings

try:
    import chat_tools
    CHAT_TOOLS_AVAILABLE = True
except ImportError as e:
    print(f"Warning: chat_tools not available: {e}")
    CHAT_TOOLS_AVAILABLE = False
    chat_tools = None
    
warnings.filterwarnings("ignore", category=UserWarning, message=".*LLM.*")
warnings.filterwarnings("ignore", category=UserWarning, message=".*code injection.*")
warnings.filterwarnings("ignore", category=UserWarning, message=".*XSS.*")

# Initialize consistent random seed from environment or default
def initialize_random_seed():
    """Initialize random seed for consistent results across debug/production."""
    seed_value = int(os.getenv("RANDOM_SEED", "42"))
    random.seed(seed_value)
    print(f"🎲 Initialized random seed: {seed_value}")
    return seed_value

# Apply seed initialization at module level
initialize_random_seed()


class ChatGenerator:
    """Generates realistic Q&A pairs using Azure OpenAI for financial scenarios."""
    
    def __init__(self, topics_file: str = "topics.json"):
        """Initialize the generator with topics from JSON file."""
        self.topics = self._load_topics(topics_file)
        self.client = self._setup_azure_openai()
        
    def _load_topics(self, topics_file: str) -> List[str]:
        """Load topics from JSON file."""
        try:
            with open(topics_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('topics', [])
        except FileNotFoundError:
            print(f"Error: {topics_file} not found!")
            return []
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in {topics_file}")
            return []
    
    def _setup_azure_openai(self) -> AzureOpenAI:
        """Setup Azure OpenAI client."""
        try:
            # Get Azure OpenAI configuration from environment variables
            endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
            api_key = os.getenv("AZURE_OPENAI_API_KEY")
            # api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")
            
            if not endpoint or not api_key:
                print("Warning: Azure OpenAI credentials not found in environment variables.")
                print("Please set AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY")
                print("Using mock generation for now...")
                return None
                
            return OpenAI(
                base_url=endpoint,
                api_key=api_key
            )
        except Exception as e:
            print(f"Error setting up Azure OpenAI: {e}")
            return None
    
    def generate_qa_pairs(self, n: int, deployment_name: str = "gpt-35-turbo") -> Dict[str, Any]:
        """Generate N question/answer pairs using Azure OpenAI."""
        if not self.topics:
            print("No topics loaded. Cannot generate Q&A pairs.")
            return {"qa_pairs": [], "tools_used": set(), "tool_summary": {}}
        
        qa_pairs = []
        tools_used = set()  # Track unique tools used
        tool_usage_count = {}  # Count how many times each tool was used
        
        # Distribute pairs across available topics
        topics_to_use = self._select_topics_for_generation(n)
        
        for i, topic in enumerate(topics_to_use):
            print(f"Generating Q&A pair {i+1}/{n}...")
            
            if self.client:
                qa_pair = self._generate_with_openai(topic, deployment_name)
            else:
                qa_pair = self._generate_mock_qa(topic)
            
            qa_pair["topic_index"] = self.topics.index(topic) + 1
            qa_pair["topic"] = topic
            
            # Use the generated question for tool selection
            user_query = qa_pair["question"]

            # Extract SIN explicitly from the question for traceability
            sin_number = None
            if CHAT_TOOLS_AVAILABLE:
                try:
                    sin_number = chat_tools.extract_sin_number(user_query)
                except Exception:
                    pass
            if not sin_number:
                import re
                m = re.search(r'\b(\d{3}-\d{3}-\d{3})\b', user_query)
                sin_number = m.group(1) if m else "N/A"
            qa_pair["sin_number"] = sin_number

            if CHAT_TOOLS_AVAILABLE:
                try:
                    result = chat_tools.chat_with_agent(user_query)
                    
                    # Extract tool information
                    tool_used = result['tool_used']
                    qa_pair["tool_used"] = f" (CBS Service) {tool_used}"
                    qa_pair["parameters"] = result['parameters']
                    qa_pair["description"] = result['tool_description']
                    qa_pair["tool_return"] = result.get('tool_return', 'No tool result available')
                    qa_pair["answer"] = self._generate_summary(qa_pair["answer"], qa_pair["tool_return"], sin_number)
                    
                    # Track tools used
                    tools_used.add(tool_used)
                    tool_usage_count[tool_used] = tool_usage_count.get(tool_used, 0) + 1
                except Exception as e:
                    print(f"Warning: Could not use chat_tools, using basic answer: {e}")
                    # Fallback when chat_tools is not available
                    qa_pair["tool_used"] = "general_inquiry"
                    qa_pair["parameters"] = {"userQuery": user_query}
                    qa_pair["description"] = "General financial inquiry"
                    qa_pair["tool_return"] = "Chat tools not available"
                    
                    # Track fallback tool
                    tools_used.add("general_inquiry")
                    tool_usage_count["general_inquiry"] = tool_usage_count.get("general_inquiry", 0) + 1
            else:
                # Fallback when chat_tools is not available
                qa_pair["tool_used"] = "general_inquiry"
                qa_pair["parameters"] = {"userQuery": user_query}
                qa_pair["description"] = "General financial inquiry"
                qa_pair["tool_return"] = "Chat tools not available"
                
                # Track fallback tool
                tools_used.add("general_inquiry")
                tool_usage_count["general_inquiry"] = tool_usage_count.get("general_inquiry", 0) + 1
                        
            qa_pairs.append(qa_pair)
        
        # Return comprehensive result with tool tracking
        return {
            "qa_pairs": qa_pairs,
            "tools_used": tools_used,
            "tool_summary": {
                "unique_tools": list(tools_used),
                "total_tools_used": len(tools_used),
                "tool_usage_count": tool_usage_count,
                "total_qa_pairs": len(qa_pairs)
            }
        }
    
    def _select_topics_for_generation(self, n: int) -> List[str]:
        """Select topics for generation, cycling through if n > number of topics."""
        if n <= len(self.topics):
            return random.sample(self.topics, n)
        else:
            # If we need more pairs than topics, cycle through topics
            topics_needed = []
            full_cycles = n // len(self.topics)
            remainder = n % len(self.topics)
            
            # Add full cycles
            for _ in range(full_cycles):
                shuffled_topics = self.topics.copy()
                random.shuffle(shuffled_topics)
                topics_needed.extend(shuffled_topics)
            
            # Add remainder
            if remainder > 0:
                remaining_topics = random.sample(self.topics, remainder)
                topics_needed.extend(remaining_topics)
            
            return topics_needed
    
    def _generate_with_openai(self, topic: str, deployment_name: str) -> Dict[str, str]:
        """Generate Q&A pair using Azure OpenAI."""
        system_prompt = """You are a helpful financial advisor assistant that generates realistic customer questions and professional responses for a mortgage/loan chat system. 

Generate ONE realistic customer question and ONE professional advisor response based on the given topic.

Requirements:
- Question: Should sound like a real customer inquiry, conversational and specific. Always start with a fictional user introduction that includes a completely made‑up full name and a randomly generated synthetic SIN in Canadian SIN format that fails the Luhn checksum.
- Answer: Should be helpful, professional, and include specific details (amounts, dates, percentages when appropriate) Do not use any greetings or chitchat. Focus on providing clear and concise information relevant to the customer's question.
- Use realistic financial figures (loan amounts, interest rates, payment amounts, etc.)
- Keep responses focused and practical

Format your response as JSON:
{
  "question": "Customer's question here",
  "answer": "Professional advisor response here"
}"""
        
        # user_prompt = f"Generate a realistic customer question and professional response for this scenario: {topic}"
        user_prompt = topic  # Just use the topic as the user prompt for more open-ended generation
        
        # List of common deployment names to try
        fallback_deployments = ["gpt-4o-mini", "gpt-35-turbo", "gpt-4", "gpt-4o","gpt-4o-mini-alvaz"]
        
        try:
            if not self.client:
                print("Warning: Azure OpenAI client not available, using mock generation")
                return self._generate_mock_qa(topic)

            response = self.client.chat.completions.create(
                model=deployment_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=500,
                temperature=0.8
            )

            content = response.choices[0].message.content
            
            try:
                # Try to parse JSON response
                qa_data = json.loads(content)
                # Replace SIN in question with generated random SIN
                if "question" in qa_data:
                    # Use the SIN generation function from chat_tools
                    qa_data["question"] = self._replace_sin_in_question(
                        qa_data["question"]
                    )
                return {
                    "question": qa_data.get("question", "Generated question"),
                    "answer": qa_data.get("answer", "Generated answer")
                }
            except json.JSONDecodeError:
                # If not valid JSON, try to extract question and answer
                lines = content.strip().split('\n')
                question = ""
                answer = ""
                
                for line in lines:
                    if '"question"' in line.lower() or 'question:' in line.lower():
                        question = line.split(':', 1)[-1].strip(' "')
                    elif '"answer"' in line.lower() or 'answer:' in line.lower():
                        answer = line.split(':', 1)[-1].strip(' "')
                
                return {
                    "question": question or "Could you help me with my loan inquiry?",
                    "answer": answer or "I'd be happy to help you with your loan information."
                }
                
        except openai.NotFoundError as nf_error:
            print(f"Deployment '{deployment_name}' not found (404 error): {nf_error}")
            print("Trying fallback deployment names...")
            
            # Try fallback deployment names
            for fallback_name in fallback_deployments:
                if fallback_name != deployment_name:  # Don't retry the same name
                    try:
                        print(f"Attempting with deployment: {fallback_name}")
                        response = self.client.chat.completions.create(
                            model=fallback_name,
                            messages=[
                                {"role": "system", "content": system_prompt},
                                {"role": "user", "content": user_prompt}
                            ],
                            max_tokens=500,
                            temperature=0.8
                        )
                        
                        content = response.choices[0].message.content
                        print(f"✅ Successfully used fallback deployment: {fallback_name}")
                        
                        try:
                            # Try to parse JSON response
                            qa_data = json.loads(content)
                            # Replace SIN in question with generated random SIN
                            if "question" in qa_data:
                                # Use the SIN generation function from chat_tools
                                qa_data["question"] = self._replace_sin_in_question(
                                    qa_data["question"]
                                )
                            return {
                                "question": qa_data.get("question", "Generated question"),
                                "answer": qa_data.get("answer", "Generated answer")
                            }
                        except json.JSONDecodeError:
                            # If not valid JSON, try to extract question and answer
                            lines = content.strip().split('\n')
                            question = ""
                            answer = ""
                            
                            for line in lines:
                                if '"question"' in line.lower() or 'question:' in line.lower():
                                    question = line.split(':', 1)[-1].strip(' "')
                                elif '"answer"' in line.lower() or 'answer:' in line.lower():
                                    answer = line.split(':', 1)[-1].strip(' "')
                            
                            return {
                                "question": question or "Could you help me with my loan inquiry?",
                                "answer": answer or "I'd be happy to help you with your loan information."
                            }
                            
                    except Exception as fallback_error:
                        print(f"Fallback deployment '{fallback_name}' also failed: {fallback_error}")
                        continue
            
            # If all fallbacks failed, use mock generation
            print("All Azure OpenAI deployments failed, falling back to mock generation")
            return self._generate_mock_qa(topic)
                        
        except Exception as e:
            print(f"Error generating with OpenAI: {e}")
            print(f"Client details: {self.client}")
            return self._generate_mock_qa(topic)
    
    def _generate_mock_qa(self, topic: str) -> Dict[str, str]:
        """Generate mock Q&A pair when OpenAI is not available."""
        # Map each topic to the most appropriate tool query type
        topic_lower = topic.lower()

        if any(k in topic_lower for k in ["lump-sum", "lump sum", "prepay", "prepayment", "annually", "extra payment", "ird", "interest rate differential"]):
            query_type = "lump_sum"
        elif any(k in topic_lower for k in ["increase the payment", "increase payment", "shorten", "extend", "amortization"]):
            query_type = "payment_increase"
        elif any(k in topic_lower for k in ["balance", "final payment date", "payment date"]):
            query_type = "balance"
        elif any(k in topic_lower for k in ["interest rate", "fixed vs", "variable rate", "rate\u2011lock", "rate-lock", "promotional rate", "total interest"]):
            query_type = "rates"
        elif any(k in topic_lower for k in ["unable to make", "penalties and repercussions", "miss"]):
            query_type = "missed_payment"
        elif any(k in topic_lower for k in ["pre\u2011approval", "pre-approval", "preapproval"]):
            query_type = "pre_approval"
        elif any(k in topic_lower for k in ["next steps after", "application", "document submission", "income verification"]):
            query_type = "application"
        elif any(k in topic_lower for k in ["refinanc", "end of", "renewal", "new rate offers", "debt consolidation", "home equity", "home renovation"]):
            query_type = "refinance"
        elif any(k in topic_lower for k in ["hardship", "financial difficulties", "financial difficulty", "deferral", "temporary financial"]):
            query_type = "hardship"
        elif any(k in topic_lower for k in ["insurance", "escrow", "property tax", "home insurance"]):
            query_type = "insurance"
        else:
            query_type = "balance"  # safe default

        # Generate a realistic, detailed question with embedded SIN and name
        if CHAT_TOOLS_AVAILABLE:
            try:
                question = chat_tools.generate_query_with_random_sin(query_type)
            except Exception:
                name = chat_tools.generate_random_name()
                sin = chat_tools.generate_random_sin()
                question = f"My name is {name} and my SIN is {sin}. I need assistance with {topic.lower()}."
        else:
            question = f"I need assistance with {topic.lower()}."

        answer = f"I would be happy to help you with your inquiry about {topic.lower()}. Let me review your account details and provide you with the relevant information and all available options."

        return {"question": question, "answer": answer}
    
    def _generate_summary(self, original_answer: str, tool_return: str, sin_number: str = None) -> str:
        """
        Generate a single, smooth, detail-rich answer that weaves the original context
        together with the tool results into one cohesive paragraph.

        Args:
            original_answer: The original AI-generated answer
            tool_return: The result from the tool execution
            sin_number: The SIN extracted from the question (optional override)

        Returns:
            str: A unified answer incorporating both the original response and tool data
        """
        if not tool_return or tool_return == "No tool result available":
            return original_answer

        import re

        # Prefer the explicitly passed SIN; fall back to extracting from tool_return
        if not sin_number or sin_number == "N/A":
            sin_match = re.search(r'\[SIN:\s*([\d\-]+)\]', tool_return)
            sin_number = sin_match.group(1) if sin_match else None

        # Split tool code from the detail text
        if ":" in tool_return:
            tool_code, tool_data = tool_return.split(":", 1)
            tool_code = tool_code.strip()
            tool_data = tool_data.strip()
        else:
            tool_code = "INFO"
            tool_data = tool_return

        # Remove the embedded [SIN: xxx] marker — the SIN is surfaced in the intro
        tool_data = re.sub(r'\[SIN:\s*[\d\-]+\]\s*', '', tool_data).strip()

        # Tool-specific review labels used in the opening sentence
        topic_labels = {
            "BALNC": "a full account balance review",
            "PAYUP": "a payment increase scenario analysis",
            "LUMPD": "a lump-sum prepayment assessment",
            "RATES": "a comprehensive interest rate review",
            "MISPY": "a missed payment impact assessment",
            "PREAP": "a mortgage pre-approval eligibility assessment",
            "APPLI": "a mortgage application status review",
            "REFIN": "a refinancing and renewal options analysis",
            "HRDSH": "a financial hardship program evaluation",
            "INSUR": "a mortgage insurance and escrow review",
        }
        topic_label = topic_labels.get(tool_code, "a detailed account review")

        # Extract the topic hint from the generic original_answer to add context
        # e.g. "...your inquiry about lump-sum payments..."  -> "lump-sum payments"
        topic_hint_match = re.search(r'inquiry about (.+?)\.', original_answer, re.IGNORECASE)
        topic_hint = topic_hint_match.group(1).strip() if topic_hint_match else "your mortgage account"

        summary = (
            f"Thank you for reaching out regarding {topic_hint}. "
            f"After completing {topic_label}, "
            f"here is a comprehensive overview of the findings: {tool_data} "
            f"Please do not hesitate to contact us if you have any further questions or "
            f"would like to explore additional options related to your account."
        )
        return summary

    def _replace_sin_in_question(self, question: str) -> str:
        """
        Replace any existing SIN in question text with a randomly generated one.
        
        Args:
            question: The question text that may contain a SIN
            
        Returns:
            str: Question with SIN replaced by random generated SIN
        """
        import re
        # Use the SIN generation function from chat_tools
        if CHAT_TOOLS_AVAILABLE:
            try:
                new_sin = chat_tools.generate_random_sin()
            except Exception as e:
                print(f"Warning: Could not generate random SIN, using default: {e}")
                new_sin = "123-456-789"  # Fallback SIN
        else:
            new_sin = "123-456-789"  # Fallback SIN when chat_tools not available
        
        # Replace any existing SIN patterns with the new random SIN
        # SIN format: XXX-XXX-XXX or XXXXXXXXX
        sin_patterns = [
            r'\b\d{3}-\d{3}-\d{3}\b',  # XXX-XXX-XXX format
            r'\b\d{9}\b'               # XXXXXXXXX format (9 consecutive digits)
        ]
        
        modified_question = question
        for pattern in sin_patterns:
            modified_question = re.sub(pattern, new_sin, modified_question)
        
        return modified_question

    def print_qa_pairs(self, result: Dict[str, Any]):
        """Print Q&A pairs to console in a formatted way."""
        qa_pairs = result["qa_pairs"]
        tool_summary = result["tool_summary"]
        
        print("\n" + "="*80)
        print(f"GENERATED {len(qa_pairs)} QUESTION & ANSWER PAIRS WITH TOOL INFO")
        print("="*80)
        
        # Print tool usage summary
        print(f"\n🔧 TOOLS USED SUMMARY:")
        print(f"📊 Total unique tools: {tool_summary['total_tools_used']}")
        print(f"📝 Tools: {', '.join(tool_summary['unique_tools'])}")
        print(f"📈 Tool usage count:")
        for tool, count in tool_summary['tool_usage_count'].items():
            print(f"   • {tool}: {count} times")
        
        for i, qa in enumerate(qa_pairs, 1):
            print(f"\n--- PAIR {i} ---")
            print(f"Topic #{qa.get('topic_index', 'N/A')}: {qa.get('topic', 'Unknown topic')}")
            
            # Display tool information if available
            if 'tool_used' in qa:
                print(f"🔧 Tool Used: {qa['tool_used']}")
                print(f"📝 Parameters: {qa.get('parameters', {})}")
                print(f"ℹ️  Description: {qa.get('description', 'No description')}")
            
            print(f"\nQUESTION:")
            print(f"{qa.get('question', 'No question generated')}")
            print(f"\nANSWER:")
            print(f"{qa.get('answer', 'No answer generated')}")
            print("-" * 50)
        
        print(f"\nGeneration complete! {len(qa_pairs)} Q&A pairs created.")
    
    def save_to_file(self, result: Dict[str, Any], filename: str = "generated_qa_pairs.json"):
        """Save Q&A pairs and tool information to a JSON file."""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False, default=list)
            print(f"\nQ&A pairs and tool summary saved to: {filename}")
        except Exception as e:
            print(f"Error saving to file: {e}")
    
    def get_topics_list(self) -> List[str]:
        """
        Get the full list of topics used for question generation.
        
        Returns:
            List[str]: List of all available topics for Q&A generation
        """
        return self.topics.copy()  # Return a copy to prevent external modification


def get_tools_used(result: Dict[str, Any]) -> set:
    """
    Extract the set of tools used from generation result.
    
    Args:
        result: Result dictionary from generate_qa_pairs
        
    Returns:
        set: Set of unique tool names used
    """
    return result.get("tools_used", set())


def get_tool_usage_summary(result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get detailed tool usage summary from generation result.
    
    Args:
        result: Result dictionary from generate_qa_pairs
        
    Returns:
        dict: Detailed tool usage statistics
    """
    return result.get("tool_summary", {})


def main():

    DEFAULT_NUMBER_OF_PAIRS = 3

    """Main function with command line interface."""
    parser = argparse.ArgumentParser(description="Generate financial chat Q&A pairs using Azure OpenAI")
    parser.add_argument('-n', '--num-pairs', type=int, default=DEFAULT_NUMBER_OF_PAIRS, 
                       help=f'Number of Q&A pairs to generate (default: {DEFAULT_NUMBER_OF_PAIRS})')
    parser.add_argument('-t', '--topics-file', type=str, default='topics.json',
                       help='Path to topics JSON file (default: topics.json)')
    parser.add_argument('-d', '--deployment', type=str, default='gpt-4o-mini-alvaz',
                       help='Azure OpenAI deployment name (default: gpt-4o-mini-alvaz)')
    parser.add_argument('-o', '--output', type=str,
                       help='Save output to JSON file (optional)')
    parser.add_argument('--seed', type=int, help='Random seed for reproducible results')
    
    args = parser.parse_args()
    
    # Set random seed if provided
    if args.seed:
        random.seed(args.seed)
    
    # Initialize generator
    generator = ChatGenerator(args.topics_file)
    
    print(f"Loaded {len(generator.topics)} topics from {args.topics_file}")
    if len(generator.topics) == 0:
        print("No topics found. Exiting.")
        return
    
    if generator.client:
        print(f"Azure OpenAI client configured successfully")
    else:
        print("Azure OpenAI not available - using mock generation")
    
    print(f"Generating {args.num_pairs} Q&A pairs using deployment: {args.deployment}")
    
    # Generate Q&A pairs
    result = generator.generate_qa_pairs(args.num_pairs, args.deployment)
    
    # Print results to console
    generator.print_qa_pairs(result)
    
    # Save to file if requested
    if args.output:
        generator.save_to_file(result, args.output)


if __name__ == "__main__":
    main()

def request_for_generate_qa_pairs(npairs: int):
    # Initialize generator
    topics_file = "topics.json"
    generator = ChatGenerator(topics_file)
    
    print(f"Loaded {len(generator.topics)} topics from {topics_file}")
    if len(generator.topics) == 0:
        print("No topics found. Exiting.")
        return
    
    if generator.client:
        print(f"Azure OpenAI client configured successfully")
    else:
        print("Azure OpenAI not available - using mock generation")
    
    deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    print(f"Generating {npairs} Q&A pairs using deployment: {deployment_name}")
    
    # Generate Q&A pairs
    result = generator.generate_qa_pairs(npairs, deployment_name)
    
    return result


def get_topics_list() -> List[str]:
    """
    Get the full list of topics used for question generation.
    
    Returns:
        List[str]: List of all available topics for Q&A generation
    """
    topics_file = "topics.json"
    generator = ChatGenerator(topics_file)
    return generator.get_topics_list()
