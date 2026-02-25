#!/usr/bin/env python3
# pylint: skip-file
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

# Suppress additional security warnings for AI-generated content
import warnings

import chat_tools
warnings.filterwarnings("ignore", category=UserWarning, message=".*LLM.*")
warnings.filterwarnings("ignore", category=UserWarning, message=".*code injection.*")
warnings.filterwarnings("ignore", category=UserWarning, message=".*XSS.*")


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
            api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")
            
            if not endpoint or not api_key:
                print("Warning: Azure OpenAI credentials not found in environment variables.")
                print("Please set AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY")
                print("Using mock generation for now...")
                return None
                
            return AzureOpenAI(
                azure_endpoint=endpoint,
                api_key=api_key,
                api_version=api_version
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
            result = chat_tools.chat_with_agent(user_query)
            
            # Extract tool information
            tool_used = result['tool_used']
            qa_pair["tool_used"] = f" (CBS Service) {tool_used}"
            qa_pair["parameters"] = result['parameters']
            qa_pair["description"] = result['tool_description']
            # qa_pair["answer"] = result['response']
            qa_pair["tool_return"] = result.get('tool_return', 'No tool result available')
            qa_pair["answer"] = self._generate_summary(qa_pair["answer"], qa_pair["tool_return"])
            
            # Track tools used
            tools_used.add(tool_used)
            tool_usage_count[tool_used] = tool_usage_count.get(tool_used, 0) + 1
                        
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
- Question: Should sound like a real customer inquiry, conversational and specific. Avoid using any greetings.
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
        try:
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
                
        except Exception as e:
            print(f"Error generating with OpenAI: {e}")
            return self._generate_mock_qa(topic)
    
    def _generate_mock_qa(self, topic: str) -> Dict[str, str]:
        """Generate mock Q&A pair when OpenAI is not available."""
        # Simple template-based generation as fallback
        question_templates = [
            "Can you help me understand about {}?",
            "I have a question regarding {}.",
            "Could you provide information on {}?",
            "I need assistance with {}."
        ]
        
        question = random.choice(question_templates).format(topic.lower())
        answer = f"I'd be happy to help you with your inquiry about {topic.lower()}. Let me provide you with the relevant information and options available to you."
        
        return {"question": question, "answer": answer}
    
    def _generate_summary(self, original_answer: str, tool_return: str) -> str:
        """
        Generate a comprehensive summary combining the original answer with tool results.
        
        Args:
            original_answer: The original AI-generated answer
            tool_return: The result from the tool execution
            
        Returns:
            str: Combined answer incorporating both the original response and tool data
        """
        if not tool_return or tool_return == "No tool result available":
            return original_answer
        
        # Extract the tool prefix and data from the tool return
        # Format: "TOOLCODE: Detailed information..."
        if ":" in tool_return:
            tool_code, tool_data = tool_return.split(":", 1)
            tool_data = tool_data.strip()
            
            # Create a comprehensive response combining both
            summary = f"{original_answer}\n\nBased on your account information: {tool_data}"
        else:
            # If no specific formatting, just append the tool result
            summary = f"{original_answer}\n\nAccount details: {tool_return}"
        
        return summary

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

    DEFAULT_NUMBER_OF_PAIRS = 15

    """Main function with command line interface."""
    parser = argparse.ArgumentParser(description="Generate financial chat Q&A pairs using Azure OpenAI")
    parser.add_argument('-n', '--num-pairs', type=int, default=DEFAULT_NUMBER_OF_PAIRS, 
                       help=f'Number of Q&A pairs to generate (default: {DEFAULT_NUMBER_OF_PAIRS})')
    parser.add_argument('-t', '--topics-file', type=str, default='topics.json',
                       help='Path to topics JSON file (default: topics.json)')
    parser.add_argument('-d', '--deployment', type=str, default='gpt-35-turbo',
                       help='Azure OpenAI deployment name (default: gpt-35-turbo)')
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
