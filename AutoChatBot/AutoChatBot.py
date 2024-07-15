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

    def __init__(self):
        self.gpt3_chat_completion = GPT3ChatCompletion()
        self.togetherai_chat_completion = TogetherAIChatCompletion()
        self.parser = ParserCreator().parser
        self.conversation_json_reader = ConversationJsonReader()
        self.string_file_reader = StringFileReader()
        self.openai_completion_saver = ChatCompletionSaver()
        self.togetherai_model_retriever = TogetherAIModelRetriever()  # Instantiate the new class

    def decide_conversation(self, args):
        if args.file_path:
            try:
                conversation = self.conversation_json_reader.read_file(args.file_path)
            except ValueError as e:
                conversation = self.string_file_reader.read_file(args.file_path)
        elif args.question:
            conversation = args.question
        else:
            self.parser.error(self.FAIL + self.BOLD + 'Please enter the word you want the machine to say. Enter -h for help')
        return conversation

    def str_to_dict_list(self, conversation):
        if isinstance(conversation, str):
            conversation = [{"role": "user", "content": conversation}]
        return conversation

    def extend_context(self, args, conversation):
        if args.context is not None:
            self.context_manager = ContextManager(context_folder = 'context_prompts/context.json', is_single_file = True)
            try:
                context = self.context_manager.retrieve_context(args.context)
                context.extend(conversation)
                conversation = context
            except FileNotFoundError:
                exit()
        return conversation

    def make_api_request(self, args, conversation):
        if args.api == "openai":
            response = self.gpt3_chat_completion.make_api_request(
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
            response = self.togetherai_chat_completion.make_api_request(
                conversation=conversation
            )
        else:
            raise ValueError("Invalid API selection. Choose 'openai' or 'togetherai'.")
        return response

    def execute_code(self, args, response):
        file_path = 'sandbox_scripts/myscript.py'
        if args.run_code:
            py_file_executor = PyFileExecutor(
                file_path=file_path,
                code=response,
            )
            error_output = py_file_executor.save_code_to_file(file_path, response)
            error_output = py_file_executor.execute_code(file_path)
            return error_output
        else:
            return None

    def retry_api_request(self, args, response_content, max_attempts=3):
        conversation = None  # Initialize conversation variable for API requests

        for attempt in range(max_attempts):
            if conversation is not None:
                # Make an API request only after the initial attempt
                response = self.make_api_request(args, conversation)
                print("Chat Completion Response:", response)
                self.openai_completion_saver.save_to_file(response, args.save_path)
                response_content = response['choices'][0]['message']['content']
            
            error_output = self.execute_code(args, response_content)
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
                conversation = self.str_to_dict_list(conversation)
                conversation = self.extend_context(args, conversation)
            else:
                print("Execution completed successfully.")
                return True
        else:
            return False

    def run_code_with_unittest(self, args, response_content, max_attempts=3):
        conversation = None  # Initialize conversation variable for API requests

        for attempt in range(max_attempts):
            if conversation is not None:
                # Make an API request only after the initial attempt
                response = self.make_api_request(args, conversation)
                print("Chat Completion Response:", response)
                self.openai_completion_saver.save_to_file(response, args.save_path)
                response_content = response['choices'][0]['message']['content']
            
            error_output = self.execute_code(args, response_content)
            
            if error_output:
                print("Error Output:", error_output)
                conversation = CodeErrorFormatter.format_code_error(
                    code=executed_code,
                    error_output=error_output,
                )
                conversation = self.str_to_dict_list(conversation)
                conversation = self.extend_context(args, conversation)
            else:
                print("Execution completed successfully.")
                return True
        else:
            return False



    def run(self):
        args = self.parser.parse_args()
        if args.show_available_context:
            # Alternatively you can just pass the directory and set "is_single_file" to false
            self.context_manager = ContextManager(context_folder = 'context_prompts/context.json', is_single_file = True)
            context_names = self.context_manager.get_all_context_names()
            print("Available Context Names:", context_names)
        if args.show_models:
            models = self.togetherai_model_retriever.get_available_models()
            print("Available Models for TogetherAI:\n")
            self.togetherai_model_retriever.print_models_table(models)

        if args.file_path or args.question:
            conversation = self.decide_conversation(args)
            conversation = self.str_to_dict_list(conversation)
            conversation = self.extend_context(args, conversation)
            response = self.make_api_request(args, conversation)
            print("Chat Completion Response:", response)
            self.openai_completion_saver.save_to_file(response, args.save_path)
            response_content = response['choices'][0]['message']['content']
        
        if args.run_code:
            success = self.retry_api_request(args, response_content)
        if args.run_code_with_unittest:
            success = self.run_code_with_unittest(args, response_content)




def main():
    bot = ChatBot()
    bot.run()

if __name__ == '__main__':
    main()
