import unittest
from unittest.mock import patch, mock_open
import json
from AutoChatBot.ContextManager import ContextManager

class TestContextManager(unittest.TestCase):

    @patch('AutoChatBot.ContextManager.pkg_resources.resource_filename')
    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({
        "banana": {
            "context": [
                {"role": "system", "content": "You are a helpful assistant."}
            ]
        }
    }))
    def test_load_context_data_single_file(self, mock_open, mock_resource_filename):
        mock_resource_filename.return_value = 'mocked_path'

        context_file = 'context_prompts/context.json'
        context_data = ContextManager.load_context_data(context_folder=context_file, is_single_file=True)

        expected_data = {
            'banana': [
                {'role': 'system', 'content': 'You are a helpful assistant.'}
            ]
        }

        self.assertEqual(context_data, expected_data)

    def test_retrieve_context(self):
        context_data = {
            'banana': [
                {'role': 'system', 'content': 'You are a helpful assistant.'}
            ]
        }

        context_name = 'banana'
        retrieved_context = ContextManager.retrieve_context(context_data, context_name)
        expected_context = [
            {'role': 'system', 'content': 'You are a helpful assistant.'}
        ]
        self.assertEqual(retrieved_context, expected_context)

        context_name = 'apple'
        retrieved_context = ContextManager.retrieve_context(context_data, context_name)
        self.assertEqual(retrieved_context, "Context 'apple' does not exist.")

    def test_get_all_context_names(self):
        context_data = {
            'banana': [
                {'role': 'system', 'content': 'You are a helpful assistant.'}
            ],
            'apple': [
                {'role': 'system', 'content': 'You are a friendly assistant.'}
            ]
        }

        all_context_names = ContextManager.get_all_context_names(context_data)
        expected_context_names = ['banana', 'apple']
        self.assertEqual(all_context_names, expected_context_names)

if __name__ == "__main__":
    unittest.main()
