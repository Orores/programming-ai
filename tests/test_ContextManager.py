import os
import sys

import unittest
from unittest.mock import patch, MagicMock, Mock, call
import json
import tempfile

# Add the src directory to the Python path for imports
sys.path.append('AutoChatBot')

from AutoChatBot.ContextManager import ContextManager

class TestContextManager(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.context_folder = self.temp_dir.name

    def tearDown(self):
        self.temp_dir.cleanup()

    @patch('ContextManager.ConversationJsonReader', autospec=True)
    def test_load_context_data(self, MockConversationJsonReader):
        MockConversationJsonReader_instance = MockConversationJsonReader.return_value
        MockConversationJsonReader_instance.read_file.side_effect = [
            {'test': 'data1'},
            {'test': 'data2'}
        ]

        with open(os.path.join(self.context_folder, 'file1.json'), 'w') as file1:
            print(self.context_folder)
            json.dump([{'role': 'user'},{'content': 'Hello'}], file1)
        
        with open(os.path.join(self.context_folder, 'file2.json'), 'w') as file2:
            json.dump([{'role': 'user2'},{'content': 'Hello2'}], file2)

        context_manager = ContextManager(self.context_folder)
        
        expected_context_data = {
            'file1.json': [{'role': 'user'},{'content': 'Hello'}],
            'file2.json': [{'role': 'user2'},{'content': 'Hello2'}]
        }
        self.assertEqual(context_manager.context_data, expected_context_data)

    def test_retrieve_context_existing_file(self):
        context_data = {
            'existing_file.json': [{'role': 'test', 'content': 'Test context'}]
        }
        context_manager = ContextManager(self.context_folder)
        context_manager.context_data = context_data

        retrieved_context = context_manager.retrieve_context('existing_file.json')
        
        self.assertEqual(retrieved_context, [{'role': 'test', 'content': 'Test context'}])

    def test_retrieve_context_non_existing_file(self):
        context_manager = ContextManager(self.context_folder)
        context_manager.context_data = {}

        retrieved_context = context_manager.retrieve_context('non_existing_file.json')
        
        self.assertEqual(retrieved_context, "Context file 'non_existing_file.json' does not exist.")

    def test_get_all_context_names(self):
        context_data = {
            'file1.json': [{'role': 'test1'}],
            'file2.json': [{'role': 'test2'}]
        }
        context_manager = ContextManager(self.context_folder)
        context_manager.context_data = context_data

        all_context_names = context_manager.get_all_context_names()
        expected_names = ['file1.json', 'file2.json']

        self.assertEqual(all_context_names, expected_names)

if __name__ == '__main__':
    unittest.main()
