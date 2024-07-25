import os
import json

class ContextManager:
    """
    A class for managing context stored in multiple JSON files within a local directory.

    This class provides static methods to retrieve context based on the file name or subdirectory name, and display context metadata.

    Steps:
    1. Use load_context_data() to load context data from the folder path containing JSON files.
    2. Use retrieve_context() method to get context for a specific context file or subdirectory.
    3. Use get_all_context_names() method to get a list of all existing context names with metadata.
    4. Use get_specific_context() to get the last n user/assistant exchanges along with the initial system message.
    """

    @staticmethod
    def load_context_data(context_folder):
        """
        Load context data from JSON files within a directory into memory.

        Args:
        - context_folder (str): Folder path containing JSON files.
        
        Returns:
        - dict: Dictionary containing aggregated context data from all JSON files.
        """
        context_data = {}
        for root, _, files in os.walk(context_folder):
            for file_name in files:
                if file_name.endswith(".json"):
                    file_path = os.path.join(root, file_name)
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        context_data.update(data)
        return context_data

    @staticmethod
    def retrieve_context(context_data, context_name):
        """
        Retrieve context metadata and content from a specific context name.

        Args:
        - context_data (dict): Dictionary containing context data loaded from JSON files.
        - context_name (str): Name of the context.

        Returns:
        - dict: Context data from the specified context name, or a message indicating no context found.
        """
        return context_data.get(context_name, f"Context '{context_name}' does not exist.")

    @staticmethod
    def get_all_context_names(context_data):
        """
        Get a list of all existing context names along with their metadata.

        Args:
        - context_data (dict): Dictionary containing context data loaded from JSON files.

        Returns:
        - list: List of strings containing all existing context names with metadata.
        """
        context_list = []
        for name, data in context_data.items():
            print(f"\033[91mName: {name}\033[0m")
            print(f"  \033[94mDescription: {data.get('description', 'None')}\033[0m")
            print(f"  \033[94mTags: {', '.join(data.get('tags', [])) or 'None'}\033[0m")
            print(f"  \033[94mID: {data.get('id', 'None')}\033[0m")
            context_list.append(name)
        return context_list

    @staticmethod
    def get_specific_context(context_data, context_name, n=10):
        """
        Retrieve the last n user/assistant exchanges along with the initial system message.

        Args:
        - context_data (dict): Dictionary containing context data loaded from JSON files.
        - context_name (str): Name of the context.
        - n (int): Number of user/assistant exchanges to retrieve.

        Returns:
        - list: List of dict containing the context messages.
        """
        context = context_data.get(context_name)
        if not context:
            return f"Context '{context_name}' does not exist."
        
        system_message = next((msg for msg in context['context'] if msg['role'] == 'system'), None)
        user_assistant_messages = [msg for msg in context['context'] if msg['role'] in ['user', 'assistant']]
        return [system_message] + user_assistant_messages[-n:]

# Usage example:
if __name__ == "__main__":
    # Example for multiple JSON files in a directory
    context_folder = 'context_prompts'
    context_data = ContextManager.load_context_data(context_folder)

    # Retrieve context from a specific context name
    context_name = 'banana'
    retrieved_context = ContextManager.retrieve_context(context_data, context_name)
    print(retrieved_context)  # Output: Full context data for 'banana'

    # Get all existing context names with metadata
    all_context_names = ContextManager.get_all_context_names(context_data)
    print(all_context_names)

    # Retrieve specific context
    specific_context = ContextManager.get_specific_context(context_data, 'apple', n=5)
    print(specific_context)
