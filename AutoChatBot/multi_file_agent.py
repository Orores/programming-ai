import os
import json
from typing import List, Dict
from AutoChatBot.ChatAPIHandler import ChatAPIHandler
from AutoChatBot.ConversationPreparer import ConversationPreparer
from AutoChatBot.RemoveLanguageDelimiters import CodeExtractor

class MultiFileAgent:
    """
    MultiFileAgent: This class uses AutoChatBot to generate and update multiple files based on reference files and user-provided questions.
    
    Methods:
    - read_file_content(file_path: str) -> str:
        Reads the content of a file.
    - construct_conversation(reference_files: List[str], rewrite_files: List[str]) -> List[Dict[str, str]]:
        Constructs the conversation history based on reference and rewrite files.
    - construct_task_string(question: str) -> str:
        Constructs the task string for the prompt.
    - generate_file_content(conversation: List[Dict[str, str]], file_path: str, task: str) -> str:
        Generates content for a file using AutoChatBot.
    - execute(reference_files: List[str], rewrite_files: List[str], question: str = None, question_file_path: str = None, debug: bool = False) -> Dict[str, str]:
        Orchestrates the multi-file generation and update process.
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
    def construct_conversation(reference_files: List[str], rewrite_files: List[str]) -> List[Dict[str, str]]:
        """
        Constructs the conversation history based on reference and rewrite files.
        
        Parameters:
        reference_files (List[str]): List of reference file paths.
        rewrite_files (List[str]): List of rewrite file paths.
        
        Returns:
        List[Dict[str, str]]: The constructed conversation history.
        """
        conversation = []

        # Add reference files to the conversation
        for file_path in reference_files:
            user_message = {"role": "user", "content": f"The file {file_path} shall be used as a reference for similar files in the future. Now show me only the current {file_path} content:\n\n"}
            conversation.append(user_message)
            assistant_message = {"role": "assistant", "content": MultiFileAgent.read_file_content(file_path) + "\n\n"}
            conversation.append(assistant_message)

        # Separate rewrite files into existing and non-existing
        existing_files = [file_path for file_path in rewrite_files if os.path.exists(file_path)]
        non_existing_files = [file_path for file_path in rewrite_files if not os.path.exists(file_path)]

        # Add existing rewrite files to the conversation
        for file_path in existing_files:
            user_message = {"role": "user", "content": f"We will be working on {file_path} in the future. Now show me only the current {file_path} content:\n\n"}
            conversation.append(user_message)
            assistant_message = {"role": "assistant", "content": MultiFileAgent.read_file_content(file_path) + "\n\n"}
            conversation.append(assistant_message)

        # Add non-existing rewrite files to the conversation
        if non_existing_files:
            user_message = {"role": "user", "content": f"The following files will be created in the project: {', '.join(non_existing_files)}.\n\n"}
            conversation.append(user_message)

        return conversation

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
    def generate_file_content(conversation: List[Dict[str, str]], file_path: str, task: str) -> str:
        """
        Generates content for a file using AutoChatBot.
        
        Parameters:
        conversation (List[Dict[str, str]]): The conversation history.
        file_path (str): Path to the file to update.
        task (str): The task string.
        
        Returns:
        str: Generated content for the file.
        
        Raises:
        ValueError: If the response format is invalid or does not contain the expected keys.
        """
        task_modified = task + f"Now show me only the rewritten {file_path}:\n\n"
        conversation.append({"role": "user", "content": task_modified})
        
        response = ChatAPIHandler.make_api_request(
            api="openai",
            model="gpt-4o",
            temperature=0.7,
            max_tokens=4000,
            conversation=conversation,
        )
        content = response.get("choices", [{}])[0].get("message", {}).get("content", "")
        print('CONTENT')
        print(content)

        if file_path.endswith(".py"):
            content = MultiFileAgent.filter_python_code(content)
        elif file_path.endswith(".design"):
            pass
            #content = MultiFileAgent.filter_markdown_content(content)
        
        return content

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
    def execute(reference_files: List[str], rewrite_files: List[str], question: str = None, question_file_path: str = None, debug: bool = False) -> Dict[str, str]:
        """
        Orchestrates the multi-file generation and update process.
        
        Parameters:
        reference_files (List[str]): List of reference file paths.
        rewrite_files (List[str]): List of rewrite file paths.
        question (str, optional): The question to be included in the task string. Default is `None`.
        question_file_path (str, optional): The path to the file containing the question. Default is `None`.
        debug (bool): Debug flag.
        
        Returns:
        Dict[str, str]: Dictionary with file paths as keys and generated content as values.
        """
        # Step 1: Decide conversation from question or question_file_path
        question = ConversationPreparer.decide_conversation(file_path=question_file_path, question=question)

        # Step 2: Construct conversation history
        conversation = MultiFileAgent.construct_conversation(reference_files, rewrite_files)

        # Step 3: Construct task string
        task_string = MultiFileAgent.construct_task_string(question)

        # Step 4: Generate and update content for each rewrite file
        result = {}
        for file_path in rewrite_files:
            print(conversation)
            content = MultiFileAgent.generate_file_content(conversation, file_path, task_string)
            result[file_path] = content
            conversation.append({"role": "assistant", "content": content + "\n\n"})

        if debug:
            print(json.dumps(result, indent=4))

        return result

# Example usage:
if __name__ == "__main__":
    reference_files = ["reference_code/workout_tracker.design", "reference_code/test_workout_tracker.py"]
    rewrite_files = ["AutoChatBot/AutoChatBot.design", "AutoChatBot/AutoChatBot.py"]
    question_file_path = "path/to/question.txt"
    
    result = MultiFileAgent.execute(reference_files, rewrite_files, question_file_path=question_file_path, debug=True)
    for file_path, content in result.items():
        with open(file_path, 'w') as file:
            file.write(content)
    print("Generated Content:", result)
