import os
import subprocess
from .RemoveLanguageDelimiters import CodeExtractor

class PyFileExecutor:
    """
    PyFileExecutor: This class provides static methods to save a string as a .py file and execute it using a subprocess.

    Example usage:
        error_output = PyFileExecutor.save_code_to_file(file_path="script.py", code="print('Hello, World!')")
        if error_output:
            print("Error Output:", error_output)
        else:
            executed_code, error_output = PyFileExecutor.execute_code(file_path="script.py")
            if error_output:
                print("Error Output:", error_output)
            else:
                print("Execution completed successfully.")
    """

    @staticmethod
    def save_code_to_file(file_path, code, language='python'):
        """
        Saves the provided code to the specified file path as a .py file after extracting the code.

        Parameters:
        - file_path (str): Path to the .py file.
        - code (str): Code to be saved to the file.
        - language (str): Language of the code to be extracted.

        Returns:
        - str: Error output if there is an error, None if there is no error.
        """
        try:
            extracted_code = CodeExtractor.extract_code(code, language)
            code_to_save = extracted_code if extracted_code else code

            # Create the directory if it does not exist
            directory, file_name = os.path.split(file_path)
            if directory:
                os.makedirs(directory, exist_ok=True)

            # Save the code as a .py file
            with open(file_path, 'w') as file:
                file.write(code_to_save)
                print('Code written to: ',file_path)

            return None
        except Exception as e:
            return str(e)

    @staticmethod
    def is_error(output):
        """
        Checks if the given output string indicates an error.

        Parameters:
        - output (str): The output string to be checked.

        Returns:
        - bool: True if there is an error, False otherwise.
        """
        if output.strip().endswith("OK") or output.strip() == "":
            return False
        else:
            return True

    @staticmethod
    def execute_code(file_path):
        """
        Executes the .py file at the specified file path using a subprocess with the -m flag.

        Parameters:
        - file_path (str): Path to the .py file to be executed.

        Returns:
        - str: Error output if there is an error, None if there is no error.
        """
        try:
            # Convert file path to module path using dot notation
            module_path = file_path.replace('/', '.').replace('\\', '.').rstrip('.py')

            # Prepare the command for executing the module using the -m flag
            command = ["python", "-m", module_path]

            # Execute the module using a subprocess
            process = subprocess.run(command, capture_output=True)

            # Check if there is any error output
            stderr_output = process.stderr.decode().strip()
            if stderr_output and PyFileExecutor.is_error(stderr_output):
                return stderr_output
            else:
                return None
        except Exception as e:
            return str(e)



def main():
    input_string = '''
```python
print('Hello, World!')
```
    '''
    file_path = "sandbox_scripts/script.py"
    error_output = PyFileExecutor.save_code_to_file(file_path=file_path, code=input_string, language='python')
    if error_output:
        print("Error Output:", error_output)
    else:
        error_output = PyFileExecutor.execute_code(file_path)
        if error_output:
            print("Executed Code:\n", input_string)
            print("Error Output:", error_output)
        else:
            print("Executed Code:\n", input_string)
            print("Execution completed successfully.")

def main_light():
    error = PyFileExecutor.execute_code('tests/test_myscript.py')
    print('ERROR: ')
    print(error)

# Usage example:
if __name__ == "__main__":
    main_light()
