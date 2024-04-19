import os
from dotenv import load_dotenv
import requests
import argparse

from StringFileReader import StringFileReader
from ConversationJsonReader import ConversationJsonReader
from ParserCreator import ParserCreator
from GPTChatCompletion import GPT3ChatCompletion
from GPTChatCompletionSaver import ChatCompletionSaver
from ContextManager import ContextManager
from PyFileExecutor import PyFileExecutor
from CodeErrorFormatter import CodeErrorFormatter


class ChatBot:
    """
    ChatBot: This class combines the functionality of both GPT3ChatCompletion and FileReader classes.
    It automatically reads files, determines whether they contain conversations or single questions,
    and utilizes GPT-3 for chat completion accordingly.
    """

    FAIL = '\33[91m'
    OKGREEN = '\33[92m'
    OKCYAN ='\33[96m'
    ORANGE = '\33[93m'
    BOLD = '\33[1m'

    def __init__(self):
        self.chat_completion = GPT3ChatCompletion()
        self.parser = ParserCreator().parser
        self.conversation_json_reader = ConversationJsonReader()
        self.string_file_reader = StringFileReader()
        self.openai_completion_saver = ChatCompletionSaver()
        self.context_manager = ContextManager(context_folder = 'context_prompts')

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
            try:
                context = self.context_manager.retrieve_context(args.context)
                context.extend(conversation)
                conversation=context
            except FileNotFoundError:
                exit()
        return conversation



    def run(self):
        args = self.parser.parse_args()
        if args.show_available_context:
            context_names = self.context_manager.get_all_context_names()
            print("Available Context Names:", context_names)
        else:
            conversation = self.decide_conversation(args)
            conversation = self.str_to_dict_list(conversation)
            conversation = self.extend_context(args, conversation)
            response = self.chat_completion.make_api_request(
                    conversation = conversation,
                    model = args.model,
                    temperature = args.temperature,
                    max_tokens = args.max_tokens,
                    stop_sequences = args.stop_sequences,
                    frequency_penalty = args.frequency_penalty,
                    presence_penalty = args.presence_penalty,
                    top_p = args.top_p,
                    )

            #print("Chat Completion Response:", response)
            self.openai_completion_saver.save_to_file(response, args.save_path)
            response = response['choices'][0]['message']['content']
            file_path = 'sandbox_scripts/myscript.py'
            if args.run_code:
                py_file_executor = PyFileExecutor(
                        file_path = file_path,
                        code = response,
                        )
                error_output = py_file_executor.execute()
                if error_output:
                    print("Error Output:", error_output)
                    conversation = CodeErrorFormatter.format_code_error(
                            code = code,
                            error_output = error_output,
                            ) 
                else:
                    print("Execution completed successfully.")

def main():
    bot = ChatBot()
    bot.run()


if __name__ == '__main__':
    main()
