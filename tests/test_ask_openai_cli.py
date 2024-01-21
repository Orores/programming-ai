import unittest
import subprocess
import os

class TestAskOpenAICLIIntegration(unittest.TestCase):

    def setUp(self):
        # Load the API key from the .env file or environment
        if not os.getenv('OPENAI_API_KEY'):
            from dotenv import load_dotenv
            load_dotenv()

    def test_openai_api_response(self):
        # Simulate command line execution of the script
        result = subprocess.run(['python', '../src/ask_openai_cli.py', '--question', 'What is the capital of France?'], capture_output=True, text=True)

        # Check for a non-empty response
        self.assertTrue(result.stdout)

if __name__ == '__main__':
    unittest.main()

