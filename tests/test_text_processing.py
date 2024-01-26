import unittest
from datetime import datetime
from unittest.mock import patch

from text_processing import TextProcessing as tp


class TestTextProcessing(unittest.TestCase):
    """Unit tests for TextProcessing.

    Covers methods like num_tokens, clean_text, parse_response, concatenate_strings,
    parse_llm_server, and measure_performance.
    """

    def test_num_tokens_normal(self):
        """Test num_tokens with a typical string."""
        with patch("tiktoken.get_encoding") as mock_encoding:
            mock_encoding.return_value.encode.return_value = ["tok_1", "tok_2", "tok_3"]
            result = tp.num_tokens("Test string")
            self.assertEqual(result, 3)

    def test_num_tokens_empty_string(self):
        """Test num_tokens with an empty string."""
        with patch("tiktoken.get_encoding") as mock_encoding:
            mock_encoding.return_value.encode.return_value = []
            result = tp.num_tokens("")
            self.assertEqual(result, 0)

    def test_clean_text_normal(self):
        """Test clean_text with a typical string."""
        result = tp.clean_text("  Hello, World!  ")
        self.assertEqual(result, "Hello, World!")

    def test_clean_text_special_chars(self):
        """Test clean_text with special characters."""
        result = tp.clean_text("<|Hello... World??|>")
        self.assertEqual(result, "Hello... World??")

    def test_clean_text_empty_string(self):
        """Test clean_text with an empty string."""
        result = tp.clean_text(" ")
        self.assertEqual(result, "")

    def test_parse_response_with_keywords(self):
        """Test parse_response with input containing keywords."""
        result = tp.parse_response("Text here. [/user]")
        self.assertEqual(result, "Text here.")

        result = tp.parse_response("Text here: |user|")
        self.assertEqual(result, "Text here:")

    def test_parse_response_without_keywords(self):
        """Test parse_response with input not containing keywords."""
        result = tp.parse_response("No keywords here")
        self.assertEqual(result, "No keywords here")

    def test_parse_response_empty_string(self):
        """Test parse_response with an empty string."""
        result = tp.parse_response("")
        self.assertEqual(result, "")

    def test_concatenate_strings_normal(self):
        """Test concatenate_strings with typical list of strings."""
        result = tp.concatenate_strings(["Taco", "Cat"])
        self.assertEqual(result, "Taco Cat")

    def test_concatenate_strings_empty_list(self):
        """Test concatenate_strings with an empty list."""
        result = tp.concatenate_strings([])
        self.assertEqual(result, "")

    def test_concatenate_strings_non_string_elements(self):
        """Test concatenate_strings with non-string elements."""
        with self.assertRaises(TypeError):
            tp.concatenate_strings(["A", 123, "B"])

    def test_concatenate_strings_non_list_input(self):
        """Test concatenate_strings with non-list input."""
        with self.assertRaises(TypeError):
            tp.concatenate_strings("Non list")

    def test_parse_llm_server_with_string(self):
        """Test parse_llm_server with string input."""
        result = tp.parse_llm_server("Test string")
        self.assertEqual(result, "Test string")

    def test_parse_llm_server_with_list(self):
        """Test parse_llm_server with list input."""
        result = tp.parse_llm_server(["Test", "string"])
        self.assertEqual(result, "Test string")

    def test_parse_llm_server_invalid_input(self):
        """Test parse_llm_server with invalid input type."""
        with self.assertRaises(TypeError):
            tp.parse_llm_server(123)

    @patch("text_processing.TextProcessing.num_tokens")
    def test_measure_performance(self, mock_num_tokens):
        """Mock num_tokens to return a fixed value."""
        mock_num_tokens.return_value = 10

        start_time = datetime(2024, 1, 1, 12, 0, 0)
        end_time = datetime(2024, 1, 1, 12, 0, 10)  # 10 seconds later

        tps = tp.measure_performance(start_time, end_time, "Test string")
        self.assertEqual(tps, 1.0)


if __name__ == "__main__":
    unittest.main()
