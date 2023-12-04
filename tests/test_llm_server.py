import os
import unittest

from fastapi.testclient import TestClient

from llm_server import Config, app


class TestLLMServer(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
    
    def test_generate_endpoint(self):
        response = self.client.post("/generate", json={"text": "Hello"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("text", response.json())
    
    def test_config_defaults(self):
        config = Config()
        self.assertEqual(config.llm_model, "mistralai/Mistral-7B-Instruct-v0.1")

    def test_config_env_override(self):
        os.environ["MODEL"] = "test_model"
        config = Config()
        self.assertEqual(config.llm_model, "test_model")
        del os.environ["MODEL"]

if __name__ == "__main__":
    unittest.main()
