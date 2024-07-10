"""Config settings for LLMs and server parameters."""

from pydantic_settings import BaseSettings


# ----- Config Settings -----
class Settings(BaseSettings):
    # ----- LLM -----
    DEFAULT_MODEL: str = "TheBloke/Mistral-7B-Instruct-v0.2-GPTQ"

    # ----- Constants -----
    NUM_GPUS: int = 1
    NUM_RESPONSES: int = 1
    MAX_TOKENS: int = 512
    MAX_SEQ_LEN: int = 16384
    TEMPERATURE: float = 0.0
    TOP_P: float = 0.95
    API_URL: str = "http://localhost:8888"

    # ----- GPU Utilization Settings -----
    DEFAULT_GPU_UTIL: float = 1.00
    AWQ_GPU_UTIL: float = 1.00 # before: 0.50, 0.60
    GPTQ_GPU_UTIL: float = 1.00 # before: 0.25, 0.45

    # ----- LLM Agent Settings -----
    USE_AGENT: bool = False
    LLM_AGENT: str = "LLMRouter"  # Default agent

    # ----- Hugging Face Hub Settings -----
    HF_HUB_OFFLINE: bool = False

    # ----- IF USING MISTRAL MODELS -----
    MISTRAL_MODELS: list[str] = [
        "mistralai/Mistral-7B-Instruct-v0.2",
        "TheBloke/Mistral-7B-Instruct-v0.2-AWQ",
        "TheBloke/Mistral-7B-Instruct-v0.2-GPTQ",
        "mistralai/Mistral-7B-Instruct-v0.1",
        "TheBloke/Mistral-7B-Instruct-v0.1-AWQ",
        "TheBloke/Mistral-7B-v0.1-GPTQ",
    ]
    USE_MISTRAL: bool = bool(DEFAULT_MODEL in MISTRAL_MODELS)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


# ----- Model Names -----
class LLM:
    """HuggingFace models.

    The models below can be used for the DEFAULT_MODEL.
    """

    OPT_125M = "facebook/opt-125m"
    # MISTRAL_7B = "mistralai/Mistral-7B-Instruct-v0.1"
    # MISTRAL_CPU = "TheBloke/Mistral-7B-Instruct-v0.1-GGUF"  # Has issues
    # MISTRAL_AWQ = "TheBloke/Mistral-7B-Instruct-v0.1-AWQ"
    # MISTRAL_GPTQ = "TheBloke/Mistral-7B-v0.1-GPTQ"
    MISTRAL_V2 = "mistralai/Mistral-7B-Instruct-v0.2"
    MISTRAL_V2_AWQ = "TheBloke/Mistral-7B-Instruct-v0.2-AWQ"
    MISTRAL_V2_GPTQ = "TheBloke/Mistral-7B-Instruct-v0.2-GPTQ"
    MIXTRAL_GPTQ = "TheBloke/Mixtral-8x7B-v0.1-GPTQ"
    DOLPHIN_GPTQ = "TheBloke/dolphin-2.5-mixtral-8x7b-GPTQ"
    ZEPHYR_7B = "HuggingFaceH4/zephyr-7b-beta"
    HERMES_2_5 = "teknium/OpenHermes-2.5-Mistral-7B"
    HERMES_AWQ = "TheBloke/OpenHermes-2.5-Mistral-7B-AWQ"
    HERMES_GPTQ = "TheBloke/OpenHermes-2.5-Mistral-7B-GPTQ"
    HERMES_PRO = "NousResearch/Hermes-2-Pro-Mistral-7B"
    YARN_64K = "NousResearch/Yarn-Mistral-7b-64k"
    YARN_128K = "NousResearch/Yarn-Mistral-7b-128k"
    PHI_2 = "microsoft/phi-2"
    PHI_2_GPTQ = "TheBloke/phi-2-GPTQ"
    DOLPHIN_26_PHI = "cognitivecomputations/dolphin-2_6-phi-2"  # doesn't work with vLLM
    DOLPHIN_26_PHI_GPTQ = "TheBloke/dolphin-2_6-phi-2-GPTQ"  # doesn't work with vLLM
    PHI_2_ORANGE = "rhysjones/phi-2-orange"  # doesn't work with vLLM
