import unittest
from unittest.mock import patch, MagicMock
from AutoChatBot.CodeExecutor import CodeExecutor

class TestCodeExecutor(unittest.TestCase):

    @patch('AutoChatBot.CodeExecutor.PyFileExecutor')
    def test_execute_code_runs_code(self, mock_pyfile_executor):
        mock_pyfile_executor.save_code_to_file.return_value = None
        mock_pyfile_executor.execute_code.return_value = None
        
        result = CodeExecutor.execute_code(True, "print('Hello, World!')", "sandbox_scripts/test_script.py")
        
        mock_pyfile_executor.save_code_to_file.assert_called_once_with("sandbox_scripts/test_script.py", "print('Hello, World!')")
        mock_pyfile_executor.execute_code.assert_called_once_with("sandbox_scripts/test_script.py")
        self.assertIsNone(result)

    @patch('AutoChatBot.CodeExecutor.PyFileExecutor')
    def test_execute_code_does_not_run_code(self, mock_pyfile_executor):
        result = CodeExecutor.execute_code(False, "print('Hello, World!')")
        
        mock_pyfile_executor.save_code_to_file.assert_not_called()
        mock_pyfile_executor.execute_code.assert_not_called()
        self.assertIsNone(result)

    @patch('AutoChatBot.CodeExecutor.ChatAPIHandler')
    @patch('AutoChatBot.CodeExecutor.ChatCompletionSaver')
    @patch('AutoChatBot.CodeExecutor.CodeErrorFormatter')
    @patch('AutoChatBot.CodeExecutor.ConversationPreparer')
    @patch('AutoChatBot.CodeExecutor.CodeExtractor')
    @patch('AutoChatBot.CodeExecutor.PyFileExecutor')
    def test_retry_api_request_successful_execution(self, mock_pyfile_executor, mock_code_extractor, mock_conversation_preparer, mock_code_error_formatter, mock_completion_saver, mock_chat_api_handler):
        mock_pyfile_executor.save_code_to_file.return_value = None
        mock_pyfile_executor.execute_code.return_value = None
        mock_chat_api_handler.make_api_request.return_value = {
            'choices': [{'message': {'content': "print('Hello, World!')"}}]
        }
        
        result = CodeExecutor.retry_api_request(
            api="dummy_api", model="dummy_model", temperature=0.5, max_tokens=100,
            top_p=1.0, frequency_penalty=0, presence_penalty=0, stop_sequences=[],
            top_k=50, repetition_penalty=1.0, save_path="dummy_path",
            code_save_path="sandbox_scripts/test_script.py", run_code=True,
            response_content="print('Hello, World!')", max_attempts=2
        )
        
        self.assertTrue(result)
        mock_chat_api_handler.make_api_request.assert_not_called()  # Expect no API call on successful first execution
        mock_pyfile_executor.save_code_to_file.assert_called()
        mock_pyfile_executor.execute_code.assert_called()
        mock_completion_saver.save_to_file.assert_not_called()  # Expect save_to_file not called on successful first execution

    @patch('AutoChatBot.CodeExecutor.ChatAPIHandler')
    @patch('AutoChatBot.CodeExecutor.ChatCompletionSaver')
    @patch('AutoChatBot.CodeExecutor.CodeErrorFormatter')
    @patch('AutoChatBot.CodeExecutor.ConversationPreparer')
    @patch('AutoChatBot.CodeExecutor.CodeExtractor')
    @patch('AutoChatBot.CodeExecutor.PyFileExecutor')
    def test_retry_api_request_with_errors(self, mock_pyfile_executor, mock_code_extractor, mock_conversation_preparer, mock_code_error_formatter, mock_completion_saver, mock_chat_api_handler):
        mock_pyfile_executor.save_code_to_file.return_value = None
        mock_pyfile_executor.execute_code.side_effect = ["Syntax Error", None]
        mock_chat_api_handler.make_api_request.return_value = {
            'choices': [{'message': {'content': "print('Hello, World!')"}}]
        }
        mock_code_error_formatter.format_code_error.return_value = "Formatted error"
        mock_conversation_preparer.str_to_dict_list.return_value = [{'role': 'user', 'content': 'Formatted error'}]
        mock_conversation_preparer.extend_context.return_value = [{'role': 'user', 'content': 'Formatted error'}]
        
        result = CodeExecutor.retry_api_request(
            api="dummy_api", model="dummy_model", temperature=0.5, max_tokens=100,
            top_p=1.0, frequency_penalty=0, presence_penalty=0, stop_sequences=[],
            top_k=50, repetition_penalty=1.0, save_path="dummy_path",
            code_save_path="sandbox_scripts/test_script.py", run_code=True,
            response_content="print('Hello, World!')", max_attempts=2
        )
        
        self.assertTrue(result)
        mock_chat_api_handler.make_api_request.assert_called()
        mock_pyfile_executor.save_code_to_file.assert_called()
        mock_pyfile_executor.execute_code.assert_called()
        mock_completion_saver.save_to_file.assert_called()
        mock_code_error_formatter.format_code_error.assert_called()
        mock_conversation_preparer.str_to_dict_list.assert_called()
        mock_conversation_preparer.extend_context.assert_called()

    def test_run_code_with_unittest(self):
        # Placeholder test case for future implementation of run_code_with_unittest
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
