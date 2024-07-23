import unittest
import os
import tempfile
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
        
        # Create some additional temporary text files
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

    def test_read_text_file(self):
        content = StringFileReader.read_file(self.text_file_path)
        self.assertEqual(content, "This is a sample text file.", "The content of the text file was not read correctly.")

    def test_read_existing_file1(self):
        content = StringFileReader.read_file(self.file1_path)
        self.assertEqual(content, "This is file 1.", "The content of file 1 was not read correctly.")

    def test_read_existing_file2(self):
        content = StringFileReader.read_file(self.file2_path)
        self.assertEqual(content, "This is file 2.", "The content of file 2 was not read correctly.")

    def test_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            StringFileReader.read_file("/path/to/nonexistent/file")

    def test_content_type(self):
        content = StringFileReader.read_file(self.file1_path)
        self.assertIsInstance(content, str, "The content read from the file is not a string.")

if __name__ == '__main__':
    unittest.main()
