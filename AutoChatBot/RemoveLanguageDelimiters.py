import re

class CodeExtractor:
    """
    A class to extract code blocks from a string based on the specified language.
    
    Static Methods:
    - extract_code(input_string, language): Extracts the code block for the specified language from the input string.
    
    Usage example:
        input_string = '''
        Here is some text.

        ```python
        print("Hello, World!")
        ```

        More text.
        '''
        extracted_code = CodeExtractor.extract_code(input_string, 'python')
        print(extracted_code)
    """
    
    @staticmethod
    def extract_code(input_string, language):
        """
        Extracts the code block for the specified language from the input string.
        
        Args:
        - input_string (str): The input string containing the code block.
        - language (str): The programming language of the code block to extract.
        
        Returns:
        - str: The extracted code block, or an empty string if no code block is found.
        """
        pattern = rf'```{language}(.*?)```'
        match = re.search(pattern, input_string, re.DOTALL)
        if match:
            return match.group(1).strip()
        return ""

# Usage example:
if __name__ == "__main__":
    input_string = '''
Hello boys my name is gorden I a like pizza
```python
import curses
import argparse

# Function to display menu and handle user input
def main_menu(stdscr):
    # Clear screen
    stdscr.clear()
    stdscr.refresh()

    # Menu options
    menu = ['Option 1', 'Option 2', 'Option 3', 'Exit']
    current_row = 0

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        for idx, row in enumerate(menu):
            x = width // 2 - len(row) // 2
            y = height // 2 - len(menu) // 2 + idx
            if idx == current_row:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, row)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, row)

        stdscr.refresh()

        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            stdscr.clear()
            if current_row == len(menu) - 1:  # Exit option
                break
            stdscr.addstr(0, 0, f"You selected '{menu[current_row]}'")
            stdscr.refresh()
            stdscr.getch()  # Wait for another key press
            stdscr.clear()

def main():
    parser = argparse.ArgumentParser(description="CLI application using curses.")
    args = parser.parse_args()

    # Initialize curses application
    curses.wrapper(main_menu)

if __name__ == "__main__":
    main()
```
    '''
    extracted_code = CodeExtractor.extract_code(input_string, 'python')
    print(extracted_code)
