import os

class DirectoryReader:
    @staticmethod
    def read_and_format_py_files(directory):
        """
        Reads the contents of all .py files in the given directory (including nested directories)
        and returns a neatly formatted string with each file's path and contents.

        :param directory: The directory to search for .py files.
        :return: A formatted string with paths and contents of all .py files.
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

# Usage Example (if you want to run it as a standalone script):
if __name__ == "__main__":
    directory = input("Enter the directory path: ")
    print(DirectoryReader.read_and_format_py_files(directory))
