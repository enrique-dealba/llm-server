import re
from typing import List, Union

import tiktoken


class TextProcessing:
    """For text processing operations.
    
    Includes tokenization, cleaning, parsing, and concatenation.
    """
    @staticmethod
    def num_tokens(string: str, encoding_name: str = "cl100k_base") -> int:
        """Counts the number of tokens in a string based on a specified encoding."""
        encoding = tiktoken.get_encoding(encoding_name)
        return len(encoding.encode(string))

    @staticmethod
    def clean_text(input_text: str) -> str:
        """Cleans text by removing specific characters and whitespace."""
        cleaned_text = input_text.strip("<|>")
        cleaned_text = re.sub(r"\s+", " ", cleaned_text).strip()
        for punct in [".", ",", "?", "!"]:
            cleaned_text = cleaned_text.replace(f" {punct}", punct)
        return cleaned_text

    @staticmethod
    def parse_response(input_string: str) -> str:
        """Parses response to extract text before a set of keywords."""
        keywords = ["[/user]", "|user|", "user", "[/USER]", "USER"]
        for keyword in keywords:
            keyword_index = input_string.find(keyword)
            if keyword_index != -1:
                return input_string[:keyword_index].strip()
        return input_string

    @staticmethod
    def concatenate_strings(responses: List[str]) -> str:
        """Concatenates list of strings into single string."""
        if isinstance(responses, list) and all(
            isinstance(item, str) for item in responses
        ):
            return " ".join(responses)
        raise TypeError("Input must be a list of strings")

    @staticmethod
    def parse_llm_server(input_data: Union[str, List[str]]) -> str:
        """Parses input data from LLM server."""
        if isinstance(input_data, list):
            return " ".join(input_data)
        elif isinstance(input_data, str):
            return input_data
        else:
            raise TypeError("Input must be a string or a list of strings.")
        
    @staticmethod
    def measure_performance(start_time, end_time, response_text):
        """Calculates the tokens per second (tps) performance of a text response."""
        elapsed_time = end_time - start_time
        tokens = TextProcessing.num_tokens(response_text)
        tps = float(tokens) / float(elapsed_time)
        return tps
