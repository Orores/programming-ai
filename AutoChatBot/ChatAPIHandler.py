from .GPTChatCompletion import GPT3ChatCompletion
from .TogetherAIChatCompletion import TogetherAIChatCompletion

class ChatAPIHandler:
    @staticmethod
    def make_api_request(
        api: str,
        model: str,
        temperature: float,
        max_tokens: int,
        top_p: float,
        conversation: list,
        frequency_penalty: float = 0.0,
        presence_penalty: float = 0.0,
        stop_sequences: list = None,
        top_k: int = 50,
        repetition_penalty: float = 1.0
    ) -> dict:
        """
        Handle API request to either OpenAI or TogetherAI based on the provided arguments.

        Args:
            api (str): The API to use, either 'openai' or 'togetherai'.
            model (str): The model name to use for the completion request.
            temperature (float): Controls randomness: lower values make completions more deterministic.
            max_tokens (int): Maximum number of tokens to generate in the completion.
            top_p (float): Nucleus sampling: top p of the probability mass is considered for sampling.
            conversation (list): The conversation context as a list of dictionaries.
            frequency_penalty (float, optional): Penalty for frequent tokens. Defaults to 0.0.
            presence_penalty (float, optional): Penalty for new tokens. Defaults to 0.0.
            stop_sequences (list, optional): Sequences where the API should stop generating further tokens. Defaults to None.
            top_k (int, optional): Top-k sampling: The number of highest probability vocabulary tokens to keep for sampling. Defaults to 50.
            repetition_penalty (float, optional): Penalty for repetition of tokens. Defaults to 1.0.

        Returns:
            dict: The response from the API request.

        Raises:
            ValueError: If an invalid API is selected.

        Examples:
            >>> response = ChatAPIHandler.make_api_request(
            >>>     api="openai",
            >>>     model="gpt-3.5-turbo",
            >>>     temperature=0.7,
            >>>     max_tokens=150,
            >>>     top_p=0.9,
            >>>     conversation=[{"role": "user", "content": "Hello, how are you?"}],
            >>>     frequency_penalty=0.5,
            >>>     presence_penalty=0.6,
            >>>     stop_sequences=["\n"],
            >>>     top_k=40,
            >>>     repetition_penalty=1.2
            >>> )
        """
        if api == "openai":
            api_key = GPT3ChatCompletion.load_api_key()
            response = GPT3ChatCompletion.make_api_request(
                api_key=api_key,
                conversation=conversation,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                stop_sequences=stop_sequences,
                frequency_penalty=frequency_penalty,
                presence_penalty=presence_penalty,
                top_p=top_p,
            )
        elif api == "togetherai":
            api_key = TogetherAIChatCompletion.load_api_key()
            response = TogetherAIChatCompletion.make_api_request(
                conversation=conversation,
                api_key=api_key,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                top_k=top_k,
                repetition_penalty=repetition_penalty,
            )
        else:
            raise ValueError("Invalid API selection. Choose 'openai' or 'togetherai'.")
        return response

class ChatAPIHandler2:
    @staticmethod
    def make_api_request(args, conversation):
        if args.api == "openai":
            api_key = GPT3ChatCompletion.load_api_key()
            response = GPT3ChatCompletion.make_api_request(
                api_key=api_key,
                conversation=conversation,
                model=args.model,
                temperature=args.temperature,
                max_tokens=args.max_tokens,
                stop_sequences=args.stop_sequences,
                frequency_penalty=args.frequency_penalty,
                presence_penalty=args.presence_penalty,
                top_p=args.top_p,
            )
        elif args.api == "togetherai":
            api_key = TogetherAIChatCompletion.load_api_key()
            response = TogetherAIChatCompletion.make_api_request(
                conversation=conversation,
                api_key=api_key,
                model=args.model,
                temperature=args.temperature,
                max_tokens=args.max_tokens,
                top_p=args.top_p,
                top_k=args.top_k,
                repetition_penalty=args.repetition_penalty,
            )
        else:
            raise ValueError("Invalid API selection. Choose 'openai' or 'togetherai'.")
        return response
