import unittest
from unittest.mock import patch
from AutoChatBot.ChatApiHandler import make_api_request
from sandbox_scripts.code_generator_agent import CodeGeneratorAgent

class TestCodeGeneratorAgent(unittest.TestCase):

    @patch('AutoChatBot.ChatApiHandler.make_api_request')
    def test_generate_application_code(self, mock_make_api_request):
        """
        Tests the `generate_application_code` method for generating application code.
        """
        mock_make_api_request.return_value = {"text": "print('Hello, World!')"}
        
        api_params = CodeGeneratorAgent.setup_api_parameters(
            api="example_api",
            model="example_model",
            temperature=0.7,
            max_tokens=150,
            top_p=0.9,
            conversation=["Generate the application code."]
        )
        
        application_code = CodeGeneratorAgent.generate_application_code(api_params)
        self.assertEqual(application_code, "print('Hello, World!')")

    @patch('AutoChatBot.ChatApiHandler.make_api_request')
    def test_generate_unit_test_code(self, mock_make_api_request):
        """
        Tests the `generate_unit_test_code` method for generating unit test code.
        """
        mock_make_api_request.return_value = {"text": "def test_hello():\n    assert True"}
        
        api_params = CodeGeneratorAgent.setup_api_parameters(
            api="example_api",
            model="example_model",
            temperature=0.7,
            max_tokens=150,
            top_p=0.9,
            conversation=["Generate the unit test code."]
        )
        
        unit_test_code = CodeGeneratorAgent.generate_unit_test_code(api_params)
        self.assertEqual(unit_test_code, "def test_hello():\n    assert True")

    @patch('AutoChatBot.ChatApiHandler.make_api_request')
    def test_compile_results(self, mock_make_api_request):
        """
        Tests the `compile_results` method for generating both application and unit test code.
        """
        mock_make_api_request.side_effect = [
            {"text": "print('Hello, World!')"},
            {"text": "def test_hello():\n    assert True"}
        ]
        
        api_name = "example_api"
        model = "example_model"
        temperature = 0.7
        max_tokens = 150
        top_p = 0.9
        conversation = ["I need to write a Python script that performs X.", "Can you provide the code for it?"]

        application_code, unit_test_code = CodeGeneratorAgent.compile_results(api_name, model, temperature, max_tokens, top_p, conversation)
        
        self.assertEqual(application_code, "print('Hello, World!')")
        self.assertEqual(unit_test_code, "def test_hello():\n    assert True")

if __name__ == "__main__":
    unittest.main()
