import unittest
from AutoChatBot.response_processor import TextProcessor

class TestTextProcessor(unittest.TestCase):

    def test_basic_think_extraction(self):
        input_string = 'Hello! ❬think❭Should I mention the weather?❬/think❭'
        message, think = TextProcessor.filter_think(input_string)
        self.assertEqual(message, 'Hello!')
        self.assertEqual(think, 'Should I mention the weather?')

    def test_multiple_think_bubbles(self):
        input_string = '''First line
        ❬think❭Decision point A❬/think❭
        Middle text
        ❬think❭Decision point B❬/think❭
        Final line'''
        
        message, think = TextProcessor.filter_think(input_string)
        expected_message = '''First line
        
        Middle text
        
        Final line'''
        expected_think = 'Decision point A\nDecision point B'
        
        self.assertEqual(message.strip(), expected_message.strip())
        self.assertEqual(think, expected_think)

    def test_multiline_think_block(self):
        input_string = '''Start message
        ❬think❭Line one of thought
        Line two of thought
        Line three of thought❬/think❭
        End message'''
        
        message, think = TextProcessor.filter_think(input_string)
        expected_message = '''Start message
        
        End message'''
        expected_think = 'Line one of thought\nLine two of thought\nLine three of thought'
        
        self.assertEqual(message.strip(), expected_message.strip())
        self.assertEqual(think, expected_think)

    def test_missing_closing_tag(self):
        input_string = 'Text ❬think❭Unclosed thought'
        message, think = TextProcessor.filter_think(input_string)
        self.assertEqual(message, 'Text ❬think❭Unclosed thought')
        self.assertEqual(think, '')

    def test_empty_input(self):
        message, think = TextProcessor.filter_think('')
        self.assertEqual(message, '')
        self.assertEqual(think, '')

    def test_no_think_blocks(self):
        input_string = 'Simple message without any thoughts'
        message, think = TextProcessor.filter_think(input_string)
        self.assertEqual(message, input_string)
        self.assertEqual(think, '')

    def test_special_characters_preservation(self):
        input_string = 'Normal text ❬think❭!@#$%^&*()_+❬/think❭'
        message, think = TextProcessor.filter_think(input_string)
        self.assertEqual(message, 'Normal text')
        self.assertEqual(think, '!@#$%^&*()_+')

    def test_execute_method_removal(self):
        input_string = 'Hello ❬think❭hidden❬/think❭ world'
        result = TextProcessor.execute(input_string)
        self.assertEqual(result, 'Hello  world')

    def test_execute_method_no_removal(self):
        input_string = 'Hello ❬think❭hidden❬/think❭ world'
        result = TextProcessor.execute(input_string, remove_think=False)
        self.assertEqual(result, input_string)

    def test_large_multiline_think_block(self):
        input_string = '''hello
        ❬think❭This is a large multiline think block.
        It contains many lines of text.
        It should be entirely removed when processed.
        Leaving only the non-think block text.❬/think❭'''
        
        result = TextProcessor.execute(input_string)
        self.assertEqual(result.strip(), 'hello')

    def test_very_large_multiline_think_block(self):
        input_string =''' 
        <think>
        Okay, the user is working on a file called temp/hello.tmp. Previously, they asked to see the current content, which was "whatup". Now, they have a task to "say hello" and want to see the rewritten content of the same file.

        I need to confirm that the user wants the file updated to "hello" based on the task. They mentioned "rewritten temp/hello.tmp", which implies overwriting the previous content. Since there's no other instruction, replacing "whatup" with "hello" is the logical step.

        So the correct response is to display the new content as "hello" within the specified code block format.
        </think>

        hello
        '''
        
        result = TextProcessor.execute(input_string)
        self.assertEqual(result.strip(), 'hello')



if __name__ == '__main__':
    unittest.main()
