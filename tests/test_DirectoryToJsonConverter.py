import unittest
import tempfile
import os
import sys
import json
from AutoChatBot.DirectoryToJsonConverter import DirectoryToJsonConverter

class TestDirectoryToJsonConverter(unittest.TestCase):
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
        DirectoryToJsonConverter.convert_directories_to_json(self.tmp_input_dir.name, self.tmp_output_dir.name)

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
    def setUp(self):
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
        self.input_directory.cleanup()

    def test_convert_directories_to_single_json(self):
        with tempfile.TemporaryDirectory() as output_directory:
            DirectoryToJsonConverter.convert_directories_to_single_json(self.input_directory.name, output_directory)

            output_json_file = os.path.join(output_directory, 'context.json')
            self.assertTrue(os.path.exists(output_json_file), "The output JSON file was not created.")

            with open(output_json_file, 'r') as f:
                output_data = json.load(f)

            expected_output_data = {
                'subdir1': {
                    'context': [
                        {'role': 'role_1_string', 'content': 'content_1_string'},
                        {'role': 'role_2_string', 'content': 'content_2_string'}
                    ]
                },
                'subdir2': {
                    'context': [
                        {'role': 'role_1_string', 'content': 'content_1_string'}
                    ]
                }
            }
            self.assertEqual(output_data, expected_output_data, "The output JSON file does not have the expected content.")

class TestDirectoryToJsonConverterBasedOnMode(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.TemporaryDirectory()

        cls.subdir1 = os.path.join(cls.temp_dir.name, 'subdir1')
        os.makedirs(cls.subdir1)
        with open(os.path.join(cls.subdir1, 'role_1.txt'), 'w') as f:
            f.write("role_1_string")
        with open(os.path.join(cls.subdir1, 'content_1.txt'), 'w') as f:
            f.write("content_1_string")
        with open(os.path.join(cls.subdir1, 'role_2.txt'), 'w') as f:
            f.write("role_2_string")
        with open(os.path.join(cls.subdir1, 'content_2.txt'), 'w') as f:
            f.write("content_2_string")

        cls.subdir2 = os.path.join(cls.temp_dir.name, 'subdir2')
        os.makedirs(cls.subdir2)
        with open(os.path.join(cls.subdir2, 'role_1.txt'), 'w') as f:
            f.write("role_1_string")
        with open(os.path.join(cls.subdir2, 'content_1.txt'), 'w') as f:
            f.write("content_1_string")

    @classmethod
    def tearDownClass(cls):
        cls.temp_dir.cleanup()

    def test_convert_directories_to_json(self):
        output_directory = os.path.join(self.temp_dir.name, 'output')
        DirectoryToJsonConverter.convert_directories_to_json_based_on_mode(self.temp_dir.name, output_directory, 'multiple')

        self.assertTrue(os.path.exists(os.path.join(output_directory, 'subdir1.json')))
        self.assertTrue(os.path.exists(os.path.join(output_directory, 'subdir2.json')))

        with open(os.path.join(output_directory, 'subdir1.json'), 'r') as f:
            json_data = json.load(f)
            expected_data = [
                {"role": "role_1_string", "content": "content_1_string"},
                {"role": "role_2_string", "content": "content_2_string"}
            ]
            self.assertEqual(json_data, expected_data)

        with open(os.path.join(output_directory, 'subdir2.json'), 'r') as f:
            json_data = json.load(f)
            expected_data = [
                {"role": "role_1_string", "content": "content_1_string"}
            ]
            self.assertEqual(json_data, expected_data)

    def test_convert_directories_to_single_json(self):
        output_directory = os.path.join(self.temp_dir.name, 'output')
        DirectoryToJsonConverter.convert_directories_to_json_based_on_mode(self.temp_dir.name, output_directory, 'single')

        self.assertTrue(os.path.exists(os.path.join(output_directory, 'context.json')))

        with open(os.path.join(output_directory, 'context.json'), 'r') as f:
            json_data = json.load(f)
            expected_data = {
                "subdir1": {
                    "context": [
                        {"role": "role_1_string", "content": "content_1_string"},
                        {"role": "role_2_string", "content": "content_2_string"}
                    ]
                },
                "subdir2": {
                    "context": [
                        {"role": "role_1_string", "content": "content_1_string"}
                    ]
                },
                "output" : {
                    "context" : [] # Because the output directory is in the same folder as the subdirs, hence the test is bad.
                }
            }
            self.assertEqual(json_data, expected_data)

if __name__ == '__main__':
    unittest.main()
