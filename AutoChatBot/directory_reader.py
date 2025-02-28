import os
import argparse

class DirectoryReader:
    """
    Short Description:
    This class provides functionalities to read and format the contents of .py files within a specified directory,
    including subdirectories, and return them as a neatly formatted string.

    Methods:
    - read_and_format_py_files(directory: str) -> str:
        Reads the contents of all .py files in the given directory and returns a formatted string with each file's path and contents.
    """

    @staticmethod
    def read_and_format_py_files(directory: str) -> str:
        """
        Short Description:
        Reads the contents of all .py files in the given directory (including nested directories)
        and returns a neatly formatted string with each file's path and contents.

        Parameters:
        directory (str): The directory to search for .py files.
            Example: "/path/to/directory"

        Returns:
        str: A formatted string with paths and contents of all .py files.
            Example:
            "File: /path/to/directory/file1.py
            --------------------
            <content of file1.py>
            
            File: /path/to/directory/subdir/file2.py
            --------------------
            <content of file2.py>
            "

        How to Use:
        This method takes a directory path as input, searches for all .py files within that directory and its subdirectories,
        reads their contents, and returns a formatted string containing the path and contents of each .py file.

        Usage Example:
        >>> formatted_content = DirectoryReader.read_and_format_py_files("/path/to/directory")
        >>> print(formatted_content)
        """
        formatted_output = []
        
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        file_content = f.read()
                    
                    formatted_output.append(f"File: {file_path}\n{'-'*20}\n{file_content}\n")
        
        return ''.join(formatted_output)

def main():
    """
    Short Description:
    The main function to parse command line arguments and print the formatted contents of .py files in the specified directory.

    How to Use:
    This function uses argparse to parse the directory argument from the command line, then calls the DirectoryReader.read_and_format_py_files
    method to read and format the contents of .py files in the specified directory, and finally prints the formatted contents.

    Usage Example:
    Run the script from the command line as follows:
    $ python script_name.py --directory /path/to/directory
    """
    parser = argparse.ArgumentParser(description="Read and format .py files in a directory")
    parser.add_argument("--directory", help="The directory to search for .py files", required=True)
    args = parser.parse_args()

    directory = args.directory
    print(DirectoryReader.read_and_format_py_files(directory))

if __name__ == "__main__":
    main()