import unittest
from unittest.mock import patch, mock_open
from AutoChatBot.GetFunctionContextFromError import ErrorContextExtractor

class TestErrorContextExtractor(unittest.TestCase):

    def setUp(self):
        self.code_base_dir = "/mock/path/"
        self.error_string = """
        Traceback (most recent call last):
          File "/mock/path/module1.py", line 10, in <module>
            some_function()
          File "/mock/path/module2.py", line 20, in some_function
            another_function()
          File "/mock/path/module3.py", line 30, in another_function
            raise ValueError("An error occurred")
        ValueError: An error occurred
        """

    def test_parse_error_string(self):
        expected_output = [
            ("/mock/path/module1.py", 10),
            ("/mock/path/module2.py", 20),
            ("/mock/path/module3.py", 30)
        ]
        self.assertEqual(ErrorContextExtractor.parse_error_string(self.error_string), expected_output)

    @patch('builtins.open', new_callable=mock_open, read_data="\n\n\n\n\n\n\n\n\ndef some_function():\npass\n")
    @patch('os.path.isfile', return_value=True)
    def test_extract_function_source(self, mock_isfile, mock_open):
        file_path = "/mock/path/module1.py"
        line_number = 10
        expected_output = "def some_function():\npass"
        actual_output = ErrorContextExtractor.extract_function_source(file_path, line_number)
        self.assertEqual(actual_output, expected_output)

if __name__ == '__main__':
    unittest.main()
