import unittest
import tempfile
import os
import json
import argparse
from unittest.mock import patch, MagicMock
from AutoChatBot.AutoChatBot import ChatBot
from AutoChatBot.multi_file_agent import MultiFileAgent
from AutoChatBot.python_file_executor import PythonFileExecutor
from AutoChatBot.ParserCreator import ParserCreator

class TestAutoChatBot(unittest.TestCase):
    """
    Unit tests for the AutoChatBot class, focusing on the integration of the multi-file agent and other chatbot functionalities.

    Testing Strategy:
    1. Test the `execute_multifile_agent` method.
    2. Test the `execute_files` method.
    3. Test the `main` method for parsing arguments and executing functionalities.
    4. Mock external dependencies such as file I/O and API requests to ensure robustness.
    5. Test the execution of files and capture their stdout and stderr.
    """

    def setUp(self):
        """
        Initializes the settings for the tests, including the temporary file path.
        """
        self.tempdir = tempfile.TemporaryDirectory()
        self.reference_files = [os.path.join(self.tempdir.name, "ref_file_1.txt"), os.path.join(self.tempdir.name, "ref_file_2.txt")]
        self.rewrite_files = [os.path.join(self.tempdir.name, "rewrite_file_1.txt"), os.path.join(self.tempdir.name, "rewrite_file_2.txt")]
        self.execute_files = [os.path.join(self.tempdir.name, "execute_file_1.py"), os.path.join(self.tempdir.name, "execute_file_2.py")]
        self.question_file = os.path.join(self.tempdir.name, "question.txt")
        self.question = "What is the purpose of this test?"
        self.debug = True
        self.output_dir = os.path.join(self.tempdir.name, "output")

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

    @patch.object(MultiFileAgent, 'execute', return_value={"rewrite_file_1.txt": "Updated content 1", "rewrite_file_2.txt": "Updated content 2"})
    def test_execute_multifile_agent(self, mock_execute):
        """
        Tests the `execute_multifile_agent` method for integrating with `MultiFileAgent`.
        """
        parser = ParserCreator.create_parser()
        args = parser.parse_args([
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
        
        result = ChatBot.execute_multifile_agent(self.reference_files, self.rewrite_files, self.question, None, args, self.debug)
        self.assertEqual(result, {"rewrite_file_1.txt": "Updated content 1", "rewrite_file_2.txt": "Updated content 2"})
        mock_execute.assert_called_once_with(self.reference_files, self.rewrite_files, self.question, None, args, self.debug)

    @patch.object(PythonFileExecutor, 'execute', return_value={"execute_file_1.py": ("Output 1", ""), "execute_file_2.py": ("Output 2", "")})
    def test_execute_files(self, mock_execute):
        """
        Tests the `execute_files` method for integrating with `PythonFileExecutor`.
        """
        result = ChatBot.execute_files(self.execute_files)
        self.assertEqual(result, {"execute_file_1.py": ("Output 1", ""), "execute_file_2.py": ("Output 2", "")})
        mock_execute.assert_called_once_with(self.execute_files)

    @patch('argparse.ArgumentParser.parse_args')
    @patch.object(ChatBot, 'execute_multifile_agent', return_value={"rewrite_file_1.txt": "Updated content 1", "rewrite_file_2.txt": "Updated content 2"})
    @patch.object(ChatBot, 'execute_files', return_value={"execute_file_1.py": ("Output 1", ""), "execute_file_2.py": ("Output 2", "")})
    def test_main(self, mock_execute_files, mock_execute_multifile_agent, mock_parse_args):
        """
        Tests the `main` method for parsing arguments and executing the multi-file agent and file execution functionalities.
        """
        mock_parse_args.return_value = argparse.Namespace(
            multi_file_agent=True,
            reference_files=self.reference_files,
            rewrite_files=self.rewrite_files,
            execute_files=self.execute_files,
            question=None,
            question_file_path=self.question_file,
            debug=self.debug,
            output_dir=self.output_dir,
            show_available_context=False,
            show_models=False,
            file_path=None,
            api='openai',
            model='gpt-3.5-turbo',
            max_tokens=100,
            temperature=1,
            frequency_penalty=0,
            presence_penalty=0,
            top_p=1,
            top_k=50,
            repetition_penalty=1,
            stop_sequences=None,
            context=None,
            save_path='response.tmp',
            run_code=False,
            run_code_with_unittest=False
        )

        with patch('builtins.open', unittest.mock.mock_open()) as mock_file:
            ChatBot.main()
            mock_execute_multifile_agent.assert_called_once_with(self.reference_files, self.rewrite_files, None, self.question_file, mock_parse_args.return_value, self.debug)
            mock_execute_files.assert_called_once_with(self.execute_files)
            mock_file.assert_any_call('rewrite_file_1.txt', 'w')
            mock_file.assert_any_call('rewrite_file_2.txt', 'w')

if __name__ == "__main__":
    unittest.main()

