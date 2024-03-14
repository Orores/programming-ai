import unittest
from unittest.mock import patch
import os
import requests
import json
from dotenv import load_dotenv
from fuzzywuzzy import fuzz
from src.ask_openai_cli_003 import OpenAIAssistant  # Update the import to use the class

class TestOpenAIAssistant(unittest.TestCase):

    @patch('src.ask_openai_cli_003.requests.post')
    def test_ask_question_method(self, mock_post):
        # Define a mock API response
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
            ]
        }).encode('utf-8')
        mock_post.return_value = mock_response

        # Create an instance of OpenAIAssistant
        assistant = OpenAIAssistant()
        response = assistant.ask_question("Your question goes here.")  # Provide the question you want to test

        # Define the expected response and a matching threshold for fuzzy comparison
        expected_response = mock_response_text
        matching_threshold = 80

        # Perform a fuzzy comparison and assert that it's above the threshold
        similarity_score = fuzz.partial_ratio(expected_response, response)
        self.assertGreaterEqual(similarity_score, matching_threshold,
                                f"API response similarity score ({similarity_score}) is below the threshold.")

        # Check if the expected output is returned as the response
        self.assertEqual(response, expected_response)

    @patch('src.ask_openai_cli_003.load_dotenv')  # Mock load_dotenv to avoid actually loading .env file in tests
    def test_real_api_call(self, mock_load_dotenv):
        # Prevent the actual loading of environment variables
        mock_load_dotenv.return_value = None

        # Assuming the API key is set manually for the test, or use another way to inject the API key
        assistant = OpenAIAssistant()
        assistant.api_key = 'your_test_api_key_here'  # Replace with a valid API key or mock method

        response = assistant.ask_question("What is the capital of France?")  # Question about the capital of France

        # Ensure that a real API response is received (status code 200)
        self.assertIsInstance(response, str, "Response should be a string")
        self.assertIn("Paris", response, "Response should contain 'Paris'")

if __name__ == "__main__":
    unittest.main()
