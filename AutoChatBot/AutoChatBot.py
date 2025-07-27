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
from .PyFileExecutor import PyFileExecutor
from .default_api_parameters import DEFAULT_CHAT_PARAMETERS

class ChatBot:
    """
    The main ChatBot class to execute the chatbot functionalities.

    Usage of chat_parameters:
    -------------------------
    Wherever chat completions are requested, the parameters are bundled into a single dictionary called `chat_parameters`.
    The structure of this dict is detailed in AutoChatBot/default_api_parameters.py. Update or extend this dict as needed 
    for new settings or models.

    Methods
    -------
    main():
        The main method to run the chatbot.
    execute_multifile_agent(reference_files: list, rewrite_files: list, question: str = None, question_file: str = None, args = None, debug: bool = False) -> dict:
        Executes the multi-file agent to generate and update multiple files.
    """

    FAIL = '\33[91m'      # red, error
    OKGREEN = '\33[92m'   # green, success
    OKCYAN = '\33[96m'    # cyan, info
    ORANGE = '\33[93m'    # orange, warning
    BOLD = '\33[1m'       # bold

    @staticmethod
    def execute_multifile_agent(reference_files: list, rewrite_files: list, question: str = None, question_file: str = None, args = None, debug: bool = False) -> dict:
        """
        Executes the multi-file agent to generate and update multiple files based on reference files and user-provided questions.

        Parameters:
        reference_files (list): List of paths to the reference files. Can be an empty list.
        rewrite_files (list): List of paths to the rewrite files.
        question (str, optional): The question to be included in the task string. Default is `None`.
        question_file (str, optional): The path to the file containing the question. Default is `None`.
        args (Namespace): Parsed CLI arguments for API call.
        debug (bool): Debug flag.

        Returns:
        dict: Dictionary with file paths as keys and generated content as values.
        """
        return MultiFileAgent.execute(reference_files or [], rewrite_files, question, question_file, args, debug)

    @staticmethod
    def gather_chat_parameters_from_args(args) -> dict:
        """
        Gather chat parameters dictionary from parsed argparse args, using the default parameters as template.

        Returns:
            dict: Chat parameters, structure as in AutoChatBot/default_api_parameters.py.
        """
        chat_parameters = DEFAULT_CHAT_PARAMETERS.copy()
        arg_fields = [
            "api", "model", "temperature", "max_tokens", "top_p", "frequency_penalty", "presence_penalty",
            "stop_sequences", "top_k", "repetition_penalty"
        ]
        for field in arg_fields:
            if hasattr(args, field) and getattr(args, field) is not None:
                chat_parameters[field] = getattr(args, field)
        return chat_parameters

    @staticmethod
    def main():
        """
        The main method to run the chatbot. Parses arguments and executes the chatbot logic.
        All chat/completions API settings are handled through the chat_parameters dictionary, see AutoChatBot/default_api_parameters.py.
        """
        parser = ParserCreator.create_parser()
        args = parser.parse_args()
        
        if getattr(args, "show_available_context", False):
            context_data = ContextManager.load_context_data(context_folder='context')
            context_names = ContextManager.get_all_context_names(context_data)
            print("Available contexts:", context_names)
        
        if getattr(args, "show_models", False):
            models = TogetherAIModelRetriever.get_available_models()
            print("Available Models for TogetherAI:\n")
            TogetherAIModelRetriever.print_models_table(models)

        chat_parameters = ChatBot.gather_chat_parameters_from_args(args)
        response_content = None  # Ensure scope
        
        if getattr(args, "file_path", None) or getattr(args, "question", None):
            conversation = ConversationPreparer.decide_conversation(file_path=getattr(args, "file_path", None), question=getattr(args, "question", None))
            conversation = ConversationPreparer.str_to_dict_list(conversation)
            conversation = ConversationPreparer.extend_context(context_name=getattr(args, "context", None), conversation=conversation)
            response = ChatAPIHandler.make_api_request(
                chat_parameters=chat_parameters,
                conversation=conversation,
            )
            print("Chat Completion Response:", response)
            ChatCompletionSaver.save_to_file(response, getattr(args, "save_path", None))
            # Only set response_content if response has 'choices'
            if 'choices' in response and response['choices']:
                response_content = response['choices'][0]['message']['content']
        
        if getattr(args, "run_code", False):
            CodeExecutor.retry_api_request(
                chat_parameters=chat_parameters,
                save_path=getattr(args, "save_path", None),
                code_save_path=getattr(args, "code_save_path", None),
                run_code=getattr(args, "run_code", False),
                response_content=response_content
            )
            
        if getattr(args, "multi_file_agent", False):
            result = ChatBot.execute_multifile_agent(
                getattr(args, "reference_files", []),
                getattr(args, "rewrite_files", []),
                getattr(args, "question", None),
                getattr(args, "question_file", None),
                args, getattr(args, "debug", False)
            )
            for file_path, content in result.items():
                directory = os.path.dirname(file_path)
                if directory and not os.path.exists(directory):
                    os.makedirs(directory)
                with open(file_path, 'w') as file:
                    file.write(content)
            print("Generated Content:", result)

        if getattr(args, "execute_files", None):
            exec_outputs = {}
            for file_path in args.execute_files:
                stdout, stderr = PyFileExecutor.execute_code(file_path)
                exec_outputs[file_path] = (stdout, stderr)
            for file_path, (stdout, stderr) in exec_outputs.items():
                print(f"Output for {file_path}:\nSTDOUT:\n{stdout}\nSTDERR:\n{stderr}")

if __name__ == '__main__':
    ChatBot.main()
