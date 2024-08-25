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
            error_output = PyFileExecutor.save_code_to_file(code_save_path, response)
            error_output = PyFileExecutor.execute_code(code_save_path)
            return error_output
        else:
            return None

    @staticmethod
    def retry_api_request(api, model, temperature, max_tokens, top_p, frequency_penalty, presence_penalty, stop_sequences, top_k, repetition_penalty, save_path, code_save_path, run_code, response_content, max_attempts=3, context_name=None):
        """
        Retries API requests and executes the code if needed.

        Args:
            api (str): The API endpoint.
            model (str): The model to use for the API request.
            temperature (float): Sampling temperature.
            max_tokens (int): Maximum number of tokens.
            top_p (float): Nucleus sampling probability.
            frequency_penalty (float): Frequency penalty.
            presence_penalty (float): Presence penalty.
            stop_sequences (list): Stop sequences for the API.
            top_k (int): Top-K sampling.
            repetition_penalty (float): Repetition penalty.
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
                # Make an API request only after the initial attempt
                response = ChatAPIHandler.make_api_request(api, model, temperature, max_tokens, top_p, conversation, frequency_penalty, presence_penalty, stop_sequences, top_k, repetition_penalty)
                print("Chat Completion Response:", response)
                ChatCompletionSaver.save_to_file(response, save_path)
                response_content = response['choices'][0]['message']['content']
            
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

