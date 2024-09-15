import unittest
import tempfile
import os
from unittest.mock import patch
from AutoChatBot.multi_file_agent import MultiFileAgent

class TestMultiFileAgent(unittest.TestCase):
    """
    Unit tests for the MultiFileAgent class, which uses AutoChatBot to generate and update multiple files.
    
    The testing strategy covers the following cases:
    1. Reading file content.
    2. Creating files if they do not exist.
    3. Constructing file strings.
    4. Constructing the task string.
    5. Constructing the base prompt.
    6. Filtering Python code from responses.
    7. Generating file content using AutoChatBot.
    8. Orchestrating the process using the execute method.
    """

    def setUp(self):
        """
        Initializes the settings for the tests, including the temporary file paths.
        """
        self.tempdir = tempfile.TemporaryDirectory()
        self.reference_file = os.path.join(self.tempdir.name, "reference_file.txt")
        self.rewrite_file = os.path.join(self.tempdir.name, "rewrite_file.txt")

        # Create a reference file with some content
        with open(self.reference_file, 'w') as file:
            file.write("Reference file content")

        # Create a rewrite file with some content
        with open(self.rewrite_file, 'w') as file:
            file.write("Rewrite file content")

    def tearDown(self):
        """
        Cleans up the temporary directory after tests.
        """
        self.tempdir.cleanup()

    def test_read_file_content(self):
        """
        Tests the `read_file_content` method for reading the content of a file.
        """
        content = MultiFileAgent.read_file_content(self.reference_file)
        self.assertEqual(content, "Reference file content")

        with self.assertRaises(FileNotFoundError):
            MultiFileAgent.read_file_content("non_existent_file.txt")

    def test_create_file_if_not_exists(self):
        """
        Tests the `create_file_if_not_exists` method for creating files if they do not exist.
        """
        new_file_path = os.path.join(self.tempdir.name, "new_file.txt")
        MultiFileAgent.create_file_if_not_exists(new_file_path)
        self.assertTrue(os.path.exists(new_file_path))

    def test_construct_file_string(self):
        """
        Tests the `construct_file_string` method for constructing a string representation of files and their contents.
        """
        file_string = MultiFileAgent.construct_file_string([self.reference_file, self.rewrite_file])
        expected_string = f"{self.reference_file}:\nReference file content\n\n{self.rewrite_file}:\nRewrite file content\n\n"
        self.assertEqual(file_string, expected_string)

        with self.assertRaises(FileNotFoundError):
            MultiFileAgent.construct_file_string([self.reference_file, "non_existent_file.txt"])

    def test_construct_task_string(self):
        """
        Tests the `construct_task_string` method for constructing the task string with the provided question.
        """
        task_string = MultiFileAgent.construct_task_string("What is the purpose of this code?")
        expected_string = "TASK:\n\nWhat is the purpose of this code?\n\n"
        self.assertEqual(task_string, expected_string)

    def test_construct_base_prompt(self):
        """
        Tests the `construct_base_prompt` method for constructing the base prompt string.
        """
        base_prompt = MultiFileAgent.construct_base_prompt([self.reference_file], [self.rewrite_file], "What is the purpose of this code?")
        expected_string = (
            f"{self.reference_file}:\nReference file content\n\n"
            f"{self.rewrite_file}:\nRewrite file content\n\n"
            "TASK:\n\nWhat is the purpose of this code?\n\n"
        )
        self.assertEqual(base_prompt, expected_string)

    def test_filter_python_code(self):
        """
        Tests the `filter_python_code` method for filtering out Python code from a response.
        """
        response = "```python\nprint('Hello, World!')\n```"
        code = MultiFileAgent.filter_python_code(response)
        self.assertEqual(code, "print('Hello, World!')")

    @patch('AutoChatBot.multi_file_agent.ChatAPIHandler.make_api_request')
    def test_generate_file_content(self, mock_make_api_request):
        """
        Tests the `generate_file_content` method for generating content for a file using AutoChatBot.
        """
        mock_response = {"choices": [{"message": {"content": "Generated content"}}]}
        mock_make_api_request.return_value = mock_response

        base_prompt = MultiFileAgent.construct_base_prompt([self.reference_file], [self.rewrite_file], "What is the purpose of this code?")
        content = MultiFileAgent.generate_file_content(base_prompt, self.rewrite_file, is_new=False)
        self.assertEqual(content, "Generated content")

    @patch('AutoChatBot.multi_file_agent.ChatAPIHandler.make_api_request')
    def test_execute(self, mock_make_api_request):
        """
        Tests the `execute` method for orchestrating the multi-file generation and update process.
        """
        mock_response = {"choices": [{"message": {"content": "Generated content"}}]}
        mock_make_api_request.return_value = mock_response

        result = MultiFileAgent.execute([self.reference_file], [self.rewrite_file], "What is the purpose of this code?", debug=True)
        self.assertEqual(result[self.rewrite_file], "Generated content")

    def test_execute_with_actual_api_call(self):
        """
        Tests the `execute` method with an actual API call to verify integration.
        """
        result = MultiFileAgent.execute([self.reference_file], [self.rewrite_file], "What is the purpose of this code?", debug=False)
        self.assertIn(self.rewrite_file, result)
        self.assertTrue(result[self.rewrite_file])

if __name__ == "__main__":
    unittest.main()
