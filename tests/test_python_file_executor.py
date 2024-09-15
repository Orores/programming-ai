import unittest
import tempfile
import os
from AutoChatBot.python_file_executor import PythonFileExecutor

class TestPythonFileExecutor(unittest.TestCase):
    """
    Unit tests for the PythonFileExecutor class, which executes Python files and captures their stdout and stderr.
    
    The testing strategy covers the following cases:
    1. Executing a Python file and capturing stdout and stderr.
    2. Handling file not found errors.
    3. Handling execution errors.
    4. Orchestrating the execution of multiple Python files.
    """

    def setUp(self):
        """
        Initializes the settings for the tests, including the temporary file path.
        """
        self.tempdir = tempfile.TemporaryDirectory()
        self.python_file = os.path.join(self.tempdir.name, "test_file.py")
        self.python_file_with_error = os.path.join(self.tempdir.name, "test_file_with_error.py")

        # Create a Python file with some content
        with open(self.python_file, 'w') as file:
            file.write("print('Hello, world!')")

        # Create a Python file that will raise an error
        with open(self.python_file_with_error, 'w') as file:
            file.write("raise ValueError('This is an intentional error.')")

    def tearDown(self):
        """
        Cleans up the temporary directory after tests.
        """
        self.tempdir.cleanup()

    def test_execute_code(self):
        """
        Tests the `execute_code` method for executing a Python file and capturing stdout and stderr.
        """
        stdout, stderr = PythonFileExecutor.execute_code(self.python_file)
        self.assertEqual(stdout.strip(), "Hello, world!")
        self.assertEqual(stderr, "")

    def test_execute_code_with_error(self):
        """
        Tests the `execute_code` method for handling execution errors.
        """
        stdout, stderr = PythonFileExecutor.execute_code(self.python_file_with_error)
        self.assertEqual(stdout, "")
        self.assertIn("ValueError: This is an intentional error.", stderr)

    def test_execute_code_file_not_found(self):
        """
        Tests the `execute_code` method for handling file not found errors.
        """
        with self.assertRaises(FileNotFoundError):
            PythonFileExecutor.execute_code("non_existent_file.py")

    def test_execute(self):
        """
        Tests the `execute` method for orchestrating the execution of multiple Python files.
        """
        file_paths = [self.python_file, self.python_file_with_error]
        exec_outputs = PythonFileExecutor.execute(file_paths)

        self.assertIn(self.python_file, exec_outputs)
        self.assertIn(self.python_file_with_error, exec_outputs)

        stdout, stderr = exec_outputs[self.python_file]
        self.assertEqual(stdout.strip(), "Hello, world!")
        self.assertEqual(stderr, "")

        stdout, stderr = exec_outputs[self.python_file_with_error]
        self.assertEqual(stdout, "")
        self.assertIn("ValueError: This is an intentional error.", stderr)

if __name__ == "__main__":
    unittest.main()
