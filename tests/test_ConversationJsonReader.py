import unittest
import os
import sys
import tempfile
import json
from unittest.mock import patch

# Add the src directory to the Python path for imports
sys.path.append('AutoChatBot')

from ConversationJsonReader import ConversationJsonReader

class TestConversationJsonReader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a temporary directory
        cls.temp_dir = tempfile.TemporaryDirectory()

        # Create a temporary JSON file with correct format
        cls.json_file_correct_path = os.path.join(cls.temp_dir.name, 'conversation_correct.json')
        with open(cls.json_file_correct_path, 'w') as f:
            json.dump([
                {"role": "user", "content": "Hello"},
                {"role": "system", "content": "How can I assist you?"}
            ], f)

        # Create a temporary JSON file with incorrect format
        cls.json_file_incorrect_path = os.path.join(cls.temp_dir.name, 'conversation_incorrect.json')
        with open(cls.json_file_incorrect_path, 'w') as f:
            json.dump({"user": "Hello", "system": "How can I assist you?"}, f)

    @classmethod
    def tearDownClass(cls):
        # Clean up the temporary directory and its files
        cls.temp_dir.cleanup()

    def test_read_correct_json_file(self):
        reader = ConversationJsonReader(self.json_file_correct_path)
        conversations = reader.read_file(self.json_file_correct_path)
        expected_conversations = [
            {"role": "user", "content": "Hello"},
            {"role": "system", "content": "How can I assist you?"}
        ]
        self.assertEqual(conversations, expected_conversations, "The conversations were not read correctly.")

    def test_read_incorrect_json_file(self):
        with self.assertRaises(ValueError):
            reader = ConversationJsonReader(self.json_file_incorrect_path)
            reader.read_file(self.json_file_incorrect_path)

    def test_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            reader = ConversationJsonReader("/path/to/nonexistent/file")
            reader.read_file("/path/to/nonexistent/file")

if __name__ == '__main__':
    unittest.main()

