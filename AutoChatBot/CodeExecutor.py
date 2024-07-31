from .PyFileExecutor import PyFileExecutor
from .ChatAPIHandler import ChatAPIHandler
from .GPTChatCompletionSaver import ChatCompletionSaver
from .CodeErrorFormatter import CodeErrorFormatter
from .ConversationPreparer import ConversationPreparer
from .RemoveLanguageDelimiters import CodeExtractor

class CodeExecutor:
    @staticmethod
    def execute_code(args, response):
        file_path = 'sandbox_scripts/myscript.py'
        if args.run_code:
            error_output = PyFileExecutor.save_code_to_file(file_path, response)
            error_output = PyFileExecutor.execute_code(file_path)
            return error_output
        else:
            return None

    @staticmethod
    def retry_api_request(args, response_content, max_attempts=3):
        conversation = None  # Initialize conversation variable for API requests

        for attempt in range(max_attempts):
            if conversation is not None:
                # Make an API request only after the initial attempt
                response = ChatAPIHandler.make_api_request(args, conversation)
                print("Chat Completion Response:", response)
                ChatCompletionSaver.save_to_file(response, args.save_path)
                response_content = response['choices'][0]['message']['content']
            
            error_output = CodeExecutor.execute_code(args, response_content)
            extracted_code = CodeExtractor.extract_code(response_content)
            executed_code = extracted_code if extracted_code else response_content
            if file_path.startswith('/') or file_path.startswith('\\'):
                print("Warning: File path starts with a leading slash, which is unusual.")

            if error_output:
                print("Error Output:", error_output)
                conversation = CodeErrorFormatter.format_code_error(
                    code=executed_code,
                    error_output=error_output,
                )
                conversation = ConversationPreparer.str_to_dict_list(conversation)
                conversation = ConversationPreparer.extend_context(args, conversation)
            else:
                print("Execution completed successfully.")
                return True
        else:
            return False

    @staticmethod
    def run_code_with_unittest(args, response_content, max_attempts=3):
        conversation = None  # Initialize conversation variable for API requests

        for attempt in range(max_attempts):
            if conversation is not None:
                # Make an API request only after the initial attempt
                response = ChatAPIHandler.make_api_request(args, conversation)
                print("Chat Completion Response:", response)
                ChatCompletionSaver.save_to_file(response, args.save_path)
                response_content = response['choices'][0]['message']['content']
            
            error_output = CodeExecutor.execute_code(args, response_content)
            
            if error_output:
                print("Error Output:", error_output)
                conversation = CodeErrorFormatter.format_code_error(
                    code=executed_code,
                    error_output=error_output,
                )
                conversation = ConversationPreparer.str_to_dict_list(conversation)
                conversation = ConversationPreparer.extend_context(args, conversation)
            else:
                print("Execution completed successfully.")
                return True
        else:
            return False
