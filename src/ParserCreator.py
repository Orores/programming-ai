import argparse

class ParserCreator:
    """
    Command Line Interface for GPT-3 Chat Completion
    """

    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Command Line Interface for GPT-3 Chat Completion")
        self.parser.add_argument("--model", type=str, default="gpt-3.5-turbo", help="Model name for the OpenAI completion request.")
        self.parser.add_argument("--max_tokens", type=int, default=100, help="Maximum number of tokens to generate in the completion.")
        self.parser.add_argument("--temperature", type=float, default=1, help="Controls randomness: lower values make completions more deterministic.")
        self.parser.add_argument("--frequency_penalty", type=float, default=0, help="Penalty for frequent tokens, increasing this value produces more varied results.")
        self.parser.add_argument("--presence_penalty", type=float, default=0, help="Penalty for new tokens, increasing this value encourages new tokens in the completion.")
        self.parser.add_argument("--top_p", type=float, default=1, help="Nucleus sampling: top p of the probability mass is considered for sampling.")
        self.parser.add_argument("--stop_sequences", nargs='*', help="Sequences where the API should stop generating further tokens.")
        self.parser.add_argument("--question", type=str, help="The question or prompt to ask the model.")
        self.parser.add_argument("--file_path", type=str, help="Path to the file.")
        self.parser.add_argument("--save_path", type=str, default="response.tmp", help="Path to save the response.")
        self.parser.add_argument("--context", type=str, help="File path for the context.")

if __name__ == "__main__":
    creator = ParserCreator()  # Create an instance of ParserCreator
    args = creator.parser.parse_args()  # Parse arguments
    print("Arguments provided:")
    print(f"Model: {args.model}")
    print(f"Max tokens: {args.max_tokens}")
    print(f"Temperature: {args.temperature}")
    print(f"Frequency penalty: {args.frequency_penalty}")
    print(f"Presence penalty: {args.presence_penalty}")
    print(f"Top p: {args.top_p}")
    print(f"Stop sequences: {args.stop_sequences}")
    print(f"Question: {args.question}")
    print(f"File Path: {args.file_path}")
    print(f"Save Path: {args.save_path}")
    print(f"Context: {args.context}")
