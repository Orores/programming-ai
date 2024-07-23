import unittest
from dotenv import load_dotenv
import os
from AutoChatBot.GPTChatCompletion import GPT3ChatCompletion  # Adjust the import according to your module path

class TestGPT3ChatCompletion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Load environment variables from .env
        load_dotenv()

        # Load the OPENAI_API_KEY from environment variables
        cls.api_key = os.getenv('OPENAI_API_KEY')
        assert cls.api_key is not None, "OPENAI_API_KEY environment variable not set."

        # Define a conversation example to pass
        cls.conversation = [{"role": "user", "content": "Hello, who won the world series in 2020?"}]

        # Make the API request
        cls.response = GPT3ChatCompletion.make_api_request(
            api_key=cls.api_key,
            conversation=cls.conversation,
            model="gpt-3.5-turbo",
            max_tokens=100
        )

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
