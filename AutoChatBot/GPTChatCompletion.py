import os
from dotenv import load_dotenv
import requests

class GPT3ChatCompletion:
    """
    GPT3ChatCompletion: Handles OpenAI API chat completion requests.

    Usage:
        Pass all relevant parameters in the `chat_parameters` dict (see AutoChatBot/default_api_parameters.py
        for structure and description), plus the conversation list.

    Parameters accepted in chat_parameters include (see default_api_parameters.py for details):
        - model, temperature, max_tokens, top_p, frequency_penalty, presence_penalty, stop_sequences

    Example:
        >>> from AutoChatBot.default_api_parameters import DEFAULT_CHAT_PARAMETERS
        >>> params = DEFAULT_CHAT_PARAMETERS.copy()
        >>> params["model"] = "gpt-3.5-turbo"
        >>> out = GPT3ChatCompletion.make_api_request(params, conversation)

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
    def extract_text_from_response(response):
        """
        Extracts the text content from the OpenAI API response object.

        Returns:
            str: The text content, or raises ValueError if missing.

        See the parent class docstring and default_api_parameters.py for example response.
        """
        try:
            return response['choices'][0]['message']['content']
        except (KeyError, IndexError):
            raise ValueError("Invalid response format")


    @staticmethod
    def make_api_request(chat_parameters: dict, conversation: list):
        """
        Perform a chat completion request to OpenAI's API.

        Args:
            chat_parameters (dict): Chat parameters (see AutoChatBot/default_api_parameters.py for description).
                Must include model, temperature, max_tokens, top_p, frequency_penalty, presence_penalty, stop_sequences.
            conversation (list): The conversation context.

        Returns:
            dict: The response dictionary from the OpenAI API.
        """
        api_key = GPT3ChatCompletion.load_api_key()
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
            "model":              chat_parameters.get("model", "gpt-3.5-turbo"),
            "temperature":        chat_parameters.get("temperature", 1.0),
            "max_tokens":         chat_parameters.get("max_tokens", 100),
            "top_p":              chat_parameters.get("top_p", 1.0),
            "frequency_penalty":  chat_parameters.get("frequency_penalty", 0),
            "presence_penalty":   chat_parameters.get("presence_penalty", 0),
            "stop":               chat_parameters.get("stop_sequences", None),
            "messages":           conversation,
        }
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
        return response.json()


