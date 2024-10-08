import unittest
from unittest.mock import patch
from io import StringIO
from dotenv import load_dotenv
import os
from AutoChatBot.TogetherAIModelRetriever import TogetherAIModelRetriever

class TestTogetherAIModelRetriever(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Load environment variables from .env
        load_dotenv()

        # Load the TOGETHERAI_API_KEY from environment variables
        cls.api_key = os.getenv('TOGETHERAI_API_KEY')
        assert cls.api_key is not None, "TOGETHERAI_API_KEY environment variable not set."

    def test_get_available_models(self):
        # Make the API request to get available models
        models = TogetherAIModelRetriever.get_available_models(self.api_key)

        # Check if the response is a list
        self.assertIsInstance(models, list, "The response is not a list")

        # Check if the list is not empty
        self.assertGreater(len(models), 0, "The response list is empty")

        # Check if each model in the list is a dictionary
        for model in models:
            self.assertIsInstance(model, dict, "A model in the response list is not a dictionary")

            # Check if the dictionary contains expected keys
            self.assertIn('id', model, "Model dictionary does not contain 'id'")
            self.assertIn('type', model, "Model dictionary does not contain 'type'")
            self.assertIn('pricing', model, "Model dictionary does not contain 'pricing'")

    @patch('sys.stdout', new_callable=StringIO)
    def test_print_models_table(self, mock_stdout):
        # Mock model data
        mock_models = [
            {
                "id": "mock_model_1",
                "type": "language",
                "pricing": {
                    "hourly": 0,
                    "input": 0.1,
                    "output": 0.1,
                    "base": 0
                }
            },
            {
                "id": "mock_model_2",
                "type": "chat",
                "pricing": {
                    "hourly": 0,
                    "input": 0.2,
                    "output": 0.2,
                    "base": 0
                }
            }
        ]

        # Call the method to print models
        TogetherAIModelRetriever.print_models_table(mock_models)

        # Capture the output
        output = mock_stdout.getvalue()

        # Define the expected output
        expected_output = (
            "ID                                       Type       Pricing (Hourly) Pricing (Input) Pricing (Output) Pricing (Base)\n"
            "------------------------------------------------------------------------------------------------------------------------\n"
            "mock_model_1                             language   0        0.1      0.1      0       \n"
            "mock_model_2                             chat       0        0.2      0.2      0       \n"
        )

        # Check if the output matches the expected output
        self.assertEqual(output, expected_output, "The table output is not as expected")

if __name__ == '__main__':
    unittest.main()
