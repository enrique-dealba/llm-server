import math
import os
import requests
import time

from typing import List, Union, Optional
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
    print(f"Tokens: {tokens}, Seconds: {num_seconds}")
    tps = tokens / num_seconds
    return math.floor(tps)

def generate_text(prompt):
    payload = {"text": prompt}
    response = requests.post(f"{API_URL}/generate", json=payload)
    return response.json()

def parse_response(input_string: str) -> Optional[str]:
    """Parses "user" or "|user|" text from Zephyr-7B."""
    keywords = ["user", "|user|"]
    for keyword in keywords:
        keyword_index = input_string.find(keyword)
        if keyword_index != -1:
            return input_string[:keyword_index].strip()
    return input_string

def parse_llm_server(input_data: Union[str, List[str]]) -> str:
    """Parses input data and returns a single string."""
    if isinstance(input_data, list):
        return " ".join(input_data)
    elif isinstance(input_data, str):
        return input_data
    else:
        raise TypeError("Input must be a string or a list of strings.")

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
            # parse_llm is useful when running my_server.py
            # result = parse_llm(result)
            # Parses LLM Server responses for Zephyr-7B
            response = result['text']
            response = parse_llm_server(response)
            response = parse_response(response)

            queries = result['queries']
            print(f"LLM Response: {response}")
            print(f"LLM Prev Queries: {queries}")
            print(f"Tokens per second: {get_tps(response, elapsed_time)} t/s")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
