import json

class ConversationJsonReader:
    """
    ConversationJsonReader: This class reads JSON files containing conversations in a specific format and validates them.
    
    Main methods:
    - read_file(file_path, is_single_file=False, subdirectory_name=None): Reads the JSON file and returns the conversation as a list of dictionaries.
    
    Example usage:
        conversations_single = ConversationJsonReader.read_file(file_path="conversations.json", is_single_file=True, subdirectory_name="subdirectory_name")
        print(conversations_single)
        
    Input:
    - file_path (str): Path to the JSON file to be read.
    - is_single_file (bool, optional): Indicates if the JSON file contains all conversations or individual files for each subdirectory.
    - subdirectory_name (str, optional): Specifies the subdirectory when dealing with the single-file format.
    
    Output:
    - conversations (list of dicts): List containing dictionaries representing the conversation. Each dictionary should have "role" and "content" keys.
    
    Raises:
    - FileNotFoundError: If the specified file path does not exist.
    - ValueError: If the JSON file does not adhere to the expected conversation format.
    
    Example JSON format:
    [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, how are you?"}
    ]
    """

    @staticmethod
    def read_file(file_path, is_single_file=False, subdirectory_name=None):
        """
        Reads the JSON file and returns the conversation as a list of dictionaries.
        
        Args:
        - file_path (str): Path to the JSON file to be read.
        - is_single_file (bool, optional): Indicates if the JSON file contains all conversations or individual files for each subdirectory.
        - subdirectory_name (str, optional): Specifies the subdirectory when dealing with the single-file format.
        
        Returns:
        - conversations (list of dicts): List containing dictionaries representing the conversation. Each dictionary should have "role" and "content" keys.
        
        Raises:
        - FileNotFoundError: If the specified file path does not exist.
        - ValueError: If the JSON file does not adhere to the expected conversation format.
        """
        try:
            # Step 1: Open the JSON file in read mode
            with open(file_path, 'r') as file:
                # Step 2: Load the JSON content from the file
                content = json.load(file)
                
                if is_single_file:
                    # Validate single file format
                    ConversationJsonReader._validate_single_file_format(content)
                    # Extract the context for the specified subdirectory
                    if subdirectory_name in content:
                        context = content[subdirectory_name].get('context', [])
                        # Validate the extracted context
                        ConversationJsonReader._validate_conversation(context)
                        return context
                    else:
                        raise ValueError(f"Subdirectory '{subdirectory_name}' not found in the JSON file.")
                else:
                    # Validate individual file format
                    ConversationJsonReader._validate_conversation(content)
                    return content
        except FileNotFoundError:
            # Step 6: Handle FileNotFoundError and raise an appropriate exception
            raise FileNotFoundError(f"File not found. Please check the path '{file_path}' and try again.")
    
    @staticmethod
    def _validate_single_file_format(content):
        """
        Validates the single file JSON format.
        
        Args:
        - content (dict): The JSON content of the file.
        
        Raises:
        - ValueError: If the JSON file does not adhere to the expected single file conversation format.
        """
        if not isinstance(content, dict):
            raise ValueError("Single file JSON must contain a dictionary with subdirectory names as keys.")
        
        for subdirectory, details in content.items():
            if not isinstance(details, dict) or 'context' not in details:
                raise ValueError(f"Each subdirectory must contain a dictionary with a 'context' key. Error in subdirectory '{subdirectory}'.")

    @staticmethod
    def _validate_conversation(conversation):
        """
        Validates the conversation JSON format.
        
        Args:
        - conversation (list of dicts): List containing dictionaries representing the conversation.
        
        Raises:
        - ValueError: If the JSON file does not adhere to the expected conversation format.
        """
        # Step 1: Check if the conversation is a list
        if not isinstance(conversation, list):
            # Step 2: Raise ValueError if the conversation is not a list
            raise ValueError(f"Conversation JSON must contain a list of dictionaries. Conversation:\n {conversation}")
        
        # Step 3: Iterate through each item in the conversation
        for item in conversation:
            # Step 4: Check if each item is a dictionary and contains "role" and "content" keys
            if not isinstance(item, dict) or "role" not in item or "content" not in item:
                # Step 5: Raise ValueError if the format is incorrect
                raise ValueError(f"Conversation JSON must contain dictionaries with 'role' and 'content' keys. Conversation:\n {item}")

if __name__ == '__main__':
    # Example usage for single file format
    conversations_single = ConversationJsonReader.read_file(file_path="AutoChatBot/context_prompts/context.json", is_single_file=True, subdirectory_name="banana")
    print(conversations_single)

    # Example usage for individual file format
    conversations_individual = ConversationJsonReader.read_file(file_path="AutoChatBot/context_prompts/banana.json")
    print(conversations_individual)
