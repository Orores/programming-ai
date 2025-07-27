import os
import json
import requests
from dotenv import load_dotenv

class TogetherAIChatCompletion:
    """
    TogetherAIChatCompletion: Handles TogetherAI API chat completion requests.

    Usage:
        Pass all relevant parameters in the `chat_parameters` dict (see AutoChatBot/default_api_parameters.py
        for structure and description), plus the conversation list.

    Parameters accepted in chat_parameters include (see default_api_parameters.py for details):
        - model, temperature, max_tokens, top_p, top_k, repetition_penalty, stop_sequences

    Example:
        >>> from AutoChatBot.default_api_parameters import DEFAULT_CHAT_PARAMETERS
        >>> params = DEFAULT_CHAT_PARAMETERS.copy()
        >>> params["model"] = "cognitivecomputations/dolphin-2.5-mixtral-8x7b"
        >>> out = TogetherAIChatCompletion.make_api_request(params, conversation)
    """

    @staticmethod
    def load_api_key():
        load_dotenv()
        return os.getenv("TOGETHERAI_API_KEY")

    @staticmethod
    def make_api_request(chat_parameters: dict, conversation: list):
        """
        Perform a chat completion request to TogetherAI's API.

        Args:
            chat_parameters (dict): Chat parameters (see AutoChatBot/default_api_parameters.py for description).
                Should include model, temperature, max_tokens, top_p, top_k, repetition_penalty, stop_sequences.
            conversation (list): The conversation context.

        Returns:
            dict: The response from the TogetherAI API.
        """
        api_key = TogetherAIChatCompletion.load_api_key()
        if api_key is None:
            return {"error": {"message": "No TogetherAI API key found", "type": "auth_error"}}

        payload = {
            "model": chat_parameters.get("model", "cognitivecomputations/dolphin-2.5-mixtral-8x7b"),
            "messages": conversation,
            "max_tokens": chat_parameters.get("max_tokens", 4000),
            "temperature": chat_parameters.get("temperature", 1.0),
            "top_p": chat_parameters.get("top_p", 0.7),
            "top_k": chat_parameters.get("top_k", 50),
            "repetition_penalty": chat_parameters.get("repetition_penalty", 1.0),
            "stream": False
        }

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }

        try:
            response = requests.post(
                'https://api.together.xyz/v1/chat/completions',
                json=payload,
                headers=headers
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            return {"error": {"message": str(e), "type": "request_error"}}

        try:
            response_json = response.json()
        except json.JSONDecodeError:
            return {"error": {"message": "Invalid JSON response", "type": "json_error"}}

        return response_json

