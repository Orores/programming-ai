import unittest
from unittest.mock import patch, MagicMock, Mock, call

import sys

from AutoChatBot.CodeErrorFormatter import CodeErrorFormatter

class TestCodeErrorFormatter(unittest.TestCase):

    def test_format_code_error(self):
        code = "print('Hello, World!')"
        error_output = "NameError: name 'print' is not defined"

        formatter = CodeErrorFormatter()
        formatted_string = formatter.format_code_error(code, error_output)

        expected_string = "code:\nprint('Hello, World!')\n\nerror:\nNameError: name 'print' is not defined"

        self.assertEqual(formatted_string, expected_string)

if __name__ == '__main__':
    unittest.main()
