import argparse

class ParserCreator:
    @staticmethod
    def create_parser():
        parser = argparse.ArgumentParser(description="Command Line Interface for Chat Bot")
        parser.add_argument("--api", type=str, choices=["openai", "togetherai"], required=True, help="Select the API to use: 'openai' or 'togetherai'")
        parser.add_argument("--model", type=str, default="gpt-3.5-turbo", help="Model name for the completion request like gpt-3.5-turbo or cognitivecomputations/dolphin-2.5-mixtral-8x7b")
        parser.add_argument("--max_tokens", type=int, default=100, help="Maximum number of tokens to generate in the completion.")
        parser.add_argument("--temperature", type=float, default=1, help="Controls randomness: lower values make completions more deterministic.")
        parser.add_argument("--frequency_penalty", type=float, default=0, help="Penalty for frequent tokens, increasing this value produces more varied results.")
        parser.add_argument("--presence_penalty", type=float, default=0, help="Penalty for new tokens, increasing this value encourages new tokens in the completion.")
        parser.add_argument("--top_p", type=float, default=1, help="Nucleus sampling: top p of the probability mass is considered for sampling.")
        parser.add_argument("--top_k", type=int, default=50, help="Top-k sampling: The number of highest probability vocabulary tokens to keep for sampling.")
        parser.add_argument("--repetition_penalty", type=float, default=1, help="Penalty for repetition of tokens, values > 1 decrease repetition.")
        parser.add_argument("--stop_sequences", nargs='*', help="Sequences where the API should stop generating further tokens.")
        parser.add_argument("--question", type=str, help="The question or prompt to ask the model.")
        parser.add_argument("--file_path", type=str, help="Path to the file containing conversation or question.")
        parser.add_argument("--context", type=str, help="Context to use for the conversation.")
        parser.add_argument("--show_available_context", action='store_true', help="Show available contexts.")
        parser.add_argument("--show_models", action='store_true', help="Show available models for TogetherAI.")
        parser.add_argument("--save_path", type=str, default='response.tmp', help="Path to save the chat completion response.")
        parser.add_argument("--run_code", action='store_true', help="Run the generated code if any.")
        parser.add_argument("--run_code_with_unittest", action='store_true', help="Generate a unittest, then a code, then run the code against the unittest.")
        parser.add_argument("--code_save_path", type=str, default='sandbox_scripts/myscript.py', help="Path to save the generated code.")
        parser.add_argument("--multi_file_agent", action='store_true', help="Execute the multi-file agent.")
        parser.add_argument("--reference_files", nargs='*', help="List of reference file paths.")
        parser.add_argument("--rewrite_files", nargs='*', help="List of rewrite file paths.")
        parser.add_argument("--debug", action='store_true', help="Enable debug mode.")
        return parser

if __name__ == "__main__":
    parser = ParserCreator.create_parser()  # Use the static method to create the parser
    args = parser.parse_args()  # Parse arguments
    print("Arguments provided:")
    print(f"Model: {args.model}")
    print(f"Max tokens: {args.max_tokens}")
    print(f"Temperature: {args.temperature}")
    print(f"Frequency penalty: {args.frequency_penalty}")
    print(f"Presence penalty: {args.presence_penalty}")
    print(f"Top p: {args.top_p}")
    print(f"Top k: {args.top_k}")
    print(f"Repetition penalty: {args.repetition_penalty}")
    print(f"Stop sequences: {args.stop_sequences}")
    print(f"Question: {args.question}")
    print(f"File Path: {args.file_path}")
    print(f"Save Path: {args.save_path}")
    print(f"Context: {args.context}")
    print(f"Code Save Path: {args.code_save_path}")
    if args.run_code:
        print("Run code option is enabled.")
    else:
        print("Run code option is not enabled.")
        
    if args.show_available_context:
        print("Show available context option is enabled.")
    else:
        print("Show available context option is not enabled.")
        
    if args.multi_file_agent:
        print("Multi-file agent option is enabled.")
        print(f"Reference Files: {args.reference_files}")
        print(f"Rewrite Files: {args.rewrite_files}")
        print(f"Debug mode: {args.debug}")
    else:
        print("Multi-file agent option is not enabled.")