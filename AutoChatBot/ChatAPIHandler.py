from .GPTChatCompletion import GPT3ChatCompletion
from .TogetherAIChatCompletion import TogetherAIChatCompletion

class ChatAPIHandler:
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
