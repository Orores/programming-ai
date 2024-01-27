import unittest
import requests
from dotenv import load_dotenv
import os
import time  # Import the time module

class TestOpenAIToken(unittest.TestCase):
    def setUp(self):
        # Load environment variables from .env file
        load_dotenv()

    def test_api_token(self):
        # Retrieve your OpenAI API key from the loaded environment variables
        api_key = os.getenv('OPENAI_API_KEY')

        # Ensure the API key is set
        self.assertIsNotNone(api_key, "Please set your OpenAI API key in the .env file.")

        # Add a 5-second delay to avoid rate limiting
        time.sleep(5)  # Delay for 5 seconds

        # Define the endpoint URL for chat completions
        endpoint_url = 'https://api.openai.com/v1/chat/completions'

        # Define a sample conversation
        conversation = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Who won the world series in 2020?"}
        ]

        # Create a dictionary with the conversation and other parameters
        data = {
            "model": "gpt-3.5-turbo",  # Specify the model to use
            "messages": conversation  # Pass the conversation as messages
        }

        # Set up the headers with your API key
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }

        # Make a POST request to the API
        response = requests.post(endpoint_url, headers=headers, json=data)

        # Check if the request was successful (status code 200)
        self.assertEqual(response.status_code, 200, f"API request failed with status code {response.status_code}")

if __name__ == '__main__':
    unittest.main()
