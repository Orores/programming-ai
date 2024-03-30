import os
from dotenv import load_dotenv
import requests
import argparse

from StringFileReader import StringFileReader
from ConversationJsonReader import ConversationJsonReader
from ParserCreator import ParserCreator
from GPTChatCompletion import GPT3ChatCompletion


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
        response = self.chat_completion.make_api_request(conversation)

        print("Chat Completion Response:", response)

if __name__ == '__main__':
    bot = ChatBot()
    bot.run()

