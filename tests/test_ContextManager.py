import unittest
import tempfile
import os
import json
from AutoChatBot.ContextManager import ContextManager

class TestContextManager(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.TemporaryDirectory()

        # Create sample JSON files in the temporary directory
        context_data_1 = {
            "banana": {
                "description": "context for bots",
                "tags": ['bot', 'simple'],
                "id": '122223334',
                "context": [
                    {"role": "system", "content": "You are a helpful assistant."}
                ]
            }
        }
        context_data_2 = {
            "apple": {
                "description": "context for cats",
                "tags": ['cat', 'simple'],
                "id": '122223e34',
                "context": [
                    {"role": "system", "content": "You are a helpful cat."},
                    {"role": "user", "content": "Hello"},
                    {"role": "assistant", "content": "Hi nya"},
                    {"role": "user", "content": "do you love me"},
                    {"role": "assistant", "content": "I meow you"},
                    {"role": "user", "content": "do you drive a car?"},
                ]
            }
        }

        with open(os.path.join(self.test_dir.name, 'context1.json'), 'w') as f:
            json.dump(context_data_1, f)
        with open(os.path.join(self.test_dir.name, 'context2.json'), 'w') as f:
            json.dump(context_data_2, f)

    def tearDown(self):
        # Cleanup the temporary directory
        self.test_dir.cleanup()

    def test_load_context_data(self):
        context_data = ContextManager.load_context_data(self.test_dir.name)
        expected_data = {
            "banana": {
                "description": "context for bots",
                "tags": ['bot', 'simple'],
                "id": '122223334',
                "context": [
                    {"role": "system", "content": "You are a helpful assistant."}
                ]
            },
            "apple": {
                "description": "context for cats",
                "tags": ['cat', 'simple'],
                "id": '122223e34',
                "context": [
                    {"role": "system", "content": "You are a helpful cat."},
                    {"role": "user", "content": "Hello"},
                    {"role": "assistant", "content": "Hi nya"},
                    {"role": "user", "content": "do you love me"},
                    {"role": "assistant", "content": "I meow you"},
                    {"role": "user", "content": "do you drive a car?"},
                ]
            }
        }
        self.assertEqual(context_data, expected_data)

    def test_retrieve_context(self):
        context_data = ContextManager.load_context_data(self.test_dir.name)
        context_name = 'banana'
        retrieved_context = ContextManager.retrieve_context(context_data, context_name)
        expected_context = {
            "description": "context for bots",
            "tags": ['bot', 'simple'],
            "id": '122223334',
            "context": [
                {"role": "system", "content": "You are a helpful assistant."}
            ]
        }
        self.assertEqual(retrieved_context, expected_context)

        context_name = 'nonexistent'
        retrieved_context = ContextManager.retrieve_context(context_data, context_name)
        self.assertEqual(retrieved_context, "Context 'nonexistent' does not exist.")

    def test_get_all_context_names(self):
        context_data = ContextManager.load_context_data(self.test_dir.name)
        all_context_names = ContextManager.get_all_context_names(context_data)
        expected_context_names = ['banana', 'apple']
        self.assertEqual(sorted(all_context_names), sorted(expected_context_names))

    def test_get_specific_context(self):
        context_data = ContextManager.load_context_data(self.test_dir.name)
        specific_context = ContextManager.get_specific_context(context_data, 'apple', n=3)
        expected_context = [
            {"role": "system", "content": "You are a helpful cat."},
            {"role": "user", "content": "do you love me"},
            {"role": "assistant", "content": "I meow you"},
            {"role": "user", "content": "do you drive a car?"},
        ]
        self.assertEqual(specific_context, expected_context)

if __name__ == "__main__":
    unittest.main()
