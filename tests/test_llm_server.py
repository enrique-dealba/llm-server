import unittest
from unittest.mock import MagicMock, patch

from fastapi import HTTPException
from fastapi.testclient import TestClient

from llm_server import Config, app, get_llm


class VLLMMock:
    """Mocks for external dependencies."""

    def __init__(self, **kwargs):
        print("VLLMMock initialized with kwargs:", kwargs)

    def __call__(self, query):
        print("VLLMMock called with query:", query)
        return "mocked response"


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
        global llm
        with patch("llm_server.llm", new=VLLMMock()):  # Patch llm
            print("Patching llm with VLLMMock")
            response = self.client.post("/generate", json={"text": "test query"})
            print("Response status code:", response.status_code)
            print("Response JSON:", response.json())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {"text": "mocked response"})


class TestConfigCreateLLM(unittest.TestCase):
    def setUp(self):
        self.config = Config()  # Initialize Config object

    @patch("llm_server.VLLM")  # Mock the VLLM class
    def test_create_llm_exception(self, mock_vllm):
        mock_vllm.side_effect = Exception("Test Exception")
        with self.assertRaises(RuntimeError) as context:
            self.config.create_llm()
        self.assertIn(
            "Failed to initialize LLM: Test Exception", str(context.exception)
        )


class TestGetLLM(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch("llm_server.get_llm_instance")
    def test_get_llm_exception(self, mock_get_llm_instance):
        mock_get_llm_instance.side_effect = Exception("Test Exception")
        print("Patching get_llm_instance to raise an exception")
        response = self.client.post("/generate", json={"text": "test query"})
        print("TestGetLLM - Response status code:", response.status_code)
        print("TestGetLLM - Response JSON:", response.json())
        self.assertEqual(response.status_code, 500)
        self.assertIn("Test Exception", response.json()["detail"])


class TestGenerateEndpoint(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_generate_exception_on_llm_call(self):
        global llm
        with patch(
            "llm_server.llm", new=MagicMock(side_effect=Exception("LLM Exception"))
        ):
            print("Patching llm with a mock that raises an exception")
            response = self.client.post("/generate", json={"text": "test query"})
            print("TestGenerateEndpoint - Response status code:", response.status_code)
            print("TestGenerateEndpoint - Response JSON:", response.json())
            self.assertEqual(response.status_code, 400)
            self.assertIn("LLM Exception", response.json()["detail"])

    @patch("llm_server.Request.json", side_effect=Exception("JSON Exception"))
    def test_generate_exception_on_request_json(self, mock_request_json):
        response = self.client.post("/generate", json={"text": "test query"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("JSON Exception", response.json()["detail"])


if __name__ == "__main__":
    unittest.main()
