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


class ChatBot:
    """
    ChatBot: This class combines the functionality of both GPT3ChatCompletion and FileReader classes.
    It automatically reads files, determines whether they contain conversations or single questions,
    and utilizes GPT-3 for chat completion accordingly.
    """

    def __init__(self):
        self.chat_completion = GPT3ChatCompletion()
        self.parser_creator = ParserCreator()
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
            raise ValueError("No conversation or question provided.")
       
        return conversation

    def run(self):
        args = self.parser_creator.parser.parse_args()
        conversation = self.decide_conversation(args)
        if isinstance(conversation, str):
            conversation = {"role": "user", "content": conversation}
        if args.context is not None:
            try:
                context = self.context_manager.retrieve_context(args.context)
                context.append(conversation)
                conversation=context
            except FileNotFoundError:
                exit()
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


if __name__ == '__main__':
    bot = ChatBot()
    bot.run()

