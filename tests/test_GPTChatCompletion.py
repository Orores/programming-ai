import unittest
from dotenv import load_dotenv
import os
from AutoChatBot.GPTChatCompletion import GPT3ChatCompletion

class TestGPT3ChatCompletion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Load environment variables from .env
        load_dotenv()

        # Prepare chat_parameters dictionary as described in AutoChatBot/default_api_parameters.py
        cls.chat_parameters = {
            "model": "gpt-3.5-turbo",
            "temperature": 1.0,
            "max_tokens": 64,
            "top_p": 1.0,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0,
            "stop_sequences": None
        }

        # Define a conversation example to pass
        cls.conversation = [{"role": "user", "content": "Hello, who won the world series in 2020?"}]

        # Make the API request
        cls.response = GPT3ChatCompletion.make_api_request(
            cls.chat_parameters,
            cls.conversation
        )

    def test_response_contains_choices(self):
        self.assertIn('choices', self.response, msg=f"The response does not contain 'choices'. Full response: {self.response}")

    def test_choices_is_list(self):
        self.assertIsInstance(self.response['choices'], list, f"'choices' is not a list. Full response: {self.response}")

    def test_choice_contains_message(self):
        if self.response['choices']:
            choice = self.response['choices'][0]
            self.assertIn('message', choice, f"The choice does not contain 'message'. Full response: {self.response}")

    def test_message_contains_role_and_content(self):
        if self.response['choices']:
            message = self.response['choices'][0].get('message', {})
            self.assertIn('role', message, f"'message' does not contain 'role'. Full response: {self.response}")
            self.assertIn('content', message, f"'message' does not contain 'content'. Full response: {self.response}")

    def test_extract_text_from_response(self):
        text = GPT3ChatCompletion.extract_text_from_response(self.response)
        self.assertIsInstance(text, str, "The extracted text should be a string.")
        self.assertGreater(len(text), 0, "The extracted text should not be empty.")

    def test_extract_text_from_response_invalid_response(self):
        invalid_response = {}
        with self.assertRaises(ValueError, msg="Invalid response format"):
            GPT3ChatCompletion.extract_text_from_response(invalid_response)

if __name__ == '__main__':
    unittest.main()

