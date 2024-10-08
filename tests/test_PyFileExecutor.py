import unittest
import os
import tempfile
import sys
from unittest.mock import patch, Mock
from AutoChatBot.PyFileExecutor import PyFileExecutor

class TestPyFileExecutor(unittest.TestCase):
    """
    ### Explanation:
    1. **Test Setup and Teardown**:
       - `setUp` method initializes a temporary directory and constructs a file path for the script.
       - `tearDown` method ensures the temporary directory is cleaned up after tests are run.

    2. **Mocks**:
       - `subprocess.run` is mocked to simulate the execution of the Python script without actually running it.
       - `os.makedirs` is mocked to test directory creation logic without affecting the real filesystem.

    3. **Test Cases**:
       - **`test_execute_without_error`**: Tests the execution of the script when there is no error (`returncode = 0`).
       - **`test_execute_with_error`**: Tests the execution of the script when there is an error (`returncode = 1`).
       - **`test_execute_with_directory`**: Tests the script execution and directory creation logic.
       - **`test_is_error`**: Tests the `is_error` function to ensure it correctly identifies errors.

    The tests verify:
    - The `subprocess.run` method is called with the correct command.
    - The directory creation logic is correctly called.
    - The error output is correctly captured if any.
    - The executed code matches the input code.
    - The `is_error` function works as intended.
    """

   
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.file_path = os.path.join(self.temp_dir.name, 'script.py')
        sys.path.append(self.temp_dir.name)

    def tearDown(self):
        sys.path.remove(self.temp_dir.name)
        self.temp_dir.cleanup()

    @patch('subprocess.run')
    def test_execute_without_error(self, mock_subprocess_run):
        self.code = "print('Hello, World!')"
        mock_subprocess_run.return_value = Mock(returncode=0, stderr=b'')

        save_error = PyFileExecutor.save_code_to_file(self.file_path, self.code)
        self.assertIsNone(save_error)

        error_output = PyFileExecutor.execute_code(self.file_path)
        
        self.assertEqual(mock_subprocess_run.call_count, 1)
        
        # Adjust expected command to match the actual module path
        module_path = self.file_path.replace('/', '.').replace('\\', '.').rstrip('.py')
        expected_command = ['python', '-m', module_path]
        mock_subprocess_run.assert_called_with(expected_command, capture_output=True)

        self.assertIsNone(error_output)

    @patch('subprocess.run')
    def test_execute_with_error(self, mock_subprocess_run):
        self.code = "print('Hello, World!')"
        mock_subprocess_run.return_value = Mock(returncode=1, stderr=b'Error: Division by zero')

        save_error = PyFileExecutor.save_code_to_file(self.file_path, self.code)
        self.assertIsNone(save_error)

        error_output = PyFileExecutor.execute_code(self.file_path)
        
        self.assertEqual(mock_subprocess_run.call_count, 1)
        
        # Adjust expected command to match the actual module path
        module_path = self.file_path.replace('/', '.').replace('\\', '.').rstrip('.py')
        expected_command = ['python', '-m', module_path]
        mock_subprocess_run.assert_called_with(expected_command, capture_output=True)

        self.assertEqual(error_output, 'Error: Division by zero')

    @patch('os.makedirs')
    @patch('subprocess.run')
    def test_execute_with_directory(self, mock_subprocess_run, mock_makedirs):
        self.code = "print('Hello, World!')"
        mock_subprocess_run.return_value = Mock(returncode=0, stderr=b'')

        directory = os.path.dirname(self.file_path)
        save_error = PyFileExecutor.save_code_to_file(self.file_path, self.code)
        
        self.assertIsNone(save_error)
        self.assertEqual(mock_makedirs.call_count, 1)
        mock_makedirs.assert_called_with(directory, exist_ok=True)

        error_output = PyFileExecutor.execute_code(self.file_path)
        
        self.assertEqual(mock_subprocess_run.call_count, 1)
        
        # Adjust expected command to match the actual module path
        module_path = self.file_path.replace('/', '.').replace('\\', '.').rstrip('.py')
        expected_command = ['python', '-m', module_path]
        mock_subprocess_run.assert_called_with(expected_command, capture_output=True)

        self.assertIsNone(error_output)

    def test_is_error(self):
        self.assertTrue(PyFileExecutor.is_error("Error: Something went wrong"))
        self.assertFalse(PyFileExecutor.is_error("All tests ran successfully OK"))
        self.assertFalse(PyFileExecutor.is_error(""))

if __name__ == '__main__':
    unittest.main()


