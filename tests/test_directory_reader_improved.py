import unittest
import tempfile
import os
import subprocess
from AutoChatBot.directory_reader import DirectoryReader

class TestDirectoryReader(unittest.TestCase):
    """
    Short Description:
    This class contains unit tests for the DirectoryReader class, which reads and formats the contents of .py files in a directory.
    
    Testing Strategy:
    The testing strategy covers the following cases:
    1. Reading and formatting the contents of multiple .py files.
    2. Handling directories with no .py files.
    3. Handling nested directories with .py files.
    4. Handling an empty directory.
    5. Verifying CLI functionality.

    Methods:
    - test_read_and_format_py_files:
        Tests the `read_and_format_py_files` method for reading and formatting multiple .py files.
    - test_empty_directory:
        Tests the `read_and_format_py_files` method for handling an empty directory.
    - test_no_py_files:
        Tests the `read_and_format_py_files` method for handling directories with no .py files.
    - test_nested_directories:
        Tests the `read_and_format_py_files` method for handling nested directories with .py files.
    - test_cli_functionality:
        Tests the CLI functionality for reading and formatting .py files.
    
    Properties Ensured:
    - Correct reading and formatting of multiple .py files.
    - Appropriate handling of empty directories and directories with no .py files.
    - Proper handling of nested directories containing .py files.
    - Correct CLI output.
    """

    def test_read_and_format_py_files(self):
        """
        Short Description:
        Tests the `read_and_format_py_files` method for reading and formatting multiple .py files.

        Test Strategy:
        Creates a temporary directory with multiple .py files and checks the formatted output.

        Expected Outcome:
        The formatted output should match the expected string with file paths and contents.
        """
        with tempfile.TemporaryDirectory() as tempdir:
            file1_path = os.path.join(tempdir, "file1.py")
            file2_path = os.path.join(tempdir, "file2.py")
            
            with open(file1_path, 'w') as f:
                f.write("print('Hello from file1')\n")
                
            with open(file2_path, 'w') as f:
                f.write("print('Hello from file2')\n")

            expected_output = f"""\
File: {file1_path}
--------------------
print('Hello from file1')

File: {file2_path}
--------------------
print('Hello from file2')
""".strip()

            actual_output = DirectoryReader.read_and_format_py_files(tempdir).strip()
            self.assertEqual(actual_output, expected_output)

    def test_empty_directory(self):
        """
        Short Description:
        Tests the `read_and_format_py_files` method for handling an empty directory.

        Test Strategy:
        Creates a temporary empty directory and checks the formatted output.

        Expected Outcome:
        The formatted output should be an empty string.
        """
        with tempfile.TemporaryDirectory() as tempdir:
            expected_output = ""
            actual_output = DirectoryReader.read_and_format_py_files(tempdir)
            self.assertEqual(actual_output, expected_output)

    def test_no_py_files(self):
        """
        Short Description:
        Tests the `read_and_format_py_files` method for handling directories with no .py files.

        Test Strategy:
        Creates a temporary directory with non-.py files and checks the formatted output.

        Expected Outcome:
        The formatted output should be an empty string.
        """
        with tempfile.TemporaryDirectory() as tempdir:
            file1_path = os.path.join(tempdir, "file1.txt")
            file2_path = os.path.join(tempdir, "file2.md")
            
            with open(file1_path, 'w') as f:
                f.write("This is a text file.\n")
                
            with open(file2_path, 'w') as f:
                f.write("This is a markdown file.\n")

            expected_output = ""
            actual_output = DirectoryReader.read_and_format_py_files(tempdir)
            self.assertEqual(actual_output, expected_output)

    def test_nested_directories(self):
        """
        Short Description:
        Tests the `read_and_format_py_files` method for handling nested directories with .py files.

        Test Strategy:
        Creates a temporary directory with nested subdirectories and .py files, then checks the formatted output.

        Expected Outcome:
        The formatted output should include file paths and contents from all nested .py files.
        """
        with tempfile.TemporaryDirectory() as tempdir:
            subdir = os.path.join(tempdir, "subdir")
            os.makedirs(subdir)

            file1_path = os.path.join(tempdir, "file1.py")
            file2_path = os.path.join(subdir, "file2.py")

            with open(file1_path, 'w') as f:
                f.write("print('Hello from file1')\n")
                
            with open(file2_path, 'w') as f:
                f.write("print('Hello from file2 in subdir')\n")

            expected_output = f"""\
File: {file1_path}
--------------------
print('Hello from file1')

File: {file2_path}
--------------------
print('Hello from file2 in subdir')
""".strip()

            actual_output = DirectoryReader.read_and_format_py_files(tempdir).strip()
            self.assertEqual(actual_output, expected_output)

    def test_cli_functionality(self):
        """
        Short Description:
        Tests the CLI functionality for reading and formatting .py files.

        Test Strategy:
        Creates a temporary directory with .py files and runs the CLI command, then checks the output.

        Expected Outcome:
        The CLI output should match the expected formatted string with file paths and contents.
        """
        with tempfile.TemporaryDirectory() as tempdir:
            file1_path = os.path.join(tempdir, "file1.py")
            file2_path = os.path.join(tempdir, "file2.py")
            
            with open(file1_path, 'w') as f:
                f.write("print('Hello from file1')\n")
                
            with open(file2_path, 'w') as f:
                f.write("print('Hello from file2')\n")

            expected_output = f"""\
File: {file1_path}
--------------------
print('Hello from file1')

File: {file2_path}
--------------------
print('Hello from file2')
""".strip()

            # Run the CLI command and capture the output
            result = subprocess.run(['python', 'AutoChatBot/directory_reader.py', '--directory', tempdir], capture_output=True, text=True)
            actual_output = result.stdout.strip()
            self.assertEqual(actual_output, expected_output)

if __name__ == "__main__":
    unittest.main()