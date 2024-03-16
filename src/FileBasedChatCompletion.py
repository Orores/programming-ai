import json
import logging
import sys
import argparse
from pathlib import Path
from src.GPTChatCompletion import GPT3ChatCompletion  # Ensure this path matches your project structure
"""
GPT3ChatCompletion: This class handles OpenAI API chat completion requests.
- Init parameters: api_key (str, optional), model (str), temperature (float), max_tokens (int), stop_sequences (list[str], optional), frequency_penalty (float), presence_penalty (float), top_p (float). 
- Main method: make_api_request(conversation) where conversation is a list of dicts formatted as [{"role": "user", "content": "Your question"}].
- Example usage:
    conversation = [{"role": "user", "content": "Hello, who won the world series in 2020?"}]
    chat_completion = GPT3ChatCompletion(model="gpt-3.5-turbo", max_tokens=100)
    response = chat_completion.make_api_request(conversation)
- Response object example:
    {
        'id': 'chatcmpl-939gfxWbMKlqGh8hkPG5IvEO6SYDq',
        'object': 'chat.completion',
        'created': 1710539249,
        'model': 'gpt-3.5-turbo-0125',
        'choices': [{
            'index': 0,
            'message': {'role': 'assistant', 'content': 'The Los Angeles Dodgers won the 2020 World Series'},
            'logprobs': None,
            'finish_reason': 'stop'
        }],
        'usage': {'prompt_tokens': 19, 'completion_tokens': 9, 'total_tokens': 28},
        'system_fingerprint': 'fp_4f2ebda25a'
    }
"""

# Setup logging
logging.basicConfig(filename='assistant.log', level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

class FileBasedChatCompletion:
    """
    FileBasedChatCompletion: Extends GPT3ChatCompletion to handle file inputs/outputs.
    - Reads questions from .tmp or conversations from .json, writes responses to .tmp.
    - Attributes:
      - input_path: Path to the input file, defaults to 'question.tmp'.
      - output_path: Path to the output file, defaults to 'response.tmp'.
      - model_params: Dict with model configuration parameters.
    - Usage:
      chat_completion = FileBasedChatCompletion(input_path="input.json", output_path="output.tmp", max_tokens=100, ...)
      chat_completion.execute()
    - Output example:
      Response text written to 'output.tmp', containing the model's reply to the input question/conversation.
    """
    def __init__(self, input_path=None, output_path='response.tmp', **kwargs):
        self.input_path = Path(input_path if input_path else 'question.tmp')
        self.output_path = Path(output_path)
        self.model_params = kwargs
        self.chat_completion = GPT3ChatCompletion(**self.model_params)

    def read_input(self):
        if self.input_path.suffix == '.json':
            try:
                with self.input_path.open('r') as file:
                    return json.load(file)
            except FileNotFoundError:
                logging.error(f'File not found: {self.input_path}')
                sys.exit(f'Error: Input file not found - {self.input_path}')
        elif self.input_path.suffix == '.tmp':
            try:
                with self.input_path.open('r') as file:
                    return [{"role": "user", "content": file.read().strip()}]
            except FileNotFoundError:
                return None  # Return None to handle prompting user later
        else:
            logging.error('Invalid file extension. Please provide a .tmp or .json file.')
            sys.exit('Error: Invalid file extension. Use .tmp for questions and .json for conversations.')

    def write_output(self, response):
        with self.output_path.open('w') as file:
            file.write(response['choices'][0]['message']['content'])

    def execute(self):
        conversation = self.read_input()
        if conversation is None:
            question = input('Input file not found. Please enter your question: ')
            conversation = [{"role": "user", "content": question}]
        response = self.chat_completion.make_api_request(conversation)
        self.write_output(response)

class CLIHandler:
    def __init__(self):
        self.parser = self._setup_parser()

    def _setup_parser(self):
        parser = argparse.ArgumentParser(description="CLI for File-Based Chat Completion with GPT-3")
        parser.add_argument("--input", type=str, help="Path to the input file (.tmp or .json)")
        parser.add_argument("--output", type=str, default="response.tmp", help="Path to the output file (.tmp)")
        # Add arguments for GPT-3 parameters
        parser.add_argument("--model", type=str, default="text-davinci-003", help="Model name")
        parser.add_argument("--max_tokens", type=int, default=100, help="Maximum number of tokens")
        parser.add_argument("--temperature", type=float, default=0.7, help="Temperature")
        parser.add_argument("--top_p", type=float, default=1.0, help="Top P")
        parser.add_argument("--frequency_penalty", type=float, default=0.0, help="Frequency Penalty")
        parser.add_argument("--presence_penalty", type=float, default=0.0, help="Presence Penalty")
        # Add more model parameters as needed
        return parser

    def run(self):
        args = self.parser.parse_args()
        # Pass all CLI arguments as model parameters to FileBasedChatCompletion
        chat_completion = FileBasedChatCompletion(
            input_path=args.input,
            output_path=args.output,
            model=args.model,
            max_tokens=args.max_tokens,
            temperature=args.temperature,
            top_p=args.top_p,
            frequency_penalty=args.frequency_penalty,
            presence_penalty=args.presence_penalty
            # Add more parameters here as needed
        )
        chat_completion.execute()

if __name__ == '__main__':
    cli_handler = CLIHandler()
    cli_handler.run()

