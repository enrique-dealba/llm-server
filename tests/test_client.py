import io
import unittest
from unittest.mock import patch

import requests

import client
from config import Settings

settings = Settings()


def mock_post(*args, **kwargs):
    """Mocks external components for testing."""

    class MockResponse:
        def json(self):
            return {"text": "Mocked LLM response", "queries": []}

    return MockResponse()


class TestClient(unittest.TestCase):
    """Tests for client class in client.py.

    Includes tests for various funcs of the Client class, including API interaction,
    error handling, and integration with the TextProcessing utilities.
    """

    def setUp(self):
        """Setup that runs before each test method."""
        self.original_api_url = settings.API_URL
        settings.API_URL = "http://mockapi.test"

        self.test_data = "Test data"
        self.client_instance = client.Client()

        # Patches external dependencies globally for testing
        self.mocked_post = patch("requests.post", side_effect=mock_post).start()

    def tearDown(self):
        """Cleanup after each test func."""
        settings.API_URL = self.original_api_url

        del self.test_data
        del self.client_instance

        # Stops all patches from setUp
        patch.stopall()

    @patch("requests.post", side_effect=mock_post)
    def test_generate_text_success(self, mock_post):
        """Tests generate_text method with successful response."""
        result = self.client_instance.generate_text("Test prompt")
        self.assertIn("Mocked LLM response", result["text"])
        self.assertIsInstance(result, dict)

    @patch("requests.post", side_effect=Exception("API request failed"))
    def test_generate_text_failure(self, mock_post):
        """Tests generate_text method with a failed API request."""
        with self.assertRaises(Exception) as context:
            self.client_instance.generate_text("Test prompt")
        self.assertTrue("API request failed" in str(context.exception))

    @patch("logging.error")
    @patch(
        "requests.post",
        side_effect=requests.exceptions.RequestException("API request failed"),
    )
    def test_generate_text_logging(self, mock_post, mock_logging):
        """Tests if logging.error is called when an API request fails."""
        with self.assertRaises(requests.exceptions.RequestException):
            self.client_instance.generate_text("Test prompt")
        mock_logging.assert_called_with("API request failed: API request failed")


if __name__ == "__main__":
    unittest.main()
