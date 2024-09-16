import unittest
import tempfile
import os
from unittest.mock import patch, MagicMock
from AutoChatBot.multi_file_agent import MultiFileAgent
from AutoChatBot.ParserCreator import ParserCreator

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
    7. Filtering Markdown content from responses.
    8. Generating file content using AutoChatBot.
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
        self.question = "What is the purpose of this code?"
        self.debug = True

        # Create reference, rewrite, and question files with some content
        for file_path in self.reference_files + self.rewrite_files:
            with open(file_path, 'w') as file:
                file.write("Sample content")

        with open(self.question_file, 'w') as file:
            file.write(self.question)

        # Create a parser and arguments for testing
        self.parser = ParserCreator.create_parser()
        self.args = self.parser.parse_args([
            "--api", "openai",
            "--model", "gpt-3.5-turbo",
            "--max_tokens", "100",
            "--temperature", "0.7",
            "--frequency_penalty", "0.5",
            "--presence_penalty", "0.6",
            "--top_p", "0.9",
            "--top_k", "40",
            "--repetition_penalty", "1.2",
            "--stop_sequences", "\n"
        ])

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

    def test_construct_conversation(self):
        """
        Tests the `construct_conversation` method for constructing the conversation history.
        """
        conversation = MultiFileAgent.construct_conversation(self.reference_files, self.rewrite_files)
        expected_conversation = [
            {"role": "user", "content": f"The file {self.reference_files[0]} shall be used as a reference for similar files in the future. Now show me only the current {self.reference_files[0]} content:\n\n"},
            {"role": "assistant", "content": "Sample content\n\n"},
            {"role": "user", "content": f"We will be working on {self.rewrite_files[0]} in the future. Now show me only the current {self.rewrite_files[0]} content:\n\n"},
            {"role": "assistant", "content": "Sample content\n\n"},
        ]
        self.assertEqual(conversation, expected_conversation)

    def test_construct_task_string(self):
        """
        Tests the `construct_task_string` method for constructing the task string with the provided question.
        """
        task_string = MultiFileAgent.construct_task_string("What is the purpose of this code?")
        expected_string = "TASK:\n\nWhat is the purpose of this code?\n\n"
        self.assertEqual(task_string, expected_string)

    @patch('AutoChatBot.ChatAPIHandler.ChatAPIHandler.make_api_request')
    def test_generate_file_content(self, mock_make_api_request):
        """
        Tests the `generate_file_content` method for generating content for a file using AutoChatBot.
        """
        mock_make_api_request.return_value = {
            "choices": [{"message": {"content": "Updated content"}}]
        }
        conversation = [
            {"role": "user", "content": "Base prompt content"},
            {"role": "assistant", "content": "Sample content"}
        ]
        file_path = self.rewrite_files[0]
        task = "TASK:\n\nWhat is the purpose of this code?\n\n"

        content = MultiFileAgent.generate_file_content(conversation, file_path, task, self.args)
        self.assertEqual(content, "Updated content")

    @patch('AutoChatBot.ChatAPIHandler.ChatAPIHandler.make_api_request', return_value={
        "choices": [{"message": {"content": "Updated content"}}]
    })
    def test_execute(self, mock_make_api_request):
        """
        Tests the `execute` method for orchestrating the multi-file generation and update process.
        """
        result = MultiFileAgent.execute(
            self.reference_files, self.rewrite_files, question=self.question, args=self.args, debug=self.debug
        )
        self.assertEqual(result[self.rewrite_files[0]], "Updated content")
        mock_make_api_request.assert_called()

if __name__ == "__main__":
    unittest.main()

