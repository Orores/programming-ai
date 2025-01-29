import unittest
import tempfile
import os
import sys
from AutoChatBot.python_file_executor import PythonFileExecutor

class TestPythonFileExecutor(unittest.TestCase):
    """
    Unit tests for the PythonFileExecutor class with overhauled error handling.
    """

    def setUp(self):
        # Create a local temporary directory for testing
        self.tempdir = tempfile.TemporaryDirectory(dir='.')
        
        # Create package structure
        self.package_dir = os.path.join(self.tempdir.name, "temp_package")
        os.makedirs(self.package_dir, exist_ok=True)
        
        # Create __init__.py files
        with open(os.path.join(self.tempdir.name, "__init__.py"), 'w') as f:
            pass
        with open(os.path.join(self.package_dir, "__init__.py"), 'w') as f:
            pass

        # Create test files inside the package
        self.test_file = os.path.join(self.package_dir, "test_file.py")
        self.error_file = os.path.join(self.package_dir, "test_file_with_error.py")

        with open(self.test_file, 'w') as f:
            f.write("print('Hello, world!')")

        with open(self.error_file, 'w') as f:
            f.write("raise ValueError('This is an intentional error.')")

        # Add tempdir to Python path
        sys.path.insert(0, self.tempdir.name)

    def tearDown(self):
        # Remove the temporary directory from the Python path
        sys.path.remove(self.tempdir.name)
        # Cleanup the temporary directory
        self.tempdir.cleanup()

    def test_execute_code(self):
        """Test normal execution with proper module handling."""
        module_name = "temp_package/test_file.py"
        stdout, stderr = PythonFileExecutor.execute_code(module_name)
        self.assertEqual(stdout.strip(), "Hello, world!")
        self.assertEqual(stderr, "")

    def test_execute_code_with_error(self):
        """Test proper error capture with full traceback."""
        module_name = "temp_package/test_file_with_error.py"
        stdout, stderr = PythonFileExecutor.execute_code(module_name)
        self.assertEqual(stdout, "")
        self.assertIn("ValueError: This is an intentional error.", stderr)

    def test_execute(self):
        """Test orchestrating execution of multiple modules."""
        modules = ["temp_package/test_file.py", "temp_package/test_file_with_error.py"]
        exec_outputs = PythonFileExecutor.execute(modules)
        
        self.assertIn("temp_package/test_file.py", exec_outputs)
        self.assertIn("temp_package/test_file_with_error.py", exec_outputs)

        stdout, stderr = exec_outputs["temp_package/test_file.py"]
        self.assertEqual(stdout.strip(), "Hello, world!")
        self.assertEqual(stderr, "")

        stdout, stderr = exec_outputs["temp_package/test_file_with_error.py"]
        self.assertEqual(stdout, "")
        self.assertIn("ValueError: This is an intentional error.", stderr)

    def test_execute_code_file_not_found(self):
        """Verify proper handling of invalid module paths."""
        with self.assertRaises(FileNotFoundError):
            PythonFileExecutor.execute_code("non_existent_module")

if __name__ == "__main__":
    unittest.main()