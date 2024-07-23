import os
import json
import pkg_resources

class ContextManager:
    """
    A class for managing context stored in multiple JSON files or a single JSON file.

    This class provides static methods to retrieve context based on the file name or subdirectory name.

    Steps:
    1. Use load_context_data() to load context data from the folder path containing JSON files or a single JSON file.
    2. Use retrieve_context() method to get context for a specific context file or subdirectory.
    3. Use get_all_context_names() method to get a list of all existing context names.
    """

    @staticmethod
    def load_context_data(context_folder='context_prompts', is_single_file=False):
        """
        Load context data from JSON files into memory.

        Args:
        - context_folder (str): Folder path containing JSON files or path to the single JSON file.
        - is_single_file (bool): Indicates whether context is stored in a single JSON file.
        
        Returns:
        - dict: Dictionary containing context data loaded from JSON files or a single JSON file.
        """
        context_data = {}
        if is_single_file:
            # Handling single JSON file scenario
            file_path = pkg_resources.resource_filename('AutoChatBot', context_folder)
            with open(file_path, 'r') as file:
                data = json.load(file)
                for topic, content in data.items():
                    if 'context' in content and isinstance(content['context'], list):
                        context_data[topic] = content['context']
                    else:
                        raise ValueError(f"Invalid structure for topic '{topic}' in single JSON file.")
        else:
            # Handling multiple JSON files scenario
            folder_path = pkg_resources.resource_filename('AutoChatBot', context_folder)
            for file_name in os.listdir(folder_path):
                if file_name.endswith(".json"):
                    file_path = os.path.join(folder_path, file_name)
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        context_data[file_name.replace('.json', '')] = data
        return context_data

    @staticmethod
    def retrieve_context(context_data, context_name):
        """
        Retrieve context from a specific context file or subdirectory.

        Args:
        - context_data (dict): Dictionary containing context data loaded from JSON files or a single JSON file.
        - context_name (str): Name of the context file or subdirectory.

        Returns:
        - list of dict or str: Context data from the specified file or subdirectory, or a message indicating no context found.

        Notes:
        - If the specified context file or subdirectory does not exist, a message will be returned.
        """
        if context_name in context_data:
            return context_data[context_name]
        else:
            return f"Context '{context_name}' does not exist."

    @staticmethod
    def get_all_context_names(context_data):
        """
        Get a list of all existing context names.

        Args:
        - context_data (dict): Dictionary containing context data loaded from JSON files or a single JSON file.

        Returns:
        - list: List of strings containing all existing context names.
        """
        return list(context_data.keys())


# Usage example:
if __name__ == "__main__":
    # Example for multiple JSON files
    context_folder = 'context_prompts'
    context_data = ContextManager.load_context_data(context_folder, is_single_file=False)

    # Retrieve context from a specific context file
    context_name = 'banana'
    retrieved_context = ContextManager.retrieve_context(context_data, context_name)
    print(retrieved_context)  # Output: [{'role': 'system', 'content': 'You are a helpful assistant.'}]

    # Get all existing context names
    all_context_names = ContextManager.get_all_context_names(context_data)
    print(all_context_names)

    # Example for single JSON file
    context_file = 'context_prompts/context.json'
    context_data_single = ContextManager.load_context_data(context_folder=context_file, is_single_file=True)

    # Retrieve context from a specific subdirectory
    retrieved_context_single = ContextManager.retrieve_context(context_data_single, 'banana')
    print(retrieved_context_single)  # Output: [{'role': 'system', 'content': 'You are a helpful assistant.'}]

    # Get all existing subdirectory names
    all_context_names_single = ContextManager.get_all_context_names(context_data_single)
    print(all_context_names_single)
