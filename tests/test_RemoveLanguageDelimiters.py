import unittest

import sys
sys.path.append('AutoChatBot')

from RemoveLanguageDelimiters import CodeExtractor

class TestCodeExtractor(unittest.TestCase):

    def test_extract_code_with_python(self):
        input_string = '''
        Here is some text.

        ```python
        print("Hello, World!")
        ```

        More text.
        '''
        expected_output = 'print("Hello, World!")'
        extracted_code = CodeExtractor.extract_code(input_string, 'python')
        self.assertEqual(extracted_code, expected_output)

    def test_extract_code_with_empty_string(self):
        input_string = ''
        expected_output = ''
        extracted_code = CodeExtractor.extract_code(input_string, 'python')
        self.assertEqual(extracted_code, expected_output)

    def test_extract_code_with_no_code_block(self):
        input_string = '''
        Here is some text.
        More text.
        '''
        expected_output = ''
        extracted_code = CodeExtractor.extract_code(input_string, 'python')
        self.assertEqual(extracted_code, expected_output)

    def test_extract_code_with_non_matching_language(self):
        input_string = '''
        Here is some text.

        ```javascript
        console.log("Hello, World!");
        ```

        More text.
        '''
        expected_output = ''
        extracted_code = CodeExtractor.extract_code(input_string, 'python')
        self.assertEqual(extracted_code, expected_output)

    def test_extract_code_with_multiple_code_blocks(self):
        input_string = '''
        Here is some text.

        ```python
        print("Hello, World!")
        ```

        More text.

        ```python
        print("Another code block")
        ```
        '''
        expected_output = 'print("Hello, World!")'
        extracted_code = CodeExtractor.extract_code(input_string, 'python')
        self.assertEqual(extracted_code, expected_output)

    def test_extract_code_with_multiline_code_block(self):
        input_string = '''
Here is some text.

```python
def hello_world():
    print("Hello, World!")
```

More text.
        '''
        expected_output = 'def hello_world():\n    print("Hello, World!")'
        extracted_code = CodeExtractor.extract_code(input_string, 'python')
        self.assertEqual(extracted_code, expected_output)

    def test_extract_code_with_special_characters(self):
        input_string = '''
        Here is some text.

        ```python
        print("Hello, World! #$%^&*()")
        ```

        More text.
        '''
        expected_output = 'print("Hello, World! #$%^&*()")'
        extracted_code = CodeExtractor.extract_code(input_string, 'python')
        self.assertEqual(extracted_code, expected_output)

if __name__ == '__main__':
    unittest.main()
