import unittest
from unittest.mock import patch

import client


class TestClient(unittest.TestCase):
    @patch('client.generate_text')
    def test_generate_text_call(self, mock_generate):
        mock_generate.return_value = {"text": "response", "queries": []}
        client.main()
    
    @patch('client.requests.post')
    def test_handle_server_response(self, mock_post):
        mock_post.return_value.json.return_value = {"text": "mocked response", "queries": []}
    
if __name__ == "__main__":
    unittest.main()
