import argparse

from .ContextManager import ContextManager
from .ParserCreator import ParserCreator
from .GPTChatCompletionSaver import ChatCompletionSaver
from .TogetherAIModelRetriever import TogetherAIModelRetriever
from .ConversationPreparer import ConversationPreparer
from .ChatAPIHandler import ChatAPIHandler
from .CodeExecutor import CodeExecutor

class ChatBot:
    """
    The main ChatBot class to execute the chatbot functionalities.

    Constants
    ---------
    FAIL : str
        Red color escape code for error messages.
    OKGREEN : str
        Green color escape code for success messages.
    OKCYAN : str
        Cyan color escape code for informational messages.
    ORANGE : str
        Orange color escape code for warning messages.
    BOLD : str
        Escape code for bold text.

    Methods
    -------
    main():
        The main method to run the chatbot.
    """
    FAIL = '\33[91m'
    OKGREEN = '\33[92m'
    OKCYAN = '\33[96m'
    ORANGE = '\33[93m'
    BOLD = '\33[1m'

    @staticmethod
    def main():
        """
        The main method to run the chatbot. Parses arguments and executes the chatbot logic.
        """
        parser = ParserCreator.create_parser()
        args = parser.parse_args()
        
        if args.show_available_context:
            context_data = ContextManager.load_context_data(context_folder='context')
            context_names = ContextManager.get_all_context_names(context_data)
            print("Available contexts:", context_names)
        
        if args.show_models:
            models = TogetherAIModelRetriever.get_available_models()
            print("Available Models for TogetherAI:\n")
            TogetherAIModelRetriever.print_models_table(models)

        if args.file_path or args.question:
            conversation = ConversationPreparer.decide_conversation(file_path=args.file_path, question=args.question)
            conversation = ConversationPreparer.str_to_dict_list(conversation)
            conversation = ConversationPreparer.extend_context(context_name=args.context, conversation=conversation)
            response = ChatAPIHandler.make_api_request(
                api=args.api,
                model=args.model,
                temperature=args.temperature,
                max_tokens=args.max_tokens,
                top_p=args.top_p,
                conversation=conversation,
                frequency_penalty=args.frequency_penalty,
                presence_penalty=args.presence_penalty,
                stop_sequences=args.stop_sequences,
                top_k=args.top_k,
                repetition_penalty=args.repetition_penalty
            )
            print("Chat Completion Response:", response)
            ChatCompletionSaver.save_to_file(response, args.save_path)
            response_content = response['choices'][0]['message']['content']
        
        if args.run_code:
            CodeExecutor.retry_api_request(
                api=args.api,
                model=args.model,
                temperature=args.temperature,
                max_tokens=args.max_tokens,
                top_p=args.top_p,
                frequency_penalty=args.frequency_penalty,
                presence_penalty=args.presence_penalty,
                stop_sequences=args.stop_sequences,
                top_k=args.top_k,
                repetition_penalty=args.repetition_penalty,
                save_path=args.save_path,
                code_save_path=args.code_save_path,
                run_code=args.run_code,
                response_content=response_content
            )
            
        if args.run_code_with_unittest:
            CodeExecutor.run_code_with_unittest(
                api=args.api,
                model=args.model,
                temperature=args.temperature,
                max_tokens=args.max_tokens,
                top_p=args.top_p,
                frequency_penalty=args.frequency_penalty,
                presence_penalty=args.presence_penalty,
                stop_sequences=args.stop_sequences,
                top_k=args.top_k,
                repetition_penalty=args.repetition_penalty,
                save_path=args.save_path,
                code_save_path=args.code_save_path,
                run_code=args.run_code_with_unittest,
                response_content=response_content
            )


if __name__ == '__main__':
    ChatBot.main()
