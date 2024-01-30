import unittest
from unittest.mock import patch

import client


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
        self.original_api_url = client.API_URL
        client.API_URL = "http://mockapi.test"

        self.test_data = "Test data"
        self.client_instance = client.Client()

        # Patches external dependencies globally for testing
        self.mocked_post = patch("requests.post", side_effect=mock_post).start()

    def tearDown(self):
        """Cleanup after each test func."""
        client.API_URL = self.original_api_url

        del self.test_data
        del self.client_instance

        # Stops all patches from setUp
        patch.stopall()

    @patch("requests.post", side_effect=mock_post)
    def test_generate_text_success(self, mock_post):
        """Tests generate_text method with successful response."""
        result = client.Client.generate_text("Test prompt")
        self.assertIn("Mocked LLM response", result["text"])
        self.assertIsInstance(result, dict)

    @patch("requests.post", side_effect=Exception("API request failed"))
    def test_generate_text_failure(self, mock_post):
        """Tests generate_text method with a failed API request."""
        with self.assertRaises(Exception) as context:
            client.Client.generate_text("Test prompt")
        self.assertTrue("API request failed" in str(context.exception))


if __name__ == "__main__":
    unittest.main()
