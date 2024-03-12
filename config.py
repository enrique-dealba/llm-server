"""Config settings for LLMs and server parameters."""

# ----- LLM -----
DEFAULT_MODEL = "cognitivecomputations/dolphin-2_6-phi-2"

# ----- Constants -----
NUM_GPUS = 1
NUM_RESPONSES = 1
MAX_TOKENS = 512
MAX_SEQ_LEN = 16384
TEMPERATURE = 0.2
TOP_P = 0.95  # Must be in (0, 1] - set to 1 to consider all tokens
API_URL = "http://localhost:8888"

# ----- GPU Utilization Settings -----
DEFAULT_GPU_UTIL = 0.30  # works for 7B models, 0.25 for 7B
AWQ_GPU_UTIL = 0.50  # min needed for 7B AWQ models, 0.31 for 7B AWQ
GPTQ_GPU_UTIL = 0.25  # min needed for 7B GPTQ models, 0.5 for 7B GPTQ (.15->.25)


# ----- Model Names -----
class LLM:
    """HuggingFace models."""

    OPT_125M = "facebook/opt-125m"
    MISTRAL_7B = "mistralai/Mistral-7B-Instruct-v0.1"
    MISTRAL_CPU = "TheBloke/Mistral-7B-Instruct-v0.1-GGUF"  # Has issues
    MISTRAL_AWQ = "TheBloke/Mistral-7B-Instruct-v0.1-AWQ"
    MISTRAL_GPTQ = "TheBloke/Mistral-7B-v0.1-GPTQ"
    MISTRAL_V2 = "mistralai/Mistral-7B-Instruct-v0.2"
    MISTRAL_V2_AWQ = "TheBloke/Mistral-7B-Instruct-v0.2-AWQ"
    MISTRAL_V2_GPTQ = "TheBloke/Mistral-7B-Instruct-v0.2-GPTQ"
    MIXTRAL_GPTQ = "TheBloke/Mixtral-8x7B-v0.1-GPTQ"
    DOLPHIN_GPTQ = "TheBloke/dolphin-2.5-mixtral-8x7b-GPTQ"
    ZEPHYR_7B = "HuggingFaceH4/zephyr-7b-beta"
    HERMES_2_5 = "teknium/OpenHermes-2.5-Mistral-7B"
    HERMES_AWQ = "TheBloke/OpenHermes-2.5-Mistral-7B-AWQ"
    HERMES_GPTQ = "TheBloke/OpenHermes-2.5-Mistral-7B-GPTQ"
    YARN_64K = "NousResearch/Yarn-Mistral-7b-64k"
    YARN_128K = "NousResearch/Yarn-Mistral-7b-128k"
    PHI_2 = "microsoft/phi-2"
    PHI_2_GPTQ = "TheBloke/phi-2-GPTQ"
    DOLPHIN_26_PHI = "cognitivecomputations/dolphin-2_6-phi-2"
    DOLPHIN_26_PHI_GPTQ = "TheBloke/dolphin-2_6-phi-2-GPTQ"  # doesn't work with vLLM
