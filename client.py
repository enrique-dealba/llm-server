import requests
import yaml

# Load configurations from config.yaml
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

API_URL = config["api_url"]

def generate_text(prompt):
    payload = {"text": prompt}
    response = requests.post(f"{API_URL}/custom_generate", json=payload)
    return response.json()

if __name__ == "__main__":
    prompt = input("Prompt: ")
    result = generate_text(prompt)
    print(f"LLM Response: {result}")
