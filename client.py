import math
import os
import requests
import time

from typing import List, Union
from dotenv import load_dotenv
import tiktoken

load_dotenv()

API_URL = os.getenv("API_URL")

def num_tokens(string: str, encoding_name: str = "cl100k_base") -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def concatenate_strings(responses: List[str]) -> str:
    if isinstance(responses, list) and all(isinstance(item, str) for item in responses):
        return " ".join(responses)
    # Raise an error for invalid input types
    raise TypeError("Input must be a list of strings")

def get_tps(response: Union[str, List[str]], num_seconds):
    """Returns token per second (tps) performance for LLM."""
    if isinstance(response, list):
        response = concatenate_strings(response)
    
    tokens = num_tokens(response)
    tps = tokens / num_seconds
    return math.floor(tps)

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
    while True:
        prompt = input("Prompt: ")
        if prompt.lower() in ["quit", "exit"]:
            print("Exiting the conversation.")
            break
        
        try:
            start_time = time.time()
            result = generate_text(prompt)
            end_time = time.time()
            elapsed_time = end_time - start_time
            # result = parse_llm(result)
            response = result['text']
            queries = result['queries']
            print(f"LLM Response: {response}")
            print(f"LLM Queries: {queries}")
            print(f"Tokens per second: {get_tps(response, elapsed_time)} t/s")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
