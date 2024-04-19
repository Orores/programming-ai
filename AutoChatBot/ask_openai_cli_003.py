import argparse
from AutoChatbot.gpt3_assistant import GPT3Assistant

class AIAssistant:
    def __init__(self):
        self.assistant = GPT3Assistant()


    def extract_string_from_file(self, file):
        try:
            with open(file, 'r') as file:
                data = file.read()
                return data
        except FileNotFoundError:
            print("File not found.")
            return None

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
            reply = self.assistant.ask_question(file_question)
            if args.output_file:
                self.write_response_to_file(reply, args.output_file)
            else:
                print("Assistant's reply:", reply)
        elif args.question:
            reply = self.assistant.ask_question(args.question)
            if args.output_file:
                self.write_response_to_file(reply, args.output_file)
            else:
                print("Assistant's reply:", reply)
        else:
            parser.print_help()

if __name__ == '__main__':
    assistant = AIAssistant()
    assistant.handle_arguments()


