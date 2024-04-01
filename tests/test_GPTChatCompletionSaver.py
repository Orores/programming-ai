import os
# Add the src directory to the Python path for imports
import sys
sys.path.append('src')

import unittest
import tempfile
from GPTChatCompletionSaver import ChatCompletionSaver

class TestChatCompletionSaver(unittest.TestCase):
    def setUp(self):
        self.response_data = {
            'id': 'chatcmpl-98SUfXPKMoIF4iIge0cjrXUapUzC6',
            'object': 'chat.completion',
            'created': 1711803181,
            'model': 'gpt-3.5-turbo-0125',
            'choices': [{
                'index': 0,
                'message': {'role': 'assistant', 'content': 'Hello! How can I assist you today?'},
                'logprobs': None,
                'finish_reason': 'stop'
            }],
            'usage': {'prompt_tokens': 18, 'completion_tokens': 9, 'total_tokens': 27},
            'system_fingerprint': 'fp_3bc1b5746c'
        }
        self.temp_dir = tempfile.TemporaryDirectory()  # Create temporary directory
        self.save_path = os.path.join(self.temp_dir.name, 'test_saved_message.txt')
        self.completion_saver = ChatCompletionSaver()

    def tearDown(self):
        self.temp_dir.cleanup()  # Clean up temporary directory

    def test_save_to_file(self):
        self.completion_saver.save_to_file(self.response_data, self.save_path)
        self.assertTrue(os.path.exists(self.save_path))  # Check if file exists
        with open(self.save_path, 'r') as file:
            content = file.read().strip()
            self.assertEqual(content, 'Hello! How can I assist you today?')  # Check content

if __name__ == '__main__':
    unittest.main()

