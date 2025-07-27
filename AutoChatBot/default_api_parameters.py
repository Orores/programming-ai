"""
AutoChatBot/default_api_parameters.py

This module defines the default chat API parameters used throughout the AutoChatBot project for making requests to chat-completion APIs (OpenAI or TogetherAI).

Data Structure:
---------------
The parameters are stored in a dictionary named `DEFAULT_CHAT_PARAMETERS` with the following keys:

- api (str): Which API service to use. Accepts "openai" or "togetherai".
- model (str): The model to be used, e.g., "gpt-3.5-turbo" or "cognitivecomputations/dolphin-2.5-mixtral-8x7b".
- temperature (float): Controls randomness. Lower values make the output more deterministic.
- max_tokens (int): The maximum number of tokens to generate in the completion.
- top_p (float): Nucleus sampling; considers results of the tokens with top_p probability mass.
- frequency_penalty (float): Number penalization for frequent tokens in the output.
- presence_penalty (float): Number penalization for tokens that appear for the first time.
- stop_sequences (list or None): A list of token sequences where the API will stop generating further tokens.
- top_k (int): Top-k sampling, controls the diversity for TogetherAI.
- repetition_penalty (float): Penalty for repetition in TogetherAI.

Example Usage:
--------------
from AutoChatBot.default_api_parameters import DEFAULT_CHAT_PARAMETERS

custom_params = DEFAULT_CHAT_PARAMETERS.copy()
custom_params["model"] = "gpt-3.5-turbo"

# Pass custom_params to ChatAPIHandler.make_api_request(custom_params, conversation)
"""

DEFAULT_CHAT_PARAMETERS = {
    "api": "openai",
    "model": "gpt-4.1",
    "temperature": 0.8,
    "max_tokens": 4000,
    "top_p": 1.0,
    "frequency_penalty": 0.0,
    "presence_penalty": 0.0,
    "stop_sequences": None,
    "top_k": 50,
    "repetition_penalty": 1.0,
}
