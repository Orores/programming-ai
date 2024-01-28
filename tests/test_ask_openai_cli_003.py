import unittest
from unittest.mock import patch
import os
import requests
import json
from dotenv import load_dotenv
from fuzzywuzzy import fuzz
from src.ask_openai_cli_003 import ask_question

class TestAskOpenAICLI(unittest.TestCase):

    @patch('src.ask_openai_cli_003.requests.post')
    def test_ask_question_function(self, mock_post):
        # Load environment variables from .env file
        load_dotenv()

        # Define a mock API response with variable text (similar to your previous test)
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

        # Execute the ask_question function and capture the response
        response = ask_question("Your question goes here.")  # Provide the question you want to test

        # Perform a fuzzy comparison and assert that it's above the threshold
        similarity_score = fuzz.partial_ratio(expected_response, response)
        self.assertGreaterEqual(similarity_score, matching_threshold,
                                f"API response similarity score ({similarity_score}) is below the threshold.")

        # Check if the expected output is returned as the response
        self.assertEqual(response, expected_response)

    def test_real_api_call(self):
        load_dotenv()  # Load environment variables from .env file
        api_key = os.getenv("OPENAI_API_KEY")

        # Execute the ask_question function and capture the response
        response = ask_question("What is the capital of France?")  # Question about the capital of France

        # Ensure that a real API response is received (status code 200)
        self.assertIsInstance(response, str, "Response should be a string")
        self.assertIn("Paris", response, "Response should contain 'Paris' or 'paris'")

if __name__ == "__main__":
    unittest.main()
