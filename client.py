import requests
from dotenv import load_dotenv
import os

# Load configurations from .env file
load_dotenv()

API_URL = os.getenv("API_URL")

def generate_text(prompt):
    payload = {"text": prompt}
    response = requests.post(f"{API_URL}/generate", json=payload)
    return response.json()

def parse_llm(response):
    print(type(response))
    return response

def parse_llm(response):
    raw_text = response.get('text', [])
    if not raw_text:
        return "No response from LLM."
    
    raw_text = ' '.join(raw_text)  # Join list to a single string if needed
    lines = raw_text.split('\n')  # Split by newline to get individual lines
    parsed_str = "\n".join([line.strip() for line in lines])
    
    return parsed_str.strip()

if __name__ == "__main__":
    prompt = input("Prompt: ")
    result = generate_text(prompt)
    result = parse_llm(result)
    print(f"LLM Response: {result}")
