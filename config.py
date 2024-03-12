"""Config settings for LLMs and server parameters."""

from pydantic import BaseSettings, Field


# ----- Config Settings -----
class Settings(BaseSettings):
    # ----- LLM -----
    DEFAULT_MODEL: str = Field(
        default="mistralai/Mistral-7B-Instruct-v0.1",
        description="Default LLM model to use"
    )

    # ----- Constants -----
    NUM_GPUS: int = Field(
        default=1,
        description="Number of GPUs to use"
    )
    NUM_RESPONSES: int = Field(
        default=1,
        description="Number of responses to generate"
    )
    MAX_TOKENS: int = Field(
        default=512,
        description="Maximum number of tokens per response"
    )
    MAX_SEQ_LEN: int = Field(
        default=16384,
        description="Maximum sequence length"
    )
    TEMPERATURE: float = Field(
        default=0.2,
        description="Temperature for text generation"
    )
    TOP_P: float = Field(
        default=0.95,
        description="Top-p sampling value (must be in (0, 1])"
    )
    API_URL: str = Field(
        default="http://localhost:8888",
        description="URL for the FastAPI"
    )

    # ----- GPU Utilization Settings -----
    DEFAULT_GPU_UTIL: float = Field(
        default=0.30,
        description="Default GPU utilization (works for 7B models)"
    )
    AWQ_GPU_UTIL: float = Field(
        default=0.50,
        description="Minimum GPU utilization for 7B AWQ models"
    )
    GPTQ_GPU_UTIL: float = Field(
        default=0.25,
        description="Minimum GPU utilization for 7B GPTQ models"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# ----- Model Names -----
class LLM:
    """HuggingFace models.

    The models below can be used for the DEFAULT_MODEL.
    """

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
    PHI_2_ORANGE = "rhysjones/phi-2-orange"
