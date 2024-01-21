import unittest
import re
import sys
import os

# Adjust the path to include the src directory
sys.path.append(os.path.abspath(os.path.join('..', 'src')))
import src.ask_openai_cli

class TestAskOpenAICLIIntegration(unittest.TestCase):

    def setUp(self):
        # Load the real API key from the .env file or environment
        from dotenv import load_dotenv
        load_dotenv()
        self.api_key = os.getenv('OPENAI_API_KEY')
        
        if not self.api_key:
            raise ValueError("No OpenAI API key found. Please check your .env file.")

    def test_openai_api_real_connection(self):
        # Call the function with a real API key
        question = "What is the capital of France?"
        response = ask_openai_cli.ask_question(question)

        # Check if 'Paris' or 'paris' is in the response using regex
        self.assertTrue(re.search(r'\bParis\b', response, re.IGNORECASE))

if __name__ == '__main__':
    unittest.main()

