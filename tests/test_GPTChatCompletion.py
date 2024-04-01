import unittest
from dotenv import load_dotenv
import os
import sys

# Add the src directory to the Python path for imports
sys.path.append('src')

from GPTChatCompletion import GPT3ChatCompletion

class TestGPT3ChatCompletion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Load environment variables from .env
        load_dotenv()

        # Load the OPENAI_API_KEY from environment variables
        api_key = os.getenv('OPENAI_API_KEY')
        assert api_key is not None, "OPENAI_API_KEY environment variable not set."

        # Initialize the GPT3ChatCompletion with desired parameters
        cls.chat_completion = GPT3ChatCompletion(api_key=api_key, model="gpt-3.5-turbo", max_tokens=2000)

        # Define a conversation example to pass
        conversation = [{"role": "user", "content": "Hello, who won the world series in 2020?"}]

        # Make the API request
        cls.response = cls.chat_completion.make_api_request(conversation)

    def test_response_contains_choices(self):
        # Check if the API call was successful
        self.assertIn('choices', self.response, msg=f"The response does not contain 'choices'. Full response: {self.response}")

    def test_choices_is_list(self):
        # Validate the 'choices' is a list
        self.assertIsInstance(self.response['choices'], list, f"'choices' is not a list. Full response: {self.response}")

    def test_choice_contains_message(self):
        # Check if the first choice contains a 'message'
        if self.response['choices']:
            choice = self.response['choices'][0]
            self.assertIn('message', choice, f"The choice does not contain 'message'. Full response: {self.response}")

    def test_message_contains_role_and_content(self):
        # Check if the 'message' contains both 'role' and 'content'
        if self.response['choices']:
            message = self.response['choices'][0].get('message', {})
            self.assertIn('role', message, f"'message' does not contain 'role'. Full response: {self.response}")
            self.assertIn('content', message, f"'message' does not contain 'content'. Full response: {self.response}")

if __name__ == '__main__':
    unittest.main()

