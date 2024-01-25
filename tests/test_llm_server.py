import unittest
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from llm_server import Config, app


class VLLMMock:
    """Mocks for external dependencies."""
    
    def __init__(self, **kwargs):
        print("VLLMMock initialized with kwargs:", kwargs)
        pass

    def __call__(self, query):
        print("VLLMMock called with query:", query)
        # Mock the behavior of the LLM as it would in the actual endpoint
        return "mocked response"  # Ensure this matches the actual endpoint's behavior


# Test cases for the Config class
class TestConfig(unittest.TestCase):
    def test_init(self):
        """Test initialization of Config."""
        config = Config()
        self.assertEqual(config.llm_model, "mistralai/Mistral-7B-Instruct-v0.1")
        self.assertEqual(config.num_gpus, 1)

    def test_create_llm(self):
        """Test the create_llm method."""
        config = Config()
        with patch("llm_server.VLLM", new=VLLMMock):
            llm = config.create_llm(quantization=None)
            self.assertIsInstance(llm, VLLMMock)


class TestFastAPIEndpoints(unittest.TestCase):
    """Test cases for FastAPI endpoints."""

    def setUp(self):
        self.client = TestClient(app)
        print("TestClient for app initialized")

    def test_generate_endpoint(self):
        """Test the /generate endpoint."""
        with patch("llm_server.get_llm", return_value=VLLMMock()) as mock_get_llm:
            print("Patching get_llm with VLLMMock")
            response = self.client.post("/generate", json={"text": "test query"})
            print("Response status code:", response.status_code)
            print("Response JSON:", response.json())

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {"text": "mocked response"})
            mock_get_llm.assert_called_once()


if __name__ == "__main__":
    unittest.main()
