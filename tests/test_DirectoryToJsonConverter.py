import unittest
import tempfile
import os
import sys
import json

# Add the src directory to the Python path for imports
sys.path.append('AutoChatBot')

from DirectoryToJsonConverter import DirectoryToJsonConverter

class TestDirectoryToJsonConverter(unittest.TestCase):
    """Test class for the DirectoryToJsonConverter.

    This class is designed to test the functionality of the DirectoryToJsonConverter class,
    which is responsible for converting directories containing role and content files into JSON format.

    Testing Methodology:
    1. Set up a temporary input directory with subdirectories and files for testing.
    2. Create an instance of the DirectoryToJsonConverter class and convert the directories to JSON.
    3. Check if JSON files were created correctly for each subdirectory.
    4. Verify the content of the JSON files against the expected structure.
    5. Clean up the temporary directories after testing.

    Testing Steps:
    - setUp: Prepare the input directory with testing data.
    - test_convert_directories_to_json: Test the conversion of directories to JSON format.
    - tearDown: Clean up the temporary directories used for testing.

    Test Cases:
    - test_convert_directories_to_json: Tests the conversion process and JSON file creation.

    Attributes:
    - tmp_input_dir: Temporary directory for input data.
    - tmp_output_dir: Temporary directory for output data.

    Sample Folder/Files Hierarchy:
    - Input Directory:
        - subdir1
            - role_1.txt
            - role_2.txt
            - role_3.txt
            - content_1.txt
            - content_2.txt
            - content_3.txt
        - subdir2
            - role_1.txt
            - role_2.txt
            - role_3.txt
            - content_1.txt
            - content_2.txt
            - content_3.txt

    Sample JSON Format:
    Each JSON file represents a subdirectory and contains an array of dictionaries where each dictionary
    corresponds to a role and its associated content. Example:
    {
        "roles": [
            {
                "role": "Role 1 for subdir1",
                "content": "Content 1 for subdir1"
            },
            {
                "role": "Role 2 for subdir1",
                "content": "Content 2 for subdir1"
            },
            {
                "role": "Role 3 for subdir1",
                "content": "Content 3 for subdir1"
            }
        ]
    }

    """

    def setUp(self):
        self.tmp_input_dir = tempfile.TemporaryDirectory()
        self.tmp_output_dir = tempfile.TemporaryDirectory()

        # Create subdirectories with role and content files for testing
        for subdir_name in ['subdir1', 'subdir2']:
            subdir_path = os.path.join(self.tmp_input_dir.name, subdir_name)
            os.makedirs(subdir_path)

            # Create role and content files
            for i in range(1, 4):
                with open(os.path.join(subdir_path, f'role_{i}.txt'), 'w') as role_fp:
                    role_fp.write(f'Role {i} for {subdir_name}')
                with open(os.path.join(subdir_path, f'content_{i}.txt'), 'w') as content_fp:
                    content_fp.write(f'Content {i} for {subdir_name}')

    def test_convert_directories_to_json(self):
        converter = DirectoryToJsonConverter(self.tmp_input_dir.name, self.tmp_output_dir.name)
        converter.convert_directories_to_json()

        # Check if JSON files were created correctly
        for subdir_name in ['subdir1', 'subdir2']:
            json_file_path = os.path.join(self.tmp_output_dir.name, f'{subdir_name}.json')
            self.assertTrue(os.path.exists(json_file_path), f"JSON file {json_file_path} does not exist.")

            with open(json_file_path, 'r') as json_fp:
                json_data = json.load(json_fp)
                self.assertEqual(len(json_data), 3)

    def tearDown(self):
        self.tmp_input_dir.cleanup()
        self.tmp_output_dir.cleanup()

if __name__ == '__main__':
    unittest.main()
