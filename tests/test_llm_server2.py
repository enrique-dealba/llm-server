import unittest
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient
from langchain.llms import VLLM

from config import Settings
from llm_agent.llm_memory import MemoryLLM
from llm_server import create_llm, app


settings = Settings()


class VLLMMock:
    """Mocks for external dependencies."""

    def __init__(self, **kwargs):
        """Initializes mock with given kwargs."""
        print("VLLMMock initialized with kwargs:", kwargs)

    def __call__(self, query):
        """Returns mocked response when the mock is called."""
        print("VLLMMock called with query:", query)
        return "mocked response"


class TestConfig(unittest.TestCase):
    """Test cases for the Config class."""

    def setUp(self):
        """Set up the test environment."""
        # Patch the VLLM class to avoid actual initialization
        self.vllm_patcher = patch("llm_server.VLLM")
        self.mock_vllm = self.vllm_patcher.start()
        self.mock_vllm.return_value = MagicMock(spec=VLLM)

    def tearDown(self):
        """Clean up the test environment."""
        # Stop the VLLM patcher
        self.vllm_patcher.stop()

    @patch("huggingface_hub.snapshot_download")
    def test_create_llm(self, mock_snapshot_download):
        """Ensures create_llm method correctly creates VLLM instance."""
        mock_snapshot_download.return_value = "/mock/path/to/model"

        llm = create_llm(quantization=None, use_agent=False)

        self.assertIsInstance(llm, MagicMock)
        self.mock_vllm.assert_called_once()

    @patch("huggingface_hub.snapshot_download")
    def test_create_llm_with_agent(self, mock_snapshot_download):
        """Directly tests create_llm with LLM agent paradigm."""
        mock_snapshot_download.return_value = "/mock/path/to/model"

        llm = create_llm(quantization=None, use_agent=True)

        self.assertIsInstance(llm, MemoryLLM)
        self.mock_vllm.assert_called_once()
