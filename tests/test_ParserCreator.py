import unittest
import sys
from unittest.mock import patch

# Add the src directory to the Python path for imports
sys.path.append('src')
from ParserCreator import ParserCreator  # Assuming your script file is named ParserCreator.py

class TestParserCreator(unittest.TestCase):
    def test_parse_args(self):
        test_args = ["--model", "gpt-3.5-turbo", "--max_tokens", "200", "--temperature", "0.7", "--frequency_penalty", "0.5",
                     "--presence_penalty", "0.3", "--top_p", "0.8", "--stop_sequences", "bye", "--question", "How are you?",
                     "--file_path", "/path/to/file", "--context", "/path/to/context"]
        with patch("sys.argv", ["ParserCreator.py"] + test_args):
            creator = ParserCreator()
            args = creator.parser.parse_args()

            # Check if arguments are parsed correctly
            self.assertEqual(args.model, "gpt-3.5-turbo")
            self.assertEqual(args.max_tokens, 200)
            self.assertEqual(args.temperature, 0.7)
            self.assertEqual(args.frequency_penalty, 0.5)
            self.assertEqual(args.presence_penalty, 0.3)
            self.assertEqual(args.top_p, 0.8)
            self.assertEqual(args.stop_sequences, ["bye"])
            self.assertEqual(args.question, "How are you?")
            self.assertEqual(args.file_path, "/path/to/file")
            self.assertEqual(args.context, "/path/to/context")

            # Check default value for save_path
            self.assertEqual(args.save_path, "response.tmp")

if __name__ == "__main__":
    unittest.main()
