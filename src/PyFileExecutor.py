import os
import subprocess

class PyFileExecutor:
    """
    PyFileExecutor: This class takes a file path and a string, saves the string as a .py file, and executes it using a subprocess.

    Init parameters:
    - file_path (str): Path to the .py file.
    - code (str): String representing the Python code to be executed.

    Main method:
    - execute(): Saves the code as a .py file, executes it using a subprocess, and returns the error output or None if there is no error output.

    Example usage:
        executor = PyFileExecutor(file_path="script.py", code="print('Hello, World!')")
        error_output = executor.execute()
        if error_output:
            print("Error Output:", error_output)
        else:
            print("Execution completed successfully.")
    """

    def __init__(self, file_path, code):
        self.file_path = file_path
        self.code = code

    def execute(self):
        """
        Saves the code as a .py file, executes it using a subprocess, and returns the error output or None if there is no error output.

        Returns:
        - str or None: Error output if there is an error, None if there is no error.
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
            command = ["python"]
            if directory:
                command.extend([os.path.join(directory, file_name)])
            else:
                command.append(file_name)

            # Step 4: Execute the .py file using a subprocess
            process = subprocess.run(command, capture_output=True)

            # Step 5: Check if there is any error output
            if process.stderr:
                return process.stderr.decode().strip()
            else:
                return None
        except Exception as e:
            return str(e)

# Usage example:
if __name__ == "__main__":
    code = """
print('Hello, World!')
    """

    executor = PyFileExecutor(file_path="sandbox_scripts/script.py", code=code)
    error_output = executor.execute()
    if error_output:
        print("Error Output:", error_output)
    else:
        print("Execution completed successfully.")


