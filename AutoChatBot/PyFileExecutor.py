import os
import subprocess
from .RemoveLanguageDelimiters import CodeExtractor

class PyFileExecutor:
    """
    PyFileExecutor: This class takes a file path and a string, saves the string as a .py file, and executes it using a subprocess.

    Init parameters:
    - file_path (str): Path to the .py file.
    - code (str): String representing the Python code to be executed.

    Main methods:
    - save_code_to_file(): Saves the code as a .py file.
    - execute_code(): Executes the saved .py file using a subprocess.

    Example usage:
        executor = PyFileExecutor(file_path="script.py", code="print('Hello, World!')")
        error_output = executor.save_code_to_file()
        if error_output:
            print("Error Output:", error_output)
        else:
            executed_code, error_output = executor.execute_code()
            if error_output:
                print("Error Output:", error_output)
            else:
                print("Execution completed successfully.")
    """

    def __init__(self, file_path, code, language='python'):
        extracted_code = CodeExtractor.extract_code(code, language)
        self.code = extracted_code if extracted_code else code
        if file_path.startswith('/') or file_path.startswith('\\'):
            print("Warning: File path starts with a leading slash, which is unusual.")
        self.file_path = file_path

    @staticmethod
    def save_code_to_file(file_path, code):
        """
        Saves the provided code to the specified file path as a .py file.

        Parameters:
        - file_path (str): Path to the .py file.
        - code (str): Code to be saved to the file.

        Returns:
        - str: Error output if there is an error, None if there is no error.
        """
        try:
            # Create the directory if it does not exist
            directory, file_name = os.path.split(file_path)
            if directory:
                os.makedirs(directory, exist_ok=True)

            # Save the code as a .py file
            with open(file_path, 'w') as file:
                file.write(code)

            return None
        except Exception as e:
            return str(e)

    @staticmethod
    def execute_code(file_path):
        """
        Executes the .py file at the specified file path using a subprocess with the -m flag.

        Parameters:
        - file_path (str): Path to the .py file to be executed.

        Returns:
        - tuple: (executed_code_str, error_output) where executed_code_str is the code to be executed and error_output is the error output if there is an error, None if there is no error.
        """
        try:
            # Convert file path to module path using dot notation
            module_path = file_path.replace('/', '.').replace('\\', '.').rstrip('.py')

            # Prepare the command for executing the module using the -m flag
            command = ["python", "-m", module_path]

            # Execute the module using a subprocess
            process = subprocess.run(command, capture_output=True)

            # Check if there is any error output
            if process.stderr:
                return process.stderr.decode().strip()
            else:
                return None
        except Exception as e:
            return str(e)

# Usage example:
if __name__ == "__main__":
    input_string = '''
```python
print('Hello, World!')
```
    '''
    file_path = "sandbox_scripts/script.py"
    executor = PyFileExecutor(file_path=file_path, code=input_string, language='python')
    error_output = PyFileExecutor.save_code_to_file(executor.file_path, executor.code)
    if error_output:
        print("Error Output:", error_output)
    else:
        error_output = PyFileExecutor.execute_code(executor.file_path)
        if error_output:
            print("Executed Code:\n", executor.code)
            print("Error Output:", error_output)
        else:
            print("Executed Code:\n", executor.code)
            print("Execution completed successfully.")
