import os
from dotenv import load_dotenv
import requests
import argparse

from .StringFileReader import StringFileReader
from .ConversationJsonReader import ConversationJsonReader
from .ParserCreator import ParserCreator
from .GPTChatCompletion import GPT3ChatCompletion
from .GPTChatCompletionSaver import ChatCompletionSaver
from .ContextManager import ContextManager
from .PyFileExecutor import PyFileExecutor
from .CodeErrorFormatter import CodeErrorFormatter
from .TogetherAIChatCompletion import TogetherAIChatCompletion
from .TogetherAIModelRetriever import TogetherAIModelRetriever
from .RemoveLanguageDelimiters import CodeExtractor


class ChatBot:
    """
    ChatBot: This class combines the functionality of both GPT3ChatCompletion and FileReader classes.
    It automatically reads files, determines whether they contain conversations or single questions,
    and utilizes GPT-3 or TogetherAI for chat completion accordingly.
    """

    FAIL = '\33[91m'
    OKGREEN = '\33[92m'
    OKCYAN ='\33[96m'
    ORANGE = '\33[93m'
    BOLD = '\33[1m'

    @staticmethod
    def decide_conversation(args):
        if args.file_path:
            try:
                conversation = ConversationJsonReader.read_file(args.file_path)
            except ValueError as e:
                conversation = StringFileReader.read_file(args.file_path)
        elif args.question:
            conversation = args.question
        else:
            parser = ParserCreator.create_parser()
            parser.error(ChatBot.FAIL + ChatBot.BOLD + 'Please enter the word you want the machine to say. Enter -h for help')
        return conversation

    @staticmethod
    def str_to_dict_list(conversation):
        if isinstance(conversation, str):
            conversation = [{"role": "user", "content": conversation}]
        return conversation

    @staticmethod
    def extend_context(args, conversation):
        if args.context is not None:
            context_data = ContextManager.load_context_data(context_folder='context')
            context = ContextManager.get_specific_context(context_data, args.context)
            if isinstance(context, list):  # Ensure context retrieval is successful
                context.extend(conversation)
                conversation = context
            else:
                print(context)  # Print error message if context does not exist
                exit()
        return conversation

    @staticmethod
    def make_api_request(args, conversation):
        if args.api == "openai":
            api_key = GPT3ChatCompletion.load_api_key()
            response = GPT3ChatCompletion.make_api_request(
                api_key=api_key,
                conversation=conversation,
                model=args.model,
                temperature=args.temperature,
                max_tokens=args.max_tokens,
                stop_sequences=args.stop_sequences,
                frequency_penalty=args.frequency_penalty,
                presence_penalty=args.presence_penalty,
                top_p=args.top_p,
            )
        elif args.api == "togetherai":
            api_key = TogetherAIChatCompletion.load_api_key()
            response = TogetherAIChatCompletion.make_api_request(
                conversation=conversation,
                api_key=api_key,
                model=args.model,
                temperature=args.temperature,
                max_tokens=args.max_tokens,
                top_p=args.top_p,
                top_k=args.top_k,
                repetition_penalty=args.repetition_penalty,
            )
        else:
            raise ValueError("Invalid API selection. Choose 'openai' or 'togetherai'.")
        return response

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
                response = ChatBot.make_api_request(args, conversation)
                print("Chat Completion Response:", response)
                ChatCompletionSaver.save_to_file(response, args.save_path)
                response_content = response['choices'][0]['message']['content']
            
            error_output = ChatBot.execute_code(args, response_content)
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
                conversation = ChatBot.str_to_dict_list(conversation)
                conversation = ChatBot.extend_context(args, conversation)
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
                response = ChatBot.make_api_request(args, conversation)
                print("Chat Completion Response:", response)
                ChatCompletionSaver.save_to_file(response, args.save_path)
                response_content = response['choices'][0]['message']['content']
            
            error_output = ChatBot.execute_code(args, response_content)
            
            if error_output:
                print("Error Output:", error_output)
                conversation = CodeErrorFormatter.format_code_error(
                    code=executed_code,
                    error_output=error_output,
                )
                conversation = ChatBot.str_to_dict_list(conversation)
                conversation = ChatBot.extend_context(args, conversation)
            else:
                print("Execution completed successfully.")
                return True
        else:
            return False

    @staticmethod
    def run():
        parser = ParserCreator.create_parser()
        args = parser.parse_args()
        if args.show_available_context:
            context_data = ContextManager.load_context_data(context_folder='context')
            context_names = ContextManager.get_all_context_names(context_data)
        if args.show_models:
            models = TogetherAIModelRetriever.get_available_models()
            print("Available Models for TogetherAI:\n")
            TogetherAIModelRetriever.print_models_table(models)

        if args.file_path or args.question:
            conversation = ChatBot.decide_conversation(args)
            conversation = ChatBot.str_to_dict_list(conversation)
            conversation = ChatBot.extend_context(args, conversation)
            response = ChatBot.make_api_request(args, conversation)
            print("Chat Completion Response:", response)
            ChatCompletionSaver.save_to_file(response, args.save_path)
            response_content = response['choices'][0]['message']['content']
        
        if args.run_code:
            ChatBot.retry_api_request(args, response_content)
        if args.run_code_with_unittest:
            ChatBot.run_code_with_unittest(args, response_content)


def main():
    ChatBot.run()

if __name__ == '__main__':
    main()
