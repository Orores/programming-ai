from .StringFileReader import StringFileReader
from .ConversationJsonReader import ConversationJsonReader
from .ParserCreator import ParserCreator
from .ContextManager import ContextManager

class ConversationPreparer:
    """
    A utility class to prepare conversation data for the chatbot.

    Methods
    -------
    decide_conversation(file_path=None, question=None):
        Decides and retrieves the conversation data based on the provided file path or question.
        
    str_to_dict_list(conversation):
        Converts a string conversation into a list of dictionaries with role and content.
        
    extend_context(context_name, conversation):
        Extends the given conversation with additional context data if available.
    """

    @staticmethod
    def decide_conversation(file_path=None, question=None):
        """
        Decides and retrieves the conversation data based on the provided file path or question.

        Parameters
        ----------
        file_path : str, optional
            The path to the file containing the conversation data (default is None).
        
        question : str, optional
            The question to be used as conversation data (default is None).

        Returns
        -------
        conversation : str or list
            The retrieved conversation data.
        """
        if file_path:
            try:
                conversation = ConversationJsonReader.read_file(file_path)
            except ValueError as e:
                conversation = StringFileReader.read_file(file_path)
        elif question:
            conversation = question
        else:
            parser = ParserCreator.create_parser()
            parser.error(ChatBot.FAIL + ChatBot.BOLD + 'Please enter the word you want the machine to say. Enter -h for help')
        return conversation

    @staticmethod
    def str_to_dict_list(conversation):
        """
        Converts a string conversation into a list of dictionaries with role and content.

        Parameters
        ----------
        conversation : str or list
            The conversation data as a string or a list of dictionaries.

        Returns
        -------
        conversation : list
            The conversation data as a list of dictionaries.
        """
        if isinstance(conversation, str):
            conversation = [{"role": "user", "content": conversation}]
        return conversation

    @staticmethod
    def extend_context(context_name, conversation):
        """
        Extends the given conversation with additional context data if available.

        Parameters
        ----------
        context_name : str, optional
            The name of the context to be appended (default is None).
        
        conversation : list
            The conversation data as a list of dictionaries.

        Returns
        -------
        conversation : list
            The extended conversation data with additional context.
        """
        if context_name is not None:
            context_data = ContextManager.load_context_data(context_folder='context')
            context = ContextManager.get_specific_context(context_data, context_name)
            if isinstance(context, list):  # Ensure context retrieval is successful
                context.extend(conversation)
                conversation = context
            else:
                print(context)  # Print error message if context does not exist
                exit()
        return conversation
