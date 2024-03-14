import requests
from dotenv import load_dotenv
import os
import datetime
import argparse

class AIAssistant:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.endpoint_url = 'https://api.openai.com/v1/chat/completions'
        self.input_file = 'question.tmp'
        self.output_file = 'response.tmp'
        self.language = ''

    def make_api_request(self, conversation):
        data = {
            "model": "gpt-3.5-turbo",
            "messages": conversation
        }
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        return requests.post(self.endpoint_url, headers=headers, json=data)

    def extract_assistant_reply(self, response):
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"Error: {response.status_code} {response.text}"

    def extract_string_from_file(self, file):
        try:
            with open(file, 'r') as file:
                data = file.read()
                return data
        except FileNotFoundError:
            print("File not found.")
            return None

    def ask_question(self, question):
        conversation = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question}
        ]

        response = self.make_api_request(conversation)

        self.language = 'English'

        return self.extract_assistant_reply(response)

    def write_response_to_file(self, response, output_file):
        with open(output_file, 'w') as file:
            file.write(response)
            print(f"Assistant's reply has been saved to {output_file}")

    def handle_arguments(self):
        parser = argparse.ArgumentParser(description="Ask a question to OpenAI's GPT-3 model")
        parser.add_argument("--question", type=str, help="The question to ask the assistant")
        parser.add_argument("--input_file", "-in", type=str, help="File containing the question")
        parser.add_argument("--output_file", "-out", type=str, help="File to write the response to")
        args = parser.parse_args()

        if args.input_file:
            file_question = self.extract_string_from_file(args.input_file)
            reply = self.ask_question(file_question)
            if args.output_file:
                self.write_response_to_file(reply, args.output_file)
            else:
                print("Assistant's reply:", reply)
        elif args.question:
            reply = self.ask_question(args.question)
            if args.output_file:
                self.write_response_to_file(reply, args.output_file)
            else:
                print("Assistant's reply:", reply)
        else:
            parser.print_help()

if __name__ == '__main__':
    assistant = AIAssistant()
    assistant.handle_arguments()
