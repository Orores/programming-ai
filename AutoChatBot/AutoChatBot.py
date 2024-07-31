import argparse

from .ContextManager import ContextManager
from .ParserCreator import ParserCreator
from .GPTChatCompletionSaver import ChatCompletionSaver
from .TogetherAIModelRetriever import TogetherAIModelRetriever
from .ConversationPreparer import ConversationPreparer
from .ChatAPIHandler import ChatAPIHandler
from .CodeExecutor import CodeExecutor

class ChatBot:
    FAIL = '\33[91m'
    OKGREEN = '\33[92m'
    OKCYAN = '\33[96m'
    ORANGE = '\33[93m'
    BOLD = '\33[1m'

    @staticmethod
    def run():
        parser = ParserCreator.create_parser()
        args = parser.parse_args()
        if args.show_available_context:
            context_data = ContextManager.load_context_data(context_folder='context')
            context_names = ContextManager.get_all_context_names(context_data)
        if args.show_models:
            models = TogetherAIModelRetriever.get_available_models()
            print("Available Models for TogetherAI:\n")
            TogetherAIModelRetriever.print_models_table(models)

        if args.file_path or args.question:
            conversation = ConversationPreparer.decide_conversation(args)
            conversation = ConversationPreparer.str_to_dict_list(conversation)
            conversation = ConversationPreparer.extend_context(args, conversation)
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
            CodeExecutor.retry_api_request(args, response_content)
        if args.run_code_with_unittest:
            CodeExecutor.run_code_with_unittest(args, response_content)


def main():
    ChatBot.run()

if __name__ == '__main__':
    main()
