import os
from dotenv import load_dotenv
import requests
import argparse

class GPT3ChatCompletion:
    """
    GPT3ChatCompletion: This class handles OpenAI API chat completion requests.
    
    Init parameters:
    - api_key (str, optional): The API key for authentication with the OpenAI API.
    - model (str): The model to be used for chat completion. Default is "gpt-3.5-turbo".
    - temperature (float): Controls randomness in the generation. Lower values make the generation more deterministic.
    - max_tokens (int): The maximum number of tokens to generate. Requests can use up to 4096 tokens shared between prompt and completion.
    - stop_sequences (list[str], optional): Sequences where the API should stop generating further tokens.
    - frequency_penalty (float): The penalty for frequency of tokens in the generated text.
    - presence_penalty (float): The penalty for new tokens based on their presence in the text so far.
    - top_p (float): Nucleus sampling parameter. A higher value means more diversity in the generation.
    
    Main method:
    - make_api_request(conversation): Sends a request to the OpenAI API with the specified conversation and returns the response.
    
    Example usage:
        conversation = [{"role": "user", "content": "Hello, who won the world series in 2020?"}]
        chat_completion = GPT3ChatCompletion(model="gpt-3.5-turbo", max_tokens=100)
        response = chat_completion.make_api_request(conversation)
    
    Response object example:
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

    def __init__(self, api_key=None, model="gpt-3.5-turbo", temperature=1, max_tokens=100, stop_sequences=None, frequency_penalty=0, presence_penalty=0, top_p=1):
        load_dotenv()
        self.api_key = api_key if api_key else os.getenv("OPENAI_API_KEY")
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.stop_sequences = stop_sequences
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self.top_p = top_p
        self.endpoint_url = 'https://api.openai.com/v1/chat/completions'

    def update_attributes(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{key}'")

    def make_api_request(
            self,
            conversation,
            model=None,
            temperature=None,
            max_tokens=None,
            stop_sequences=None,
            frequency_penalty=None,
            presence_penalty=None,
            top_p=None
            ):

        # Use Class defaults if None are provided
        model = model if model is not None else self.model
        temperature = temperature if temperature is not None else self.temperature
        max_tokens = max_tokens if max_tokens is not None else self.max_tokens
        stop_sequences = stop_sequences if stop_sequences is not None else self.stop_sequences
        frequency_penalty = frequency_penalty if frequency_penalty is not None else self.frequency_penalty
        presence_penalty = presence_penalty if presence_penalty is not None else self.presence_penalty
        top_p = top_p if top_p is not None else self.top_p

        # The following check does not work if the input is not a dict
        if conversation is None:
            raise ValueError("No question was asked")
        if isinstance(conversation, str): 
            conversation = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": conversation}
            ]
        data = {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "stop": self.stop_sequences,
            "frequency_penalty": self.frequency_penalty,
            "presence_penalty": self.presence_penalty,
            "top_p": self.top_p,
            "messages": conversation
        }
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        response = requests.post(self.endpoint_url, headers=headers, json=data)
        return response.json()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Command Line Interface for GPT-3 Chat Completion")
    parser.add_argument("--model", type=str, default="gpt-3.5-turbo", help="Model name for the OpenAI completion request.")
    parser.add_argument("--max_tokens", type=int, default=100, help="Maximum number of tokens to generate in the completion.")
    parser.add_argument("--temperature", type=float, default=1, help="Controls randomness: lower values make completions more deterministic.")
    parser.add_argument("--frequency_penalty", type=float, default=0, help="Penalty for frequent tokens, increasing this value produces more varied results.")
    parser.add_argument("--presence_penalty", type=float, default=0, help="Penalty for new tokens, increasing this value encourages new tokens in the completion.")
    parser.add_argument("--top_p", type=float, default=1, help="Nucleus sampling: top p of the probability mass is considered for sampling.")
    parser.add_argument("--stop_sequences", nargs='*', help="Sequences where the API should stop generating further tokens.")
    parser.add_argument("--question", type=str, help="The question or prompt to ask the model.")

    args = parser.parse_args()
    chat_completion = GPT3ChatCompletion(
        model=args.model,
        max_tokens=args.max_tokens,
        temperature=args.temperature,
        frequency_penalty=args.frequency_penalty,
        presence_penalty=args.presence_penalty,
        top_p=args.top_p,
        stop_sequences=args.stop_sequences
    )

    conversation = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": args.question}
    ]
    
    response = chat_completion.make_api_request(conversation)
    print("Chat Completion Response:", response)

