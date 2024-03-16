import unittest
import os
import sys
import tempfile
import json
from unittest.mock import patch

# Add the src directory to the Python path for imports
sys.path.append('src')

from auto_file_reader import FileReader

class TestFileReader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a temporary directory
        cls.temp_dir = tempfile.TemporaryDirectory()

        # Create a temporary text file
        cls.text_file_path = os.path.join(cls.temp_dir.name, 'text.tmp')
        with open(cls.text_file_path, 'w') as f:
            f.write("This is a sample text file.")

        # Create a temporary JSON file
        cls.json_file_path = os.path.join(cls.temp_dir.name, 'conversation.json')
        with open(cls.json_file_path, 'w') as f:
            json.dump([{"role": "user", "content": "Hello"}], f)

    @classmethod
    def tearDownClass(cls):
        # Clean up the temporary directory and its files
        cls.temp_dir.cleanup()

    def test_read_text_file(self):
        reader = FileReader(self.text_file_path)
        result = reader.read_file(self.text_file_path)
        content_type = result["type"]
        content = result["content"]
        self.assertEqual(content_type, "string", "The content type of the text file was not determined correctly.")
        self.assertEqual(content, "This is a sample text file.", "The content of the text file was not read correctly.")

    def test_read_json_file(self):
        reader = FileReader(self.json_file_path)
        result = reader.read_file(self.json_file_path)
        content_type = result["type"]
        content = result["content"]
        expected_content = [{"role": "user", "content": "Hello"}]
        self.assertEqual(content_type, "conversation", "The content type of the JSON file was not determined correctly.")
        self.assertEqual(content, expected_content, "The content of the JSON file was not read correctly.")

    def test_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            reader = FileReader("/path/to/nonexistent/file")
            reader.read_file("/path/to/nonexistent/file")

if __name__ == '__main__':
    unittest.main()

