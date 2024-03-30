import json
import argparse

class FileReader:
    """
    FileReader: This class is designed to automatically detect and read files, handling both plain text and JSON formatted files containing conversations.
    
    Init parameters:
    - file_path (str): Path to the file to be read. The class automatically determines the file's format and processes it accordingly.
    
    Main methods:
    - read_file(): Detects the file format and reads its content. For text files, it returns the string content. For JSON files, it reconstructs and returns the dictionary or list of dictionaries.
    
    Example usage:
        reader = FileReader(file_path="sample.txt")
        content = reader.read_file()
        print(content)
        
        reader = FileReader(file_path="conversations.json")
        conversations = reader.read_file()
        print(conversations)
        
    This method simplifies the interface by requiring only the path to the file, automatically handling the distinction between text and JSON formats.
    """

    def __init__(self, file_path=None):
        self.file_path = file_path

    def update_attributes(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{key}'")

    def read_file(self, file_path=None):
        try:
            if file_path:
                self.file_path = file_path
            with open(self.file_path, 'r') as file:
                try:
                    # Attempt to parse as JSON
                    content = json.load(file)
                    # Check if it's a list of dictionaries representing a conversation
                    if isinstance(content, list) and all(isinstance(item, dict) and 'role' in item and 'content' in item for item in content):
                        return {"type": "conversation", "content": content}
                    else:
                        return {"type": "string", "content": content}
                except json.JSONDecodeError:
                    # Handle as plain text
                    file.seek(0)  # Reset file pointer to the beginning
                    content = file.read()
                    return {"type": "string", "content": content}
        except FileNotFoundError:
            # Raise an error with a custom message
            raise FileNotFoundError(f"File not found. Please check the path '{self.file_path}' and try again.")
        except TypeError:
            # Raise an error with a custom message
            raise TypeError(f"None was passed as a file path, which is not valid")


    def setup_args(self, parser):
        parser.add_argument("--file_path", type=str, help="Path to the file to be read. The format (text or JSON) will be automatically detected.")

if __name__ == '__main__':
    reader = FileReader()
    parser = argparse.ArgumentParser(description="Command Line Interface for Automatically Reading Text or JSON Files")
    reader.setup_args(parser)  # Setup argument for file path
    
    args = parser.parse_args()
    reader.update_attributes(file_path=args.file_path)
    
    result = reader.read_file()
    content_type = result["type"]
    content = result["content"]
    
    if content_type == 'conversation':
        print("Conversations from JSON File:", content)
    else:
        print("Text File Content:", content)

