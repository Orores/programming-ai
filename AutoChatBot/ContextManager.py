import os
import json
from AutoChatBot.ConversationJsonReader import ConversationJsonReader
import pkg_resources

class ContextManager:
    """
    A class for managing context stored in multiple JSON files or a single JSON file.

    This class provides methods to retrieve context based on the file name or subdirectory name.

    Steps:
    1. Initialize the ContextManager with the folder path containing JSON files or single JSON file.
    2. Use retrieve_context() method to get context for a specific context file or subdirectory.
    3. Use get_all_context_names() method to get a list of all existing context names.
    """

    def __init__(self, context_folder='context_prompts', is_single_file=False, subdirectory_name=None):
        """
        Initialize the ContextManager with the folder path containing JSON files or single JSON file.

        Args:
        - context_folder (str): Folder path containing JSON files or path to the single JSON file.
        - is_single_file (bool): Indicates whether context is stored in a single JSON file.
        - subdirectory_name (str): Specifies the subdirectory when dealing with the single-file format.
        """
        self.context_folder = context_folder
        self.is_single_file = is_single_file
        self.subdirectory_name = subdirectory_name
        self.context_data = self.load_context_data()

    def load_context_data(self):
        """
        Load context data from JSON files into memory.

        Returns:
        - dict: Dictionary containing context data loaded from JSON files or a single JSON file.
        """
        context_data = {}
        if self.is_single_file:
            # Handling single JSON file scenario
            file_path = pkg_resources.resource_filename('AutoChatBot', self.context_folder)
            with open(file_path, 'r') as file:
                data = json.load(file)
                for topic, content in data.items():
                    if 'context' in content and isinstance(content['context'], list):
                        context_data[topic] = content['context']
                    else:
                        raise ValueError(f"Invalid structure for topic '{topic}' in single JSON file.")
        else:
            # Handling multiple JSON files scenario
            folder_path = pkg_resources.resource_filename('AutoChatBot', self.context_folder)
            for file_name in os.listdir(folder_path):
                if file_name.endswith(".json"):
                    file_path = os.path.join(folder_path, file_name)
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        context_data[file_name.replace('.json', '')] = data
        return context_data

    def retrieve_context(self, context_name):
        """
        Retrieve context from a specific context file or subdirectory.

        Args:
        - context_name (str): Name of the context file or subdirectory.

        Returns:
        - list of dict or str: Context data from the specified file or subdirectory, or a message indicating no context found.

        Notes:
        - If the specified context file or subdirectory does not exist, a message will be returned.
        """
        if context_name in self.context_data:
            return self.context_data[context_name]
        else:
            return f"Context '{context_name}' does not exist."

    def get_all_context_names(self):
        """
        Get a list of all existing context names.

        Returns:
        - list: List of strings containing all existing context names.
        """
        return list(self.context_data.keys())


# Usage example:
if __name__ == "__main__":
    # Example for multiple JSON files
    context_folder = 'context_prompts'
    manager = ContextManager(context_folder, is_single_file=False)

    # Retrieve context from a specific context file
    context_name = 'banana'
    retrieved_context = manager.retrieve_context(context_name)
    print(retrieved_context)  # Output: [{'role': 'system', 'content': 'You are a helpful assistant.'}]

    # Get all existing context names
    all_context_names = manager.get_all_context_names()
    print(all_context_names)

    # Example for single JSON file
    context_file = 'context_prompts/context.json'
    manager_single = ContextManager(context_folder=context_file, is_single_file=True, subdirectory_name='banana')

    # Retrieve context from a specific subdirectory
    retrieved_context_single = manager_single.retrieve_context('banana')
    print(retrieved_context_single)  # Output: [{'role': 'system', 'content': 'You are a helpful assistant.'}]

    # Get all existing subdirectory names
    all_context_names_single = manager_single.get_all_context_names()
    print(all_context_names_single)
