import unittest
from langchain_openai import OpenAI
from dotenv import load_dotenv
import os

# Load API key from .env file
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

class TestOpenAIConnection(unittest.TestCase):
    def test_openai_connection(self):
        # Initialize LangChain with the actual OpenAI
        llm = OpenAI(api_key=api_key)

        # Perform an API call using invoke
        response = llm.invoke("What is the capital of France?")
        self.assertIsNotNone(response)  # Basic check to ensure a response is received

if __name__ == '__main__':
    unittest.main()

