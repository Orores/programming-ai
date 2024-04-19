import json

class ConversationJsonReader:
    """
    ConversationJsonReader: This class reads JSON files containing conversations in a specific format and validates them.
    
    Init parameters:
    - file_path (str): Path to the JSON file to be read.
    
    Main methods:
    - read_file(file_path=None): Reads the JSON file and returns the conversation as a list of dictionaries.
    
    Example usage:
        reader = ConversationJsonReader(file_path="conversations.json")
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

    def __init__(self, file_path=None):
        self.file_path = file_path

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
                # Step 4: Validate the conversation format
                self._validate_conversation(content)
                # Step 5: Return the conversation
                return content
        except FileNotFoundError:
            # Step 6: Handle FileNotFoundError and raise an appropriate exception
            raise FileNotFoundError(f"File not found. Please check the path '{self.file_path}' and try again.")
    
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
            raise ValueError("Conversation JSON must contain a list of dictionaries.")
        
        # Step 3: Iterate through each item in the conversation
        for item in conversation:
            # Step 4: Check if each item is a dictionary and contains "role" and "content" keys
            if not isinstance(item, dict) or "role" not in item or "content" not in item:
                # Step 5: Raise ValueError if the format is incorrect
                raise ValueError("Conversation JSON must contain dictionaries with 'role' and 'content' keys.")

if __name__ == '__main__':
    # Step 1: Create an instance of ConversationJsonReader with a specified file_path
    reader = ConversationJsonReader(file_path="conversations.json")
    # Step 2: Read the file and get the conversations
    conversations = reader.read_file()
    # Step 3: Print the conversations
    print(conversations)

