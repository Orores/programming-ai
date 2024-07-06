import unittest
import os
import sys
import tempfile
from unittest.mock import patch
from AutoChatBot.StringFileReader import StringFileReader

class TestStringFileReader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a temporary directory
        cls.temp_dir = tempfile.TemporaryDirectory()

        # Create a temporary text file
        cls.text_file_path = os.path.join(cls.temp_dir.name, 'text.tmp')
        with open(cls.text_file_path, 'w') as f:
            f.write("This is a sample text file.")

        # Create a temporary non-text file
        cls.non_text_file_path = os.path.join(cls.temp_dir.name, 'image.jpg')
        with open(cls.non_text_file_path, 'wb') as f:
            f.write(b'\x00\x01\x02\x03')

    @classmethod
    def tearDownClass(cls):
        # Clean up the temporary directory and its files
        cls.temp_dir.cleanup()

    def test_read_text_file(self):
        reader = StringFileReader(self.text_file_path)
        content = reader.read_file(self.text_file_path)
        self.assertEqual(content, "This is a sample text file.", "The content of the text file was not read correctly.")

    def test_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            reader = StringFileReader("/path/to/nonexistent/file")
            reader.read_file("/path/to/nonexistent/file")

if __name__ == '__main__':
    unittest.main()

