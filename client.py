import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_URL = os.getenv("API_URL")

def generate_text(prompt):
    payload = {"text": prompt}
    response = requests.post(f"{API_URL}/generate", json=payload)
    return response.json()

def parse_llm(response):
    raw_text = response.get('text', [])
    if not raw_text:
        return "No response from LLM."
    
    raw_text = ' '.join(raw_text)
    lines = raw_text.split('\n')
    parsed_str = "\n".join([line.strip() for line in lines])

    return parsed_str.strip()

if __name__ == "__main__":
    prompt = input("Prompt: ")
    result = generate_text(prompt)
    result = parse_llm(result)
    print(f"LLM Response: {result}")
