import os
import subprocess
from .RemoveLanguageDelimiters import CodeExtractor

class PyFileExecutor:
    """
    PyFileExecutor: This class takes a file path and a string, saves the string as a .py file, and executes it using a subprocess.

    Init parameters:
    - file_path (str): Path to the .py file.
    - code (str): String representing the Python code to be executed.

    Main method:
    - execute(): Saves the code as a .py file, executes it using a subprocess, and returns the executed code string and the error output or None if there is no error output.

    Example usage:
        executor = PyFileExecutor(file_path="script.py", code="print('Hello, World!')")
        executed_code, error_output = executor.execute()
        if error_output:
            print("Error Output:", error_output)
        else:
            print("Execution completed successfully.")
    """

    def __init__(self, file_path, code, language='python'):
        extracted_code = CodeExtractor.extract_code(code, language)
        self.code = extracted_code if extracted_code else code
        self.file_path = file_path

    def execute(self):
        """
        Saves the code as a .py file, executes it using a subprocess, and returns the executed code string and the error output or None if there is no error output.

        Returns:
        - tuple: (executed_code_str, error_output) where executed_code_str is the code to be executed and error_output is the error output if there is an error, None if there is no error.
        """
        try:
            # Step 1: Create the directory if it does not exist
            directory, file_name = os.path.split(self.file_path)
            if directory:
                os.makedirs(directory, exist_ok=True)

            # Step 2: Save the code as a .py file
            with open(self.file_path, 'w') as file:
                file.write(self.code)
            
            # Step 3: Prepare the command for executing the .py file
            command = ["python", self.file_path]

            # Step 4: Execute the .py file using a subprocess
            process = subprocess.run(command, capture_output=True)

            # Step 5: Check if there is any error output
            if process.stderr:
                return self.code, process.stderr.decode().strip()
            else:
                return self.code, None
        except Exception as e:
            return self.code, str(e)

# Usage example:
if __name__ == "__main__":
    input_string = '''
```python
print('Hello, World!')
```
    '''
    file_path = "sandbox_scripts/script.py"
    executor = PyFileExecutor(file_path=file_path, code=input_string, language='python')
    executed_code, error_output = executor.execute()
    if error_output:
        print("Executed Code:\n", executed_code)
        print("Error Output:", error_output)
    else:
        print("Executed Code:\n", executed_code)
        print("Execution completed successfully.")
