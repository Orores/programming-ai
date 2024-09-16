import unittest
import tempfile
import os
from unittest.mock import patch, MagicMock
from AutoChatBot.multi_file_agent import MultiFileAgent
from AutoChatBot.PyFileExecutor import PyFileExecutor

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
    8. Executing files and capturing stdout and stderr.
    9. Orchestrating the process using the execute method.
    10. Reading the question from a file.
    """

    def setUp(self):
        """
        Initializes the settings for the tests, including the temporary file paths.
        """
        self.tempdir = tempfile.TemporaryDirectory()
        self.reference_files = [os.path.join(self.tempdir.name, "reference_file.txt")]
        self.rewrite_files = [os.path.join(self.tempdir.name, "rewrite_file.txt")]
        self.question_file = os.path.join(self.tempdir.name, "question.txt")
        self.execute_files = [os.path.join(self.tempdir.name, "execute_file.py")]
        self.question = "What is the purpose of this code?"
        self.debug = True

        # Create reference, rewrite, and question files with some content
        for file_path in self.reference_files + self.rewrite_files + self.execute_files:
            with open(file_path, 'w') as file:
                file.write("print('Hello, world!')" if file_path.endswith('.py') else "Sample content")

        with open(self.question_file, 'w') as file:
            file.write(self.question)

    def tearDown(self):
        """
        Cleans up the temporary directory after tests.
        """
        self.tempdir.cleanup()

    def test_read_file_content(self):
        """
        Tests the `read_file_content` method for reading the content of a file.
        """
        content = MultiFileAgent.read_file_content(self.reference_files[0])
        self.assertEqual(content, "Sample content")

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
        file_string = MultiFileAgent.construct_file_string(self.reference_files + self.rewrite_files)
        expected_string = f"{self.reference_files[0]}:\nSample content\n\n{self.rewrite_files[0]}:\nSample content\n\n"
        self.assertEqual(file_string, expected_string)

        with self.assertRaises(FileNotFoundError):
            MultiFileAgent.construct_file_string([self.reference_files[0], "non_existent_file.txt"])

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
        base_prompt = MultiFileAgent.construct_base_prompt(self.reference_files, self.rewrite_files, "What is the purpose of this code?")
        expected_string = (
            f"{self.reference_files[0]}:\nSample content\n\n"
            f"{self.rewrite_files[0]}:\nSample content\n\n"
            "TASK:\n\nWhat is the purpose of this code?\n\n"
        )
        self.assertEqual(base_prompt, expected_string)

    @patch('AutoChatBot.ChatAPIHandler.ChatAPIHandler.make_api_request')
    def test_generate_file_content(self, mock_make_api_request):
        """
        Tests the `generate_file_content` method for generating content for a file using AutoChatBot.
        """
        mock_make_api_request.return_value = {
            "choices": [{"message": {"content": "Updated content"}}]
        }
        base_prompt = "Base prompt content"
        file_path = self.rewrite_files[0]
        is_new = False

        content = MultiFileAgent.generate_file_content(base_prompt, file_path, is_new)
        self.assertEqual(content, "Updated content")

    @patch('AutoChatBot.PyFileExecutor.PyFileExecutor.execute_code', return_value=("Output", ""))
    def test_execute_files(self, mock_execute_code):
        """
        Tests the `execute_files` method for executing files and capturing stdout and stderr.
        """
        exec_outputs = MultiFileAgent.execute_files(self.execute_files)
        expected_outputs = {self.execute_files[0]: ("Output", "")}
        self.assertEqual(exec_outputs, expected_outputs)
        mock_execute_code.assert_called_once_with(self.execute_files[0])

    @patch('AutoChatBot.PyFileExecutor.PyFileExecutor.execute_code', return_value=("Output", ""))
    @patch('AutoChatBot.ChatAPIHandler.ChatAPIHandler.make_api_request', return_value={
        "choices": [{"message": {"content": "Updated content"}}]
    })
    def test_execute(self, mock_make_api_request, mock_execute_code):
        """
        Tests the `execute` method for orchestrating the multi-file generation, execution, and update process.
        """
        result, exec_outputs, status = MultiFileAgent.execute(
            self.reference_files, self.rewrite_files, question=self.question, execute_files=self.execute_files, debug=self.debug
        )
        self.assertEqual(result[self.rewrite_files[0]], "Updated content")
        self.assertEqual(exec_outputs[self.execute_files[0]], ("Output", ""))
        self.assertEqual(status, "Success")
        mock_make_api_request.assert_called()
        mock_execute_code.assert_called_once_with(self.execute_files[0])

    @patch('AutoChatBot.PyFileExecutor.PyFileExecutor.execute_code', return_value=("Output", "Error"))
    @patch('AutoChatBot.ChatAPIHandler.ChatAPIHandler.make_api_request', return_value={
        "choices": [{"message": {"content": "Updated content"}}]
    })
    def test_execute_with_failure(self, mock_make_api_request, mock_execute_code):
        """
        Tests the `execute` method for handling execution failures.
        """
        result, exec_outputs, status = MultiFileAgent.execute(
            self.reference_files, self.rewrite_files, question=self.question, execute_files=self.execute_files, debug=self.debug
        )
        self.assertEqual(result[self.rewrite_files[0]], "Updated content")
        self.assertEqual(exec_outputs[self.execute_files[0]], ("Output", "Error"))
        self.assertEqual(status, f"Failure: {self.execute_files[0]} had an error.")
        mock_make_api_request.assert_called()
        mock_execute_code.assert_called_once_with(self.execute_files[0])

if __name__ == "__main__":
    unittest.main()