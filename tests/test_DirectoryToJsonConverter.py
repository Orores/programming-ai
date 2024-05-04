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

    Sample Folder/File Hierarchies:
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

        # Create additional subdirectories with role and content files for alternate testing
        for subdir_name in ['subdir3', 'subdir4']:
            subdir_path = os.path.join(self.tmp_input_dir.name, subdir_name)
            os.makedirs(subdir_path)

            # Create role and content files with alternate naming convention
            for i in range(1, 4):
                with open(os.path.join(subdir_path, f'role{i}.txt'), 'w') as role_fp:
                    role_fp.write(f'Role {i} for {subdir_name}')
                with open(os.path.join(subdir_path, f'content{i}.txt'), 'w') as content_fp:
                    content_fp.write(f'Content {i} for {subdir_name}')

    def test_convert_directories_to_json(self):
        converter = DirectoryToJsonConverter(self.tmp_input_dir.name, self.tmp_output_dir.name)
        converter.convert_directories_to_json()

        # Check if JSON files were created correctly for role_i content_i
        for subdir_name in ['subdir1', 'subdir2']:
            json_file_path = os.path.join(self.tmp_output_dir.name, f'{subdir_name}.json')
            self.assertTrue(os.path.exists(json_file_path), f"JSON file {json_file_path} does not exist.")

            with open(json_file_path, 'r') as json_fp:
                json_data = json.load(json_fp)
                self.assertEqual(len(json_data), 3)

        # Check if JSON files were created correctly for rolei contenti
        for subdir_name in ['subdir3', 'subdir4']:
            json_file_path = os.path.join(self.tmp_output_dir.name, f'{subdir_name}.json')
            self.assertTrue(os.path.exists(json_file_path), f"JSON file {json_file_path} does not exist.")

            with open(json_file_path, 'r') as json_fp:
                json_data = json.load(json_fp)
                self.assertEqual(len(json_data), 3)

    def tearDown(self):
        self.tmp_input_dir.cleanup()
        self.tmp_output_dir.cleanup()

class TestDirectoryToJsonConverterSingle(unittest.TestCase):
    """
    TestDirectoryToJsonConverterSingle: This class is a unit test case for the DirectoryToJsonConverter class.
    
    Steps:
    1. Set up a temporary input directory with subdirectories and role/content files.
    2. Clean up the temporary input directory after the test completes.
    3. Test the convert_directories_to_single_json() method of DirectoryToJsonConverter.
    4. Check if the output JSON file was created and has the expected content.
    
    Example usage:
        unittest.main()
        
    Directory structure example:
        - input_directory
            - subdir1
                - role_1.txt
                - content_1.txt
                - role_2.txt
                - content_2.txt
            - subdir2
                - role_1.txt
                - content_1.txt
                
    Expected JSON structure:
        {
            "subdir1": [
                {"role": "role_1_string", "content": "content_1_string"},
                {"role": "role_2_string", "content": "content_2_string"}
            ],
            "subdir2": [
                {"role": "role_1_string", "content": "content_1_string"}
            ]
        }
    """
    def setUp(self):
        # Create a temporary input directory
        self.input_directory = tempfile.TemporaryDirectory()

        # Create subdirectories with role and content files
        subdir1 = os.path.join(self.input_directory.name, 'subdir1')
        os.makedirs(subdir1)
        with open(os.path.join(subdir1, 'role_1.txt'), 'w') as f:
            f.write('role_1_string')
        with open(os.path.join(subdir1, 'content_1.txt'), 'w') as f:
            f.write('content_1_string')
        with open(os.path.join(subdir1, 'role_2.txt'), 'w') as f:
            f.write('role_2_string')
        with open(os.path.join(subdir1, 'content_2.txt'), 'w') as f:
            f.write('content_2_string')

        subdir2 = os.path.join(self.input_directory.name, 'subdir2')
        os.makedirs(subdir2)
        with open(os.path.join(subdir2, 'role_1.txt'), 'w') as f:
            f.write('role_1_string')
        with open(os.path.join(subdir2, 'content_1.txt'), 'w') as f:
            f.write('content_1_string')

    def tearDown(self):
        # Clean up the temporary input directory
        self.input_directory.cleanup()

    def test_convert_directories_to_single_json(self):
        # Create a temporary output directory
        with tempfile.TemporaryDirectory() as output_directory:
            # Create an instance of DirectoryToJsonConverter
            converter = DirectoryToJsonConverter(self.input_directory.name, output_directory)

            # Call the convert_directories_to_single_json method
            converter.convert_directories_to_single_json()

            # Check if the output JSON file was created
            output_json_file = os.path.join(output_directory, 'all_directories.json')
            self.assertTrue(os.path.exists(output_json_file), "The output JSON file was not created.")

            # Read the output JSON file
            with open(output_json_file, 'r') as f:
                output_data = json.load(f)

            # Check the content of the JSON file
            expected_output_data = {
                'subdir1': [
                    {'role': 'role_1_string', 'content': 'content_1_string'},
                    {'role': 'role_2_string', 'content': 'content_2_string'}
                ],
                'subdir2': [
                    {'role': 'role_1_string', 'content': 'content_1_string'}
                ]
            }
            self.assertEqual(output_data, expected_output_data, "The output JSON file does not have the expected content.")

if __name__ == '__main__':
    unittest.main()
