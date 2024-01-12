DEFAULT_MODEL = "mistralai/Mistral-7B-Instruct-v0.1"
DEFAULT_GPU_UTIL = 0.25 # gpu_memory_utilization=0.25 works for 7B models
AWQ_GPU_UTIL = 0.31 # min needed for 7B AWQ models

"""
--- Choose from following models ---

## vLLM Models:
opt_model: str = "facebook/opt-125m"
mistral_model: str = "mistralai/Mistral-7B-Instruct-v0.1"
mistral_cpu: str = "TheBloke/Mistral-7B-Instruct-v0.1-GGUF" # Doesn't work
mistral_awq: str = "TheBloke/Mistral-7B-Instruct-v0.1-AWQ"
mistral_gptq: str = "TheBloke/Mistral-7B-v0.1-GPTQ"
zephyr_model: str = "HuggingFaceH4/zephyr-7b-beta"
hermes_model: str = "teknium/OpenHermes-2.5-Mistral-7B"
hermes_awq: sre = "TheBloke/OpenHermes-2.5-Mistral-7B-AWQ"

## LLM Server Models:
self.opt_model: str = "facebook/opt-125m"
self.mistral_model: str = "mistralai/Mistral-7B-Instruct-v0.1"
self.mistral_cpu: str = "TheBloke/Mistral-7B-Instruct-v0.1-GGUF"
self.zephyr_model: str = "HuggingFaceH4/zephyr-7b-beta"
self.hermes_model: str = "teknium/OpenHermes-2.5-Mistral-7B"
self.yarn_64k_model: str = "NousResearch/Yarn-Mistral-7b-64k"
self.yarn_128k_model: str = "NousResearch/Yarn-Mistral-7b-128k"

"""

NUM_RESPONSES = 1
MAX_TOKENS = 512
TEMPERATURE = 0.2
TOP_P = 0.95 # Must be in (0, 1] - set to 1 to consider all tokens
API_URL = "http://localhost:8888"
