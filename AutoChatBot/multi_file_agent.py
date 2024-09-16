import os
import json
from typing import List, Dict, Tuple
from AutoChatBot.ChatAPIHandler import ChatAPIHandler
from AutoChatBot.RemoveLanguageDelimiters import CodeExtractor
from AutoChatBot.ConversationPreparer import ConversationPreparer
from AutoChatBot.PyFileExecutor import PyFileExecutor

class MultiFileAgent:
    """
    MultiFileAgent: This class uses AutoChatBot to generate and update multiple files based on reference files and user-provided questions.
    
    Methods:
    - read_file_content(file_path: str) -> str:
        Reads the content of a file.
    - create_file_if_not_exists(file_path: str):
        Creates a file if it does not exist and ensures the directory structure.
    - construct_file_string(file_paths: List[str]) -> str:
        Constructs a string representation of files and their contents.
    - construct_task_string(question: str) -> str:
        Constructs the task string for the prompt.
    - construct_base_prompt(reference_files: List[str], rewrite_files: List[str], question: str) -> str:
        Constructs the base prompt string.
    - filter_python_code(response: str) -> str:
        Filters out Python code from a response.
    - filter_markdown_content(response: str) -> str:
        Filters out Markdown content from a response.
    - generate_file_content(base_prompt: str, file_path: str, is_new: bool) -> str:
        Generates content for a file using AutoChatBot.
    - execute_files(file_paths: List[str]) -> Dict[str, Tuple[str, str]]:
        Executes a list of files using PyFileExecutor and returns their stdout and stderr outputs.
    - execute(reference_files: List[str], rewrite_files: List[str], question: str = None, question_file_path: str = None, execute_files: List[str] = None, debug: bool = False) -> Tuple[Dict[str, str], Dict[str, Tuple[str, str]], str]:
        Orchestrates the multi-file generation, execution, and update process.
    """

    @staticmethod
    def read_file_content(file_path: str) -> str:
        """
        Reads the content of a file.
        
        Parameters:
        file_path (str): Path to the file to read.
        
        Returns:
        str: Content of the file.
        
        Raises:
        FileNotFoundError: If the specified file path does not exist.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        with open(file_path, 'r') as file:
            return file.read()

    @staticmethod
    def create_file_if_not_exists(file_path: str):
        """
        Creates a file if it does not exist and ensures the directory structure.
        
        Parameters:
        file_path (str): Path to the file to create.
        
        Returns:
        None
        
        Raises:
        OSError: If there is an issue creating the file or directory.
        """
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        if not os.path.exists(file_path):
            with open(file_path, 'w') as file:
                file.write("\n")

    @staticmethod
    def construct_file_string(file_paths: List[str]) -> str:
        """
        Constructs a string representation of files and their contents.
        
        Parameters:
        file_paths (List[str]): List of file paths.
        
        Returns:
        str: String representation of files and their contents.
        
        Raises:
        FileNotFoundError: If any of the specified file paths do not exist.
        """
        file_string = ""
        for file_path in file_paths:
            content = MultiFileAgent.read_file_content(file_path)
            file_string += f"{file_path}:\n{content}\n\n"
        return file_string

    @staticmethod
    def construct_task_string(question: str) -> str:
        """
        Constructs the task string for the prompt.
        
        Parameters:
        question (str): User-provided question.
        
        Returns:
        str: Task string for the prompt.
        """
        return f"TASK:\n\n{question}\n\n"

    @staticmethod
    def construct_base_prompt(reference_files: List[str], rewrite_files: List[str], question: str) -> str:
        """
        Constructs the base prompt string.
        
        Parameters:
        reference_files (List[str]): List of reference file paths.
        rewrite_files (List[str]): List of rewrite file paths.
        question (str): User-provided question.
        
        Returns:
        str: Base prompt string.
        """
        reference_files_string = MultiFileAgent.construct_file_string(reference_files)
        rewrite_files_string = MultiFileAgent.construct_file_string(rewrite_files)
        task_string = MultiFileAgent.construct_task_string(question)
        return reference_files_string + rewrite_files_string + task_string

    @staticmethod
    def filter_python_code(response: str) -> str:
        """
        Filters out Python code from a response.
        
        Parameters:
        response (str): The response string containing code.
        
        Returns:
        str: Filtered Python code.
        """
        return CodeExtractor.extract_code(response, language="python")

    @staticmethod
    def filter_markdown_content(response: str) -> str:
        """
        Filters out Markdown content from a response.
        
        Parameters:
        response (str): The response string containing Markdown content.
        
        Returns:
        str: Filtered Markdown content.
        """
        return CodeExtractor.extract_code(response, language="markdown")

    @staticmethod
    def generate_file_content(base_prompt: str, file_path: str, is_new: bool) -> str:
        """
        Generates content for a file using AutoChatBot.
        
        Parameters:
        base_prompt (str): The base prompt string.
        file_path (str): Path to the file to update.
        is_new (bool): Flag indicating if the file is new.
        
        Returns:
        str: Generated content for the file.
        
        Raises:
        ValueError: If the response format is invalid or does not contain the expected keys.
        """
        prompt = base_prompt + f"Now only show me the {'updated ' if not is_new else ''}{file_path}\n\n"
        response = ChatAPIHandler.make_api_request(
            api="openai",
            model="gpt-4o",
            temperature=0.7,
            max_tokens=4000,
            conversation=[{"role": "user", "content": prompt}],
        )
        content = response.get("choices", [{}])[0].get("message", {}).get("content", "")
        if file_path.endswith(".py"):
            content = MultiFileAgent.filter_python_code(content)
        elif file_path.endswith(".design"):
            content = MultiFileAgent.filter_markdown_content(content)
        return content

    @staticmethod
    def execute_files(file_paths: List[str]) -> Dict[str, Tuple[str, str]]:
        """
        Executes a list of files using PyFileExecutor and returns their stdout and stderr outputs.
        
        Parameters:
        file_paths (List[str]): List of file paths to be executed.
        
        Returns:
        Dict[str, Tuple[str, str]]: Dictionary with file paths as keys and tuples of (stdout, stderr) as values.
        
        Raises:
        FileNotFoundError: If any file to be executed does not exist.
        """
        result = {}
        for file_path in file_paths:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            stdout, stderr = PyFileExecutor.execute_code(file_path)
            result[file_path] = (stdout, stderr)
        return result

    @staticmethod
    def execute(reference_files: List[str], rewrite_files: List[str], question: str = None, question_file_path: str = None, execute_files: List[str] = None, debug: bool = False) -> Tuple[Dict[str, str], Dict[str, Tuple[str, str]], str]:
        """
        Orchestrates the multi-file generation, execution, and update process.
        
        Parameters:
        reference_files (List[str]): List of reference file paths.
        rewrite_files (List[str]): List of rewrite file paths.
        question (str, optional): The question to be included in the task string. Default is `None`.
        question_file_path (str, optional): The path to the file containing the question. Default is `None`.
        execute_files (List[str], optional): List of file paths to be executed. Default is `None`.
        debug (bool): Debug flag.
        
        Returns:
        Tuple[Dict[str, str], Dict[str, Tuple[str, str]], str]: Dictionary with file paths as keys and generated contents as values, dictionary with file paths as keys and tuples of (stdout, stderr) as values, and "Success" if all executed files have no errors, otherwise "Failure" along with the file that had the error.
        """
        # Step 1: Decide conversation from question or question_file_path
        question = ConversationPreparer.decide_conversation(file_path=question_file_path, question=question)
        
        # Step 2: Read reference files
        reference_files_string = MultiFileAgent.construct_file_string(reference_files)
        
        # Step 3: Create rewrite files if they do not exist
        for file_path in rewrite_files:
            MultiFileAgent.create_file_if_not_exists(file_path)
        
        # Step 4: Read rewrite files
        rewrite_files_string = MultiFileAgent.construct_file_string(rewrite_files)
        
        # Step 5: Construct task string
        task_string = MultiFileAgent.construct_task_string(question)
        
        # Step 6: Construct base prompt
        base_prompt = reference_files_string + rewrite_files_string + task_string
        
        # Step 7: Generate and update content for each rewrite file
        result = {}
        for file_path in rewrite_files:
            is_new = not os.path.getsize(file_path) > 1
            content = MultiFileAgent.generate_file_content(base_prompt, file_path, is_new)
            result[file_path] = content
            base_prompt += content + "\n\n"
        
        if debug:
            print(json.dumps(result, indent=4))
        
        # Step 8: Execute files and capture their outputs
        exec_outputs = {}
        status = "Success"
        if execute_files:
            exec_outputs = MultiFileAgent.execute_files(execute_files)
            for file_path, (stdout, stderr) in exec_outputs.items():
                if stderr:
                    status = f"Failure: {file_path} had an error."
                    break

        return result, exec_outputs, status

# Example usage:
if __name__ == "__main__":
    reference_files = ["reference_code/workout_tracker.design", "reference_code/test_workout_tracker.py"]
    rewrite_files = ["AutoChatBot/AutoChatBot.design", "AutoChatBot/AutoChatBot.py"]
    execute_files = ["AutoChatBot/AutoChatBot.py", "tests/test_AutoChatBot.py"]
    question_file_path = "path/to/question.txt"
    
    result, exec_outputs, status = MultiFileAgent.execute(reference_files, rewrite_files, question_file_path=question_file_path, execute_files=execute_files, debug=True)
    for file_path, content in result.items():
        with open(file_path, 'w') as file:
            file.write(content)
    print("Execution Outputs:", exec_outputs)
    print("Status:", status)