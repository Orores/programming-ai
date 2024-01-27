import unittest
from unittest.mock import patch
import os
import requests
import json
from dotenv import load_dotenv
from fuzzywuzzy import fuzz

def load_api_key():
    return os.getenv("OPENAI_API_KEY")

class TestAskOpenAICLI(unittest.TestCase):

    @patch('builtins.print')
    @patch('src.ask_openai_cli_003.requests.post')
    def test_main_function(self, mock_post, mock_print):
        from src.ask_openai_cli_003 import main

        # Load environment variables from .env file
        load_dotenv()

        # Define a mock API response with variable text
        mock_response = requests.Response()
        mock_response.status_code = 200
        mock_response_text = 'The 2020 World Series took place at Globe Life Field in Arlington, Texas.'
        mock_response._content = json.dumps({
            'choices': [
                {
                    'finish_reason': 'stop',
                    'index': 0,
                    'message': {
                        'content': mock_response_text
                    },
                    'logprobs': None
                }
            ],
            'created': 1677664795,
            'id': 'chatcmpl-7QyqpwdfhqwajicIEznoc6Q47XAyW',
            'model': 'gpt-3.5-turbo-0613',
            'object': 'chat.completion',
            'usage': {
                'completion_tokens': 17,
                'prompt_tokens': 57,
                'total_tokens': 74
            }
        }).encode('utf-8')

        # Define the expected response (with variations)
        expected_response = "The 2020 World Series took place at Globe Life Field in Arlington, Texas."

        # Define a matching threshold for fuzzy comparison
        matching_threshold = 80  # You can adjust the threshold as needed

        # Define a mock API request function
        def mock_api_request(*args, **kwargs):
            return mock_response

        # Patch the requests.post function to use the mock API request
        mock_post.side_effect = mock_api_request

        # Set the environment variable for the API key (assuming it's loaded from .env)
        api_key = load_api_key()
        os.environ["OPENAI_API_KEY"] = api_key

        # Execute the main function
        main()

        # Perform a fuzzy comparison and assert that it's above the threshold
        similarity_score = fuzz.partial_ratio(expected_response, mock_response_text)
        self.assertGreaterEqual(similarity_score, matching_threshold,
                                f"API response similarity score ({similarity_score}) is below the threshold.")

        # Check if the expected output is printed with comma separation
        mock_print.assert_called_with("Assistant's reply:", mock_response_text)

if __name__ == "__main__":
    unittest.main()
