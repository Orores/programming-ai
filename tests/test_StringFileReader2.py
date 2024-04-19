import unittest
import os
import tempfile
import sys
# Add the src directory to the Python path for imports
sys.path.append('AutoChatBot')

# Import the class to be tested
from StringFileReader import StringFileReader

class TestStringFileReader(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create a temporary directory
        cls.temp_dir = tempfile.TemporaryDirectory()

        # Create some temporary text files
        cls.file1_path = os.path.join(cls.temp_dir.name, 'file1.txt')
        with open(cls.file1_path, 'w') as f:
            f.write("This is file 1.")

        cls.file2_path = os.path.join(cls.temp_dir.name, 'file2.txt')
        with open(cls.file2_path, 'w') as f:
            f.write("This is file 2.")

    @classmethod
    def tearDownClass(cls):
        # Clean up the temporary directory and its files
        cls.temp_dir.cleanup()

    def test_read_existing_file(self):
        reader = StringFileReader(self.file1_path)
        content = reader.read_file(self.file1_path)
        expected_content = "This is file 1."
        self.assertEqual(content, expected_content, "The content of the file was not read correctly.")

    def test_read_non_existing_file(self):
        with self.assertRaises(FileNotFoundError):
            reader = StringFileReader()
            reader.read_file("/path/to/nonexistent/file")

    def test_content_type(self):
        reader = StringFileReader(self.file1_path)
        content = reader.read_file(self.file1_path)
        self.assertIsInstance(content, str, "The content read from the file is not a string.")

if __name__ == '__main__':
    unittest.main()
