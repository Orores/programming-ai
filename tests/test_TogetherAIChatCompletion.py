import unittest
from dotenv import load_dotenv
import os
from AutoChatBot.TogetherAIChatCompletion import TogetherAIChatCompletion

class TestTogetherAIChatCompletion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Load environment variables from .env
        load_dotenv()

        # Prepare chat_parameters dictionary as described in AutoChatBot/default_api_parameters.py
        cls.chat_parameters = {
            "model": "cognitivecomputations/dolphin-2.5-mixtral-8x7b",
            "temperature": 1.0,
            "max_tokens": 128,
            "top_p": 0.7,
            "top_k": 50,
            "repetition_penalty": 1.0,
            "stop_sequences": None
        }

        # Define a conversation example to pass
        cls.conversation = [
            {"role": "user", "content": "Hello, who won the world series in 2020?"}
        ]

        # Make the API request
        cls.response = TogetherAIChatCompletion.make_api_request(
            cls.chat_parameters,
            cls.conversation
        )

    def test_response_is_dict(self):
        self.assertIsInstance(self.response, dict, "The response is not a dictionary")

    def test_response_contains_error_or_choices(self):
        self.assertTrue('choices' in self.response or 'error' in self.response, 
                        msg=f"The response does not contain 'choices' or 'error'. Full response: {self.response}")

    def test_choices_is_list(self):
        if 'choices' in self.response:
            self.assertIsInstance(self.response['choices'], list, f"'choices' is not a list. Full response: {self.response}")

    def test_choice_contains_message(self):
        if 'choices' in self.response and self.response['choices']:
            choice = self.response['choices'][0]
            self.assertIn('message', choice, f"The choice does not contain 'message'. Full response: {self.response}")

    def test_message_contains_role_and_content(self):
        if 'choices' in self.response and self.response['choices']:
            message = self.response['choices'][0].get('message', {})
            self.assertIn('role', message, f"'message' does not contain 'role'. Full response: {self.response}")
            self.assertIn('content', message, f"'message' does not contain 'content'. Full response: {self.response}")

if __name__ == '__main__':
    unittest.main()

