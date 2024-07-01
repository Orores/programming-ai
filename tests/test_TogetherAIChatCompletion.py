import unittest
from dotenv import load_dotenv
import os
import sys

# Add the src directory to the Python path for imports
sys.path.append('AutoChatBot')

from TogetherAIChatCompletion import TogetherAIChatCompletion

class TestTogetherAIChatCompletion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Load environment variables from .env
        load_dotenv()

        # Load the TOGETHERAI_API_KEY from environment variables
        api_key = os.getenv('TOGETHERAI_API_KEY')
        assert api_key is not None, "TOGETHERAI_API_KEY environment variable not set."

        # Initialize the TogetherAIChatCompletion with desired parameters
        cls.chat_completion = TogetherAIChatCompletion(api_key=api_key, model="cognitivecomputations/dolphin-2.5-mixtral-8x7b", max_tokens=2000)

        # Define a conversation example to pass
        cls.conversation = [
            {"role": "user", "content": "Hello, who won the world series in 2020?"}
        ]

        # Make the API request
        cls.response = cls.chat_completion.make_api_request(cls.conversation)

    def test_response_is_dict(self):
        # Check if the response is a dictionary
        self.assertIsInstance(self.response, dict, "The response is not a dictionary")

    def test_response_contains_choices(self):
        # Check if the response contains 'choices'
        self.assertIn('choices', self.response, msg=f"The response does not contain 'choices'. Full response: {self.response}")

    def test_choices_is_list(self):
        # Validate that 'choices' is a list
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
