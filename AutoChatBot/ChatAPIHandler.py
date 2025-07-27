from .GPTChatCompletion import GPT3ChatCompletion
from .TogetherAIChatCompletion import TogetherAIChatCompletion

class ChatAPIHandler:
    @staticmethod
    def make_api_request(
        chat_parameters: dict,
        conversation: list
    ) -> dict:
        """
        Handle API request to either OpenAI or TogetherAI, based on provided chat_parameters.

        Args:
            chat_parameters (dict): Dictionary containing API request parameters. See
                AutoChatBot/default_api_parameters.py for a complete description of required and optional keys:
                - api (str): "openai" or "togetherai"
                - model, temperature, max_tokens, top_p, frequency_penalty, presence_penalty,
                  stop_sequences, top_k, repetition_penalty (see default_api_parameters.py)
            conversation (list): Conversation context as list of dictionaries.

        Returns:
            dict: The response from the chat completion API.

        Raises:
            ValueError: If an invalid API is selected.

        Examples:
            >>> from AutoChatBot.default_api_parameters import DEFAULT_CHAT_PARAMETERS
            >>> params = DEFAULT_CHAT_PARAMETERS.copy()
            >>> params["model"] = "gpt-3.5-turbo"
            >>> response = ChatAPIHandler.make_api_request(params, conversation)
        """
        api = chat_parameters.get("api", "openai")
        if api == "openai":
            return GPT3ChatCompletion.make_api_request(chat_parameters, conversation)
        elif api == "togetherai":
            return TogetherAIChatCompletion.make_api_request(chat_parameters, conversation)
        else:
            raise ValueError("Invalid API selection. Choose 'openai' or 'togetherai'.")

