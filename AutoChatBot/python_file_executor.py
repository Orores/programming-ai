import subprocess
import os
from typing import List, Tuple, Dict

class PythonFileExecutor:
    """
    PythonFileExecutor: This class is designed to execute Python files and capture their standard output (stdout) and standard error (stderr).

    Methods:
    - execute_code(file_path: str) -> Tuple[str, str]:
        Executes a Python file and captures its stdout and stderr.
    - execute(file_paths: List[str]) -> Dict[str, Tuple[str, str]]:
        Orchestrates the execution of multiple Python files and returns their outputs.
    """

    @staticmethod
    def execute_code(file_path: str) -> Tuple[str, str]:
        """
        Executes a Python file and captures its stdout and stderr.
        
        Parameters:
        file_path (str): Path to the Python file to be executed.
        
        Returns:
        Tuple[str, str]: A tuple containing stdout and stderr as strings.
        
        Raises:
        FileNotFoundError: If the specified file path does not exist.
        ExecutionError: If there is an error during file execution.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        try:
            # Convert file path to module path using dot notation
            module_path = file_path.replace('/', '.').replace('\\', '.').rstrip('.py')
            # Prepare the command for executing the module using the -m flag
            command = ["python", "-m", module_path]

            # Execute the module using a subprocess
            process = subprocess.run(command, capture_output=True)


            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout, result.stderr
        except subprocess.CalledProcessError as e:
            return e.stdout, e.stderr

    @staticmethod
    def execute(file_paths: List[str]) -> Dict[str, Tuple[str, str]]:
        """
        Orchestrates the execution of multiple Python files and returns their outputs.
        
        Parameters:
        file_paths (List[str]): List of paths to Python files to be executed.
        
        Returns:
        Dict[str, Tuple[str, str]]: Dictionary with file paths as keys and tuples of (stdout, stderr) as values.
        """
        results = {}
        for file_path in file_paths:
            stdout, stderr = PythonFileExecutor.execute_code(file_path)
            results[file_path] = (stdout, stderr)
        return results

# Example usage:
if __name__ == "__main__":
    file_paths = ["path/to/python_file1.py", "path/to/python_file2.py"]
    exec_outputs = PythonFileExecutor.execute(file_paths)
    for file_path, (stdout, stderr) in exec_outputs.items():
        print(f"Output for {file_path}:\nSTDOUT:\n{stdout}\nSTDERR:\n{stderr}")
