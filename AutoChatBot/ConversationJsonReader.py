import json

class ConversationJsonReader:
    """
    ConversationJsonReader: This class reads JSON files containing conversations in a specific format and validates them.
    
    Init parameters:
    - file_path (str): Path to the JSON file to be read.
    - is_single_file (bool): Indicates if the JSON file contains all conversations or individual files for each subdirectory.
    - subdirectory_name (str): Specifies the subdirectory when dealing with the single-file format.
    
    Main methods:
    - read_file(file_path=None): Reads the JSON file and returns the conversation as a list of dictionaries.
    
    Example usage:
        reader = ConversationJsonReader(file_path="conversations.json", is_single_file=True, subdirectory_name="subdirectory_name")
        conversations = reader.read_file()
        print(conversations)
        
    Input:
    - file_path (str, optional): Path to the JSON file to be read. If not provided, the file path specified during class initialization is used.
    
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

    def __init__(self, file_path=None, is_single_file=False, subdirectory_name=None):
        self.file_path = file_path
        self.is_single_file = is_single_file
        self.subdirectory_name = subdirectory_name

    def read_file(self, file_path=None):
        """
        Reads the JSON file and returns the conversation as a list of dictionaries.
        
        Args:
        - file_path (str, optional): Path to the JSON file to be read. If not provided, the file path specified during class initialization is used.
        
        Returns:
        - conversations (list of dicts): List containing dictionaries representing the conversation. Each dictionary should have "role" and "content" keys.
        
        Raises:
        - FileNotFoundError: If the specified file path does not exist.
        - ValueError: If the JSON file does not adhere to the expected conversation format.
        """
        try:
            # Step 1: Check if a file_path is provided, if yes, update self.file_path
            if file_path:
                self.file_path = file_path
            
            # Step 2: Open the JSON file in read mode
            with open(self.file_path, 'r') as file:
                # Step 3: Load the JSON content from the file
                content = json.load(file)
                
                if self.is_single_file:
                    # Validate single file format
                    self._validate_single_file_format(content)
                    # Extract the context for the specified subdirectory
                    if self.subdirectory_name in content:
                        context = content[self.subdirectory_name].get('context', [])
                        # Validate the extracted context
                        self._validate_conversation(context)
                        return context
                    else:
                        raise ValueError(f"Subdirectory '{self.subdirectory_name}' not found in the JSON file.")
                else:
                    # Validate individual file format
                    self._validate_conversation(content)
                    return content
        except FileNotFoundError:
            # Step 6: Handle FileNotFoundError and raise an appropriate exception
            raise FileNotFoundError(f"File not found. Please check the path '{self.file_path}' and try again.")
    
    def _validate_single_file_format(self, content):
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

    def _validate_conversation(self, conversation):
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
            raise ValueError(f"Conversation JSON must contain a list of dictionaries.\n Conversation:\n {conversation}")
        
        # Step 3: Iterate through each item in the conversation
        for item in conversation:
            # Step 4: Check if each item is a dictionary and contains "role" and "content" keys
            if not isinstance(item, dict) or ("role" not in item and "content" not in item):
                # Step 5: Raise ValueError if the format is incorrect
                raise ValueError(f"Conversation JSON must contain dictionaries with 'role' and 'content' keys.\n Conversation:\n {item}")

if __name__ == '__main__':
    # Example usage for single file format
    reader_single = ConversationJsonReader(file_path="AutoChatBot/context_prompts/context.json", is_single_file=True, subdirectory_name="banana")
    conversations_single = reader_single.read_file()
    print(conversations_single)

    # Example usage for individual file format
    reader_individual = ConversationJsonReader(file_path="AutoChatBot/context_prompts/banana.json")
    conversations_individual = reader_individual.read_file()
    print(conversations_individual)
