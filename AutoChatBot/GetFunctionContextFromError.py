import re
import os

class ErrorContextExtractor:
    """
    ErrorContextExtractor: This class handles the process of reading an error string, 
    parsing it to extract file paths and line numbers, and extracting the source code 
    for the involved functions.

    Methods:
    - parse_error_string(error_string): Parses the error string to extract file paths and line numbers.
    - extract_function_source(file_path, line_number): Extracts the function source code from the specified file and line number.
    - display_functions(functions): Displays the extracted functions.
    - process(error_string, code_base_dir): Main method to process the error string and display the function sources.
    """

    @staticmethod
    def parse_error_string(error_string):
        """
        Parses the error string to extract file paths and line numbers.
        
        Args:
        - error_string (str): The error string to parse.
        
        Returns:
        - list of tuples: A list of tuples containing file paths and line numbers.
        """
        pattern = re.compile(r'File "(.*?)", line (\d+)', re.MULTILINE)
        matches = pattern.findall(error_string)
        errors = [(match[0], int(match[1])) for match in matches]
        return errors

    @staticmethod
    def extract_function_source(file_path, line_number):
        """
        Extracts the function source code from the specified file and line number.
        
        Args:
        - file_path (str): The path to the file.
        - line_number (int): The line number where the error occurred.
        
        Returns:
        - str: The source code of the function containing the error.
        """
        if not os.path.isfile(file_path):
            return f"Cannot extract source code. File not found: {file_path}"
        
        with open(file_path, 'r') as file:
            source_code = file.read()
        
        lines = source_code.split('\n')
        start_line = end_line = line_number - 1
        
        # Find the start of the function
        while start_line > 0:
            if lines[start_line].strip().startswith('def '):
                break
            start_line -= 1
        
        # Find the end of the function
        while end_line < len(lines):
            if lines[end_line].strip() == '':
                break
            end_line += 1
        
        function_code = "\n".join(lines[start_line:end_line])
        return function_code

    @staticmethod
    def display_functions(functions):
        """
        Displays the extracted functions.
        
        Args:
        - functions (list of tuples): List containing tuples of file paths, line numbers, and function source codes.
        """
        for file_path, line_number, function_code in functions:
            print(f"File: {file_path}, Line: {line_number}")
            print("Function Source Code:")
            print(function_code)
            print("\n" + "="*50 + "\n")

    @staticmethod
    def process(error_string, code_base_dir):
        """
        Main method to process the error string and display the function sources.
        
        Args:
        - error_string (str): The error string to process.
        - code_base_dir (str): The base directory of the user's code.
        """
        parsed_errors = ErrorContextExtractor.parse_error_string(error_string)
        
        functions = []
        for file_path, line_number in parsed_errors:
            if file_path.startswith(code_base_dir):
                function_code = ErrorContextExtractor.extract_function_source(file_path, line_number)
                functions.append((file_path, line_number, function_code))
        
        ErrorContextExtractor.display_functions(functions)

if __name__ == "__main__":
    error_string = """
======================================================================
ERROR: test_format_code_error (__main__.TestCodeErrorFormatter)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/orores/programming-ai/tests/test_CodeErrorFormatter.py", line 15, in test_format
_code_error
    formatted_string = formatter.format_code_error(code, error_output)
  File "/home/orores/programming-ai/AutoChatBot/CodeErrorFormatter.py", line 32, in format_cod
e_error
    return formatted_string
NameError: name 'formatted_string' is not defined

----------------------------------------------------------------------
Ran 1 test in 0.000s

FAILED (errors=1)
    """
    ErrorContextExtractor.process(error_string, code_base_dir="/home/orores/programming-ai/")
