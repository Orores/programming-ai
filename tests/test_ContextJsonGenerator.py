import os
import sys
import json
import shutil
import tempfile
import unittest

sys.path.append('src')
from ContextJsonGenerator import ContextJsonGenerator

class TestContextJsonGenerator(unittest.TestCase):

    def setUp(self):
        # Create temporary directories for input and output
        self.input_directory = "temp_input"
        self.output_directory = "temp_output"

        os.makedirs(self.input_directory, exist_ok=True)
        os.makedirs(self.output_directory, exist_ok=True)

        # Create sample role and content files in the input directory
        with open(os.path.join(self.input_directory, "role_1.txt"), 'w') as role_file:
            role_file.write("Role 1 Data")

        with open(os.path.join(self.input_directory, "content_1.txt"), 'w') as content_file:
            content_file.write("Content 1 Data")

    def tearDown(self):
        # Remove temporary directories and files
        shutil.rmtree(self.input_directory)
        shutil.rmtree(self.output_directory)

    def test_generate_json(self):
        # Initialize the ContextJsonGenerator with the temporary input directory
        json_generator = ContextJsonGenerator(self.input_directory)

        # Generate JSON in the temporary output directory
        json_generator.generate_json(self.output_directory)

        # Verify that the JSON file is created in the output directory
        json_file_path = os.path.join(self.output_directory, f"{self.input_directory}.json")
        self.assertTrue(os.path.exists(json_file_path))

        # Optionally, you can also check the content of the generated JSON file
        with open(json_file_path, 'r') as json_file:
            json_data = json.load(json_file)
            self.assertEqual(len(json_data), 1)
            self.assertEqual(json_data[0]["role"], "Role 1 Data")
            self.assertEqual(json_data[0]["content"], "Content 1 Data")

if __name__ == '__main__':
    unittest.main()
