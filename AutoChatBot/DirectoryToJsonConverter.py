import os
import json

class DirectoryToJsonConverter:
    """
    The code takes a directory specified by the `input_directory` variable as input. Within this directory, there are subdirectories containing files named `role_i` and `content_i`, where `i` ranges from 1 to `n`. The goal is to transform each subdirectory into a JSON object with the subdirectory's name. Each JSON object will contain an array of objects structured as follows:

    ```
    [
        {"role": "role_1_string", "content": "content_1_string"},
        {"role": "role_2_string", "content": "content_2_string"},
        ...
    ]
    ```

    This transformation should be applied to each subdirectory up to `n`. The resulting JSON objects will be saved to a directory specified by the `output_directory` variable.
    """

    def __init__(self, input_directory, output_directory):
        self.input_directory = input_directory
        self.output_directory = output_directory

    def convert_directories_to_json(self):
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)

        for subdir in os.listdir(self.input_directory):
            subdir_path = os.path.join(self.input_directory, subdir)
            
            roles_contents = []
            for i in range(1, 1000): # Assuming up to 1000 subdirectories
                role_file = os.path.join(subdir_path, f'role_{i}.txt')
                content_file = os.path.join(subdir_path, f'content_{i}.txt')
                 
                if not os.path.exists(role_file) or not os.path.exists(content_file):
                    break
                with open(role_file, 'r') as role_fp, open(content_file, 'r') as content_fp:
                    role_content = {"role": role_fp.read().strip(), "content": content_fp.read().strip()}
                    roles_contents.append(role_content)
            
            output_json_file = os.path.join(self.output_directory, f'{subdir}.json')
            with open(output_json_file, 'w') as json_fp:
                json.dump(roles_contents, json_fp, indent=4)

# Example usage
input_directory = 'raw_context'
output_directory = 'context_prompts'

converter = DirectoryToJsonConverter(input_directory, output_directory)
converter.convert_directories_to_json()

