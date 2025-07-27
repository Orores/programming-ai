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
        current_directory = os.getcwd()
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        return api_key 

    @staticmethod
    def update_attributes(current_values, **kwargs):
        for key, value in kwargs.items():
            if key in current_values:
                current_values[key] = value
            else:
                raise AttributeError(f"'GPT3ChatCompletion' object has no attribute '{key}'")
        return current_values

    @staticmethod
    def extract_text_from_response(response):
        """
        Short Description:
        Extracts the text content from the OpenAI API response object.

        Parameters:
        response (dict): The response object returned by the OpenAI API.
            Example:
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

        Returns:
        str: The content of the response message.
            Example: "The Los Angeles Dodgers won the 2020 World Series"

        Raises:
        ValueError: If the response format is invalid or does not contain the expected keys.
            Example: ValueError("Invalid response format")

        How to Use:
        This method can be used to extract only the text content from the response object returned by the OpenAI API.

        Usage Example:
        >>> response = {
        >>>     'id': 'chatcmpl-939gfxWbMKlqGh8hkPG5IvEO6SYDq',
        >>>     'object': 'chat.completion',
        >>>     'created': 1710539249,
        >>>     'model': 'gpt-3.5-turbo-0125',
        >>>     'choices': [{
        >>>         'index': 0,
        >>>         'message': {'role': 'assistant', 'content': 'The Los Angeles Dodgers won the 2020 World Series'},
        >>>         'logprobs': None,
        >>>         'finish_reason': 'stop'
        >>>     }],
        >>>     'usage': {'prompt_tokens': 19, 'completion_tokens': 9, 'total_tokens': 28},
        >>>     'system_fingerprint': 'fp_4f2ebda25a'
        >>> }
        >>> text = GPT3ChatCompletion.extract_text_from_response(response)
        >>> print(text)
        "The Los Angeles Dodgers won the 2020 World Series"
        """
        try:
            return response['choices'][0]['message']['content']
        except (KeyError, IndexError):
            raise ValueError("Invalid response format")

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

