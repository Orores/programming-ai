class CodeErrorFormatter:
    """
    CodeErrorFormatter: This class formats code and error output into a string.

    Example usage:
    code = "print('Hello, World!')"
    error_output = "NameError: name 'print' is not defined"
    formatter = CodeErrorFormatter()
    formatted_string = formatter.format_code_error(code, error_output)
    print(formatted_string)

    Output:
    code:
    print('Hello, World!')

    error:
    NameError: name 'print' is not defined
    """

    def format_code_error(self, code, error_output):
        """
        Formats code and error output into a string.

        Args:
        - code (str): The code to be formatted.
        - error_output (str): The error output to be formatted.

        Returns:
        - str: The formatted string.
        """
        formatted_string = f"code:\n{code}\n\nerror:\n{error_output}"
        return formatted_string


# Usage example:
if __name__ == "__main__":
    code = "print('Hello, World!')"
    error_output = "NameError: name 'print' is not defined"
    formatter = CodeErrorFormatter()
    formatted_string = formatter.format_code_error(code, error_output)
    print(formatted_string)
