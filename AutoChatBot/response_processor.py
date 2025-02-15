import re

class TextProcessor:
    """
    Processes text to separate/maintain message content and think bubbles.
    
    Static Methods:
    - filter_think(input_string): Separates text into message/think components
    - execute(input_string, remove_think=True): Public processing interface
    
    Usage:
        processed = TextProcessor.execute("Hello ❬think❭hidden❬/think❭ world")
    """
    
    @staticmethod
    def filter_think(input_string):
        """
        Splits text into message content and think bubble content.
        
        Args:
            input_string (str): Text containing ❬think❭ blocks
            
        Returns:
            tuple: (message_content, think_content) both as strings
        """
        if not input_string:
            return ('', '')
            
        think_pattern = re.compile(r'❬think❭(.*?)❬/think❭', re.DOTALL)
        think_blocks = think_pattern.findall(input_string)
        # Process each line within think blocks to strip whitespace
        think_content = '\n'.join(
            ['\n'.join(line.strip() for line in block.splitlines()) 
             for block in think_blocks]
        )
        message_content = think_pattern.sub('', input_string)
        return (message_content.strip(), think_content)

    @staticmethod
    def execute(input_string, remove_think=True):
        """
        Main processing method that optionally removes think content.
        
        Args:
            input_string (str): Text to process
            remove_think (bool): Whether to filter think bubbles
            
        Returns:
            str: Processed text according to removal flag
        """
        if not remove_think:
            return input_string
        message, think = TextProcessor.filter_think(input_string)
        return message

# Example usage
if __name__ == "__main__":
    sample_input = '''Hello! ❬think❭Planning response...❬/think❭
    How can I assist you today?'''
    
    print("With think removal:")
    print(TextProcessor.execute(sample_input))
    
    print("\nWithout think removal:")
    print(TextProcessor.execute(sample_input, remove_think=False))
