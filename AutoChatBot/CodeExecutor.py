from .PyFileExecutor import PyFileExecutor
from .ChatAPIHandler import ChatAPIHandler
from .GPTChatCompletionSaver import ChatCompletionSaver
from .CodeErrorFormatter import CodeErrorFormatter
from .ConversationPreparer import ConversationPreparer
from .RemoveLanguageDelimiters import CodeExtractor

class CodeExecutor:
    @staticmethod
    def execute_code(run_code, response, code_save_path='sandbox_scripts/myscript.py'):
        """
        Executes the provided code if run_code is True, otherwise does nothing.

        Args:
            run_code (bool): Flag indicating whether to execute the code.
            response (str): The code content to execute.
            code_save_path (str): Path to save the code file.

        Returns:
            str: Error output if there's any, otherwise None.
        """
        if run_code:
            PyFileExecutor.save_code_to_file(code_save_path, response)
            error_output = PyFileExecutor.execute_code(code_save_path)
            return error_output
        else:
            return None

    @staticmethod
    def retry_api_request(
        chat_parameters: dict,
        save_path,
        code_save_path,
        run_code,
        response_content,
        max_attempts=3,
        context_name=None
    ):
        """
        Retries API requests and executes the code if needed, using chat_parameters dict for all API parameters.
        
        See AutoChatBot/default_api_parameters.py for the expected structure of chat_parameters.

        Args:
            chat_parameters (dict): All chat/API parameters as a dictionary.
            save_path (str): Path to save the API response.
            code_save_path (str): Path to save the code file.
            run_code (bool): Flag indicating whether to execute the code.
            response_content (str): The initial code/content to execute.
            max_attempts (int): Maximum number of retry attempts.
            context_name (str, optional): The name of the context to be appended (default is None).

        Returns:
            bool: True if execution completed successfully, False otherwise.
        """
        conversation = None  # Initialize conversation variable for API requests

        for attempt in range(max_attempts):
            if conversation is not None:
                # Only make additional API call after first execution attempt
                response = ChatAPIHandler.make_api_request(chat_parameters, conversation)
                print("Chat Completion Response:", response)
                ChatCompletionSaver.save_to_file(response, save_path)
                if 'choices' in response and response['choices']:
                    response_content = response['choices'][0]['message']['content']
                else:
                    print("API response did not contain choices. Aborting.")
                    return False

            error_output = CodeExecutor.execute_code(run_code, response_content, code_save_path=code_save_path)
            extracted_code = CodeExtractor.extract_code(response_content)
            executed_code = extracted_code if extracted_code else response_content
            if code_save_path.startswith('/') or code_save_path.startswith('\\'):
                print("Warning: File path starts with a leading slash, which is unusual.")

            if error_output:
                print("Error Output:", error_output)
                conversation = CodeErrorFormatter.format_code_error(
                    code=executed_code,
                    error_output=error_output,
                )
                conversation = ConversationPreparer.str_to_dict_list(conversation)
                conversation = ConversationPreparer.extend_context(context_name, conversation)
            else:
                print("Execution completed successfully.")
                return True
        else:
            return False

