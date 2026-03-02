from openai import OpenAI
import os
import ssl
import httpx
import urllib3
from dotenv import load_dotenv

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Disable SSL verification globally
ssl._create_default_https_context = ssl._create_unverified_context

load_dotenv()

# Create HTTP client with SSL verification disabled
http_client = httpx.Client(verify=False)

client = OpenAI(
    base_url="https://openrouter.io/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    http_client=http_client
)

resp = client.chat.completions.create(
    model="deepseek/deepseek-v3.2-speciale",
    messages=[
        {"role": "user", "content": "Write a short story about a time-traveling violinist."}
    ]
)

print(resp.choices[0].message["content"])