import sys
sys.path.append('src')

import argparse
from GPTChatCompletion import GPT3ChatCompletion
from auto_file_reader import FileReader

class ChatBot:
    """
    ChatBot: This class combines the functionality of both GPT3ChatCompletion and FileReader classes.
    It automatically reads files, determines whether they contain conversations or single questions,
    and utilizes GPT-3 for chat completion accordingly.
    """

    def __init__(self):
        self.file_reader = FileReader()
        self.chat_completion = GPT3ChatCompletion()

    def run(self):
        parser = argparse.ArgumentParser(description="Command Line Interface for Chat Bot")
        self.file_reader.setup_args(parser)  # Setup arguments for file path
        self.chat_completion.setup_args(parser)  # Setup arguments for chat completion

        args = parser.parse_args()

        # Read file and determine content type
        file_content = self.file_reader.read_file(args.file_path)
        if file_content["type"] == 'conversation':
            # If the file contains a conversation, use it as input to chat completion
            conversation = file_content["content"]
            response = self.chat_completion.make_api_request(conversation)
        else:
            # If the file contains a single question, use it as input to chat completion
            question = file_content["content"]
            conversation = [{"role": "user", "content": question}]
            response = self.chat_completion.make_api_request(conversation)

        print("Chat Completion Response:", response)

if __name__ == '__main__':
    bot = ChatBot()
    bot.run()

