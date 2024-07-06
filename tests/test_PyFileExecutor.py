import unittest
import os
import sys
import tempfile
from unittest.mock import patch, Mock, call
import subprocess
from AutoChatBot.PyFileExecutor import PyFileExecutor

class TestPyFileExecutor(unittest.TestCase):
    
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.file_path = os.path.join(self.temp_dir.name, 'script.py')
        self.code = "print('Hello, World!')"

    def tearDown(self):
        self.temp_dir.cleanup()

    @patch('subprocess.run')
    def test_execute_without_error(self, mock_subprocess_run):
        mock_subprocess_run.return_value = Mock(returncode=0, stderr=b'')
        
        executor = PyFileExecutor(self.file_path, self.code)
        error_output = executor.execute()

        self.assertEqual(mock_subprocess_run.call_count, 1)
        expected_command = ['python', self.file_path]
        mock_subprocess_run.assert_called_with(expected_command, capture_output=True)

        self.assertIsNone(error_output)

    @patch('subprocess.run')
    def test_execute_with_error(self, mock_subprocess_run):
        mock_subprocess_run.return_value = Mock(returncode=1, stderr=b'Error: Division by zero')

        executor = PyFileExecutor(self.file_path, self.code)
        error_output = executor.execute()

        self.assertEqual(mock_subprocess_run.call_count, 1)
        expected_command = ['python', self.file_path]
        mock_subprocess_run.assert_called_with(expected_command, capture_output=True)

        self.assertEqual(error_output, 'Error: Division by zero')

    @patch('os.makedirs')
    @patch('subprocess.run')
    def test_execute_with_directory(self, mock_subprocess_run, mock_makedirs):
        mock_subprocess_run.return_value = Mock(returncode=0, stderr=b'')

        directory = os.path.dirname(self.file_path)
        executor = PyFileExecutor(self.file_path, self.code)
        error_output = executor.execute()

        self.assertEqual(mock_makedirs.call_count, 1)
        mock_makedirs.assert_called_with(directory, exist_ok=True)

        self.assertEqual(mock_subprocess_run.call_count, 1)
        expected_command = ['python', os.path.join(directory, self.file_path)]
        mock_subprocess_run.assert_called_with(expected_command, capture_output=True)

        self.assertIsNone(error_output)

if __name__ == '__main__':
    unittest.main()
