import argparse
import json

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

    def read_file(self, file_path=None):
        try:
            with open(file_path, 'r') as file:
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


    @staticmethod
    def setup_args(parser):
        parser.add_argument("--file_path", type=str, default="question.tmp", help="Path to the file to be read. The format (text or JSON) will be automatically detected.")

def main():
    parser = argparse.ArgumentParser(description="Command Line Interface for Automatically Reading Text or JSON Files")
    FileReader.setup_args(parser)  # Setup argument for file path
    
    args = parser.parse_args()
    reader = FileReader(file_path=args.file_path)
    
    result = reader.read_file(args.file_path)
    content_type = result["type"]
    content = result["content"]
    
    if content_type == 'conversation':
        print("Conversations from JSON File:", content)
    else:
        print("Text File Content:", content)

if __name__ == '__main__':
    main()

