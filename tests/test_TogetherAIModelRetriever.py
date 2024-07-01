import unittest
from dotenv import load_dotenv
import os
import sys

# Add the src directory to the Python path for imports
sys.path.append('AutoChatBot')

from TogetherAIModelRetriever import TogetherAIModelRetriever

class TestTogetherAIModelRetriever(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Load environment variables from .env
        load_dotenv()

        # Load the TOGETHERAI_API_KEY from environment variables
        cls.api_key = os.getenv('TOGETHERAI_API_KEY')
        assert cls.api_key is not None, "TOGETHERAI_API_KEY environment variable not set."

        # Initialize the TogetherAIModelRetriever
        cls.model_retriever = TogetherAIModelRetriever(api_key=cls.api_key)

    def test_get_available_models(self):
        # Make the API request to get available models
        models = self.model_retriever.get_available_models()

        # Check if the response is a list
        self.assertIsInstance(models, list, "The response is not a list")

        # Check if the list is not empty
        self.assertGreater(len(models), 0, "The response list is empty")

        # Check if each model in the list is a dictionary
        for model in models:
            self.assertIsInstance(model, dict, "A model in the response list is not a dictionary")

            # Check if the dictionary contains expected keys
            self.assertIn('display_name', model, "Model dictionary does not contain 'display_name'")
            self.assertIn('type', model, "Model dictionary does not contain 'type'")
            self.assertIn('pricing', model, "Model dictionary does not contain 'pricing'")

if __name__ == '__main__':
    unittest.main()
