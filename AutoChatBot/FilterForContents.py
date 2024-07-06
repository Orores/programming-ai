import re

class CodeParser:
    def __init__(self, text):
        self.text = text
        self.parsed_data = self._parse_text()

    def _parse_text(self):
        """
        Parse text into a dictionary based on the +++section+++ and ---section--- format.
        """
        pattern = re.compile(r'\+\+\+([^\+]+)\+\+\+(.+?)---\1---', re.DOTALL)
        matches = pattern.findall(self.text)
        parsed_dict = {section.strip(): content.strip() for section, content in matches}
        return parsed_dict

    def get_parsed_data(self):
        """
        Return the parsed data as a dictionary.
        """
        return self.parsed_data

if __name__ == "__main__":
    example_text = '''
    +++python code+++
    bla bla
    ---python code---
    +++unittest+++
    blu blub
    ---unittest---
    '''
    
    parser = CodeParser(example_text)
    print(parser.get_parsed_data())
