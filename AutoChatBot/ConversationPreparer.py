from .StringFileReader import StringFileReader
from .ConversationJsonReader import ConversationJsonReader
from .ParserCreator import ParserCreator
from .ContextManager import ContextManager

class ConversationPreparer:
    @staticmethod
    def decide_conversation(args):
        if args.file_path:
            try:
                conversation = ConversationJsonReader.read_file(args.file_path)
            except ValueError as e:
                conversation = StringFileReader.read_file(args.file_path)
        elif args.question:
            conversation = args.question
        else:
            parser = ParserCreator.create_parser()
            parser.error(ChatBot.FAIL + ChatBot.BOLD + 'Please enter the word you want the machine to say. Enter -h for help')
        return conversation

    @staticmethod
    def str_to_dict_list(conversation):
        if isinstance(conversation, str):
            conversation = [{"role": "user", "content": conversation}]
        return conversation

    @staticmethod
    def extend_context(args, conversation):
        if args.context is not None:
            context_data = ContextManager.load_context_data(context_folder='context')
            context = ContextManager.get_specific_context(context_data, args.context)
            if isinstance(context, list):  # Ensure context retrieval is successful
                context.extend(conversation)
                conversation = context
            else:
                print(context)  # Print error message if context does not exist
                exit()
        return conversation
