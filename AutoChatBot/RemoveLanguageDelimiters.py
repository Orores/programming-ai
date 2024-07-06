import re

class CodeExtractor:
    """
    A class to extract code blocks from a string based on the specified language.
    If no language is specified, it attempts to infer the language and extract the code block.
    
    Static Methods:
    - extract_code(input_string, language=None): Extracts the code block for the specified language from the input string.
    
    Usage example:
        input_string = '''
        Here is some text.

        ```python
        print("Hello, World!")
        ```

        More text.
        '''
        extracted_code = CodeExtractor.extract_code(input_string)
        print(extracted_code)
    """
    
    @staticmethod
    def extract_code(input_string, language=None):
        """
        Extracts the code block for the specified language from the input string.
        If no language is specified, it attempts to infer the language and extract the code block.
        
        Args:
        - input_string (str): The input string containing the code block.
        - language (str, optional): The programming language of the code block to extract.
        
        Returns:
        - str: The extracted code block, or an empty string if no code block is found.
        """
        if language:
            pattern = rf'```{language}(.*?)```'
        else:
            pattern = r'```(\w+)?(.*?)```'
        
        match = re.search(pattern, input_string, re.DOTALL)
        if match:
            if language:
                return match.group(1).strip()
            else:
                # match.group(1) is the language (if present)
                # match.group(2) is the code block
                return match.group(2).strip()
        return ""

# Usage example:
if __name__ == "__main__":
    input_string = '''
    Here is some text.

    ```python
    print("Hello, World!")
    ```

    More text.
    '''
    extracted_code = CodeExtractor.extract_code(input_string)
    print(extracted_code)
    
    input_string_no_lang = '''
    Here is some text.

    ```
    console.log("Hello, World!");
    ```

    More text.
    '''
    extracted_code_no_lang = CodeExtractor.extract_code(input_string_no_lang)
    print(extracted_code_no_lang)
