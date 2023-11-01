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

if __name__ == "__main__":
    prompt = input("Prompt: ")
    result = generate_text(prompt)
    result = parse_llm(result)
    print(f"LLM Response: {result}")
