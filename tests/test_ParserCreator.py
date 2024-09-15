import unittest
import sys
from unittest.mock import patch
from AutoChatBot.ParserCreator import ParserCreator  # Assuming your script file is named ParserCreator.py

class TestParserCreator(unittest.TestCase):
    def test_parse_args(self):
        test_args = [
            "--api", "openai", 
            "--model", "gpt-3.5-turbo", 
            "--max_tokens", "200", 
            "--temperature", "0.7", 
            "--frequency_penalty", "0.5",
            "--presence_penalty", "0.3", 
            "--top_p", "0.8", 
            "--top_k", "60", 
            "--repetition_penalty", "1.2", 
            "--stop_sequences", "bye", 
            "--question", "How are you?",
            "--file_path", "/path/to/file", 
            "--save_path", "result.txt", 
            "--context", "/path/to/context", 
            "--run_code", 
            "--show_available_context", 
            "--code_save_path", "scripts/generated_code.py",
            "--multi_file_agent",
            "--reference_files", "ref_file_1.txt", "ref_file_2.txt",
            "--rewrite_files", "rewrite_file_1.txt", "rewrite_file_2.txt",
            "--debug"
        ]
        with patch("sys.argv", ["ParserCreator.py"] + test_args):
            parser = ParserCreator.create_parser()
            args = parser.parse_args()

            # Check if arguments are parsed correctly
            self.assertEqual(args.api, "openai")
            self.assertEqual(args.model, "gpt-3.5-turbo")
            self.assertEqual(args.max_tokens, 200)
            self.assertEqual(args.temperature, 0.7)
            self.assertEqual(args.frequency_penalty, 0.5)
            self.assertEqual(args.presence_penalty, 0.3)
            self.assertEqual(args.top_p, 0.8)
            self.assertEqual(args.top_k, 60)
            self.assertEqual(args.repetition_penalty, 1.2)
            self.assertEqual(args.stop_sequences, ["bye"])
            self.assertEqual(args.question, "How are you?")
            self.assertEqual(args.file_path, "/path/to/file")
            self.assertEqual(args.save_path, "result.txt")
            self.assertEqual(args.context, "/path/to/context")
            self.assertTrue(args.run_code)
            self.assertTrue(args.show_available_context)
            self.assertEqual(args.code_save_path, "scripts/generated_code.py")
            self.assertTrue(args.multi_file_agent)
            self.assertEqual(args.reference_files, ["ref_file_1.txt", "ref_file_2.txt"])
            self.assertEqual(args.rewrite_files, ["rewrite_file_1.txt", "rewrite_file_2.txt"])
            self.assertTrue(args.debug)

if __name__ == "__main__":
    unittest.main()