import unittest
import os
import tempfile
import json
from AutoChatBot.ConversationJsonReader import ConversationJsonReader

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

        # Create a temporary JSON file with correct single file format
        cls.json_file_single_correct_path = os.path.join(cls.temp_dir.name, 'single_conversation_correct.json')
        with open(cls.json_file_single_correct_path, 'w') as f:
            json.dump({
                "subdirectory_name": {
                    "context": [
                        {"role": "user", "content": "Hi there"},
                        {"role": "system", "content": "Hello! How can I help you today?"}
                    ]
                }
            }, f)

        # Create a temporary JSON file with incorrect single file format
        cls.json_file_single_incorrect_path = os.path.join(cls.temp_dir.name, 'single_conversation_incorrect.json')
        with open(cls.json_file_single_incorrect_path, 'w') as f:
            json.dump({
                "subdirectory_name": [
                    {"role": "user", "content": "Hi there"},
                    {"role": "system", "content": "Hello! How can I help you today?"}
                ]
            }, f)

    @classmethod
    def tearDownClass(cls):
        # Clean up the temporary directory and its files
        cls.temp_dir.cleanup()

    def test_read_correct_json_file(self):
        conversations = ConversationJsonReader.read_file(self.json_file_correct_path)
        expected_conversations = [
            {"role": "user", "content": "Hello"},
            {"role": "system", "content": "How can I assist you?"}
        ]
        self.assertEqual(conversations, expected_conversations, "The conversations were not read correctly.")

    def test_read_incorrect_json_file(self):
        with self.assertRaises(ValueError):
            ConversationJsonReader.read_file(self.json_file_incorrect_path)

    def test_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            ConversationJsonReader.read_file("/path/to/nonexistent/file")

    def test_read_correct_single_json_file(self):
        conversations = ConversationJsonReader.read_file(self.json_file_single_correct_path, is_single_file=True, subdirectory_name="subdirectory_name")
        expected_conversations = [
            {"role": "user", "content": "Hi there"},
            {"role": "system", "content": "Hello! How can I help you today?"}
        ]
        self.assertEqual(conversations, expected_conversations, "The conversations were not read correctly for single file format.")

    def test_read_incorrect_single_json_file(self):
        with self.assertRaises(ValueError):
            ConversationJsonReader.read_file(self.json_file_single_incorrect_path, is_single_file=True, subdirectory_name="subdirectory_name")

    def test_subdirectory_not_found(self):
        with self.assertRaises(ValueError):
            ConversationJsonReader.read_file(self.json_file_single_correct_path, is_single_file=True, subdirectory_name="non_existent_subdirectory")

if __name__ == '__main__':
    unittest.main()
