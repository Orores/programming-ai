class StringFileReader:
    """
    StringFileReader: This class reads text files and returns their contents as strings.
    
    Init parameters:
    - file_path (str): Path to the text file to be read.
    
    Main methods:
    - read_file(file_path=None): Reads the text file and returns its content as a string.
    
    Example usage:
        reader = StringFileReader(file_path="sample.txt")
        content = reader.read_file()
        print(content)
        
    Input:
    - file_path (str, optional): Path to the text file to be read. If not provided, the file path specified during class initialization is used.
    
    Output:
    - content (str): Content of the text file as a string.
    
    Raises:
    - FileNotFoundError: If the specified file path does not exist.
    - TypeError: If the content read from the file is not a string.
    """

    def __init__(self, file_path=None):
        self.file_path = file_path

    def read_file(self, file_path=None):
        """
        Reads the text file and returns its content as a string.
        
        Args:
        - file_path (str, optional): Path to the text file to be read. If not provided, the file path specified during class initialization is used.
        
        Returns:
        - content (str): Content of the text file as a string.
        
        Raises:
        - FileNotFoundError: If the specified file path does not exist.
        - TypeError: If the content read from the file is not a string.
        """
        try:
            # Update file_path if provided
            if file_path:
                self.file_path = file_path
            
            # Open the file and read its content as string
            with open(self.file_path, 'r') as file:
                content = file.read()
                
                # Check if the content is a string
                if not isinstance(content, str):
                    raise TypeError("The content read from the file is not a string.")
                
                return content
        except FileNotFoundError:
            # Handle FileNotFoundError
            raise FileNotFoundError(f"File not found. Please check the path '{self.file_path}' and try again.")

