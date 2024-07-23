import os
from dotenv import load_dotenv
import requests
import argparse

class GPT3ChatCompletion:
    """
    GPT3ChatCompletion: This class handles OpenAI API chat completion requests using static methods.
    
    Static methods:
    - load_api_key(): Loads the API key from the environment or .env file.
    - make_api_request(api_key, conversation, model, temperature, max_tokens, stop_sequences, frequency_penalty, presence_penalty, top_p): Sends a request to the OpenAI API with the specified parameters and returns the response.
    - update_attributes(current_values, **kwargs): Updates a dictionary of current values with provided keyword arguments.
    
    Example usage:
        conversation = [{"role": "user", "content": "Hello, who won the world series in 2020?"}]
        response = GPT3ChatCompletion.make_api_request(
            api_key="your_api_key",
            conversation=conversation,
            model="gpt-3.5-turbo",
            max_tokens=100,
            temperature=1,
            frequency_penalty=0,
            presence_penalty=0,
            top_p=1
        )
    
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

    @staticmethod
    def load_api_key():
        load_dotenv()
        return os.getenv("OPENAI_API_KEY")

    @staticmethod
    def update_attributes(current_values, **kwargs):
        for key, value in kwargs.items():
            if key in current_values:
                current_values[key] = value
            else:
                raise AttributeError(f"'GPT3ChatCompletion' object has no attribute '{key}'")
        return current_values

    @staticmethod
    def make_api_request(
            api_key,
            conversation,
            model="gpt-3.5-turbo",
            temperature=1,
            max_tokens=100,
            stop_sequences=None,
            frequency_penalty=0,
            presence_penalty=0,
            top_p=1
            ):

        if api_key is None:
            raise ValueError("API key is required")
        
        if conversation is None:
            raise ValueError("No conversation provided")
        if isinstance(conversation, str): 
            conversation = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": conversation}
            ]

        data = {
            "model": model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stop": stop_sequences,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty,
            "top_p": top_p,
            "messages": conversation
        }
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
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
    
    api_key = GPT3ChatCompletion.load_api_key()
    
    conversation = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": args.question}
    ]
    
    response = GPT3ChatCompletion.make_api_request(
        api_key=api_key,
        conversation=conversation,
        model=args.model,
        max_tokens=args.max_tokens,
        temperature=args.temperature,
        frequency_penalty=args.frequency_penalty,
        presence_penalty=args.presence_penalty,
        top_p=args.top_p,
        stop_sequences=args.stop_sequences
    )
    
    print("Chat Completion Response:", response)
