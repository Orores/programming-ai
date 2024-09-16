import argparse
import os

from .ContextManager import ContextManager
from .ParserCreator import ParserCreator
from .GPTChatCompletionSaver import ChatCompletionSaver
from .TogetherAIModelRetriever import TogetherAIModelRetriever
from .ConversationPreparer import ConversationPreparer
from .ChatAPIHandler import ChatAPIHandler
from .CodeExecutor import CodeExecutor
from .multi_file_agent import MultiFileAgent
from .python_file_executor import PythonFileExecutor

class ChatBot:
    """
    The main ChatBot class to execute the chatbot functionalities.

    Constants
    ---------
    FAIL : str
        Red color escape code for error messages.
    OKGREEN : str
        Green color escape code for success messages.
    OKCYAN : str
        Cyan color escape code for informational messages.
    ORANGE : str
        Orange color escape code for warning messages.
    BOLD : str
        Escape code for bold text.

    Methods
    -------
    main():
        The main method to run the chatbot.
    execute_multifile_agent(reference_files: list, rewrite_files: list, question: str = None, question_file_path: str = None, debug: bool = False) -> dict:
        Executes the multi-file agent to generate and update multiple files.
    execute_files(file_paths: list) -> dict:
        Executes a list of Python files and captures their stdout and stderr outputs.
    """
    FAIL = '\33[91m'
    OKGREEN = '\33[92m'
    OKCYAN = '\33[96m'
    ORANGE = '\33[93m'
    BOLD = '\33[1m'

    @staticmethod
    def execute_multifile_agent(reference_files: list, rewrite_files: list, question: str = None, question_file_path: str = None, debug: bool = False) -> dict:
        """
        Executes the multi-file agent to generate and update multiple files based on reference files and user-provided questions.

        Parameters:
        reference_files (list): List of paths to the reference files.
        rewrite_files (list): List of paths to the rewrite files.
        question (str, optional): The question to be included in the task string. Default is `None`.
        question_file_path (str, optional): The path to the file containing the question. Default is `None`.
        debug (bool): Debug flag.

        Returns:
        dict: Dictionary with file paths as keys and generated content as values.
        """
        return MultiFileAgent.execute(reference_files, rewrite_files, question, question_file_path, debug)

    @staticmethod
    def execute_files(file_paths: list) -> dict:
        """
        Executes a list of Python files and captures their stdout and stderr outputs.

        Parameters:
        file_paths (list): List of paths to Python files to be executed.

        Returns:
        dict: Dictionary with file paths as keys and tuples of (stdout, stderr) as values.
        """
        return PythonFileExecutor.execute(file_paths)

    @staticmethod
    def main():
        """
        The main method to run the chatbot. Parses arguments and executes the chatbot logic.
        """
        parser = ParserCreator.create_parser()
        args = parser.parse_args()
        
        if args.show_available_context:
            context_data = ContextManager.load_context_data(context_folder='context')
            context_names = ContextManager.get_all_context_names(context_data)
            print("Available contexts:", context_names)
        
        if args.show_models:
            models = TogetherAIModelRetriever.get_available_models()
            print("Available Models for TogetherAI:\n")
            TogetherAIModelRetriever.print_models_table(models)

        if args.file_path or args.question:
            conversation = ConversationPreparer.decide_conversation(file_path=args.file_path, question=args.question)
            conversation = ConversationPreparer.str_to_dict_list(conversation)
            conversation = ConversationPreparer.extend_context(context_name=args.context, conversation=conversation)
            response = ChatAPIHandler.make_api_request(
                api=args.api,
                model=args.model,
                temperature=args.temperature,
                max_tokens=args.max_tokens,
                top_p=args.top_p,
                conversation=conversation,
                frequency_penalty=args.frequency_penalty,
                presence_penalty=args.presence_penalty,
                stop_sequences=args.stop_sequences,
                top_k=args.top_k,
                repetition_penalty=args.repetition_penalty
            )
            print("Chat Completion Response:", response)
            ChatCompletionSaver.save_to_file(response, args.save_path)
            response_content = response['choices'][0]['message']['content']
        
        if args.run_code:
            CodeExecutor.retry_api_request(
                api=args.api,
                model=args.model,
                temperature=args.temperature,
                max_tokens=args.max_tokens,
                top_p=args.top_p,
                frequency_penalty=args.frequency_penalty,
                presence_penalty=args.presence_penalty,
                stop_sequences=args.stop_sequences,
                top_k=args.top_k,
                repetition_penalty=args.repetition_penalty,
                save_path=args.save_path,
                code_save_path=args.code_save_path,
                run_code=args.run_code,
                response_content=response_content
            )
            
        if args.run_code_with_unittest:
            CodeExecutor.run_code_with_unittest(
                api=args.api,
                model=args.model,
                temperature=args.temperature,
                max_tokens=args.max_tokens,
                top_p=args.top_p,
                frequency_penalty=args.frequency_penalty,
                presence_penalty=args.presence_penalty,
                stop_sequences=args.stop_sequences,
                top_k=args.top_k,
                repetition_penalty=args.repetition_penalty,
                save_path=args.save_path,
                code_save_path=args.code_save_path,
                run_code=args.run_code_with_unittest,
                response_content=response_content
            )

        if args.multi_file_agent:
            result = ChatBot.execute_multifile_agent(
                args.reference_files, args.rewrite_files, args.question, args.question_file_path, args.debug)
            for file_path, content in result.items():
                # Get the directory name from the file path
                directory = os.path.dirname(file_path)
                
                # If the directory does not exist, create it
                if directory and not os.path.exists(directory):
                    os.makedirs(directory)
                
                # Write the content to the file
                with open(file_path, 'w') as file:
                    file.write(content)

            print("Generated Content:", result)

        if args.execute_files:
            exec_outputs = ChatBot.execute_files(args.execute_files)
            for file_path, (stdout, stderr) in exec_outputs.items():
                print(f"Output for {file_path}:\nSTDOUT:\n{stdout}\nSTDERR:\n{stderr}")

if __name__ == '__main__':
    ChatBot.main()
