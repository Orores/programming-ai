import os
import json

class DirectoryToJsonConverter:
    """
    The code takes a directory specified by the `input_directory` variable as input. Within this directory, there are subdirectories containing files named `role_i` and `content_i`, where `i` ranges from 1 to `n`.
    
    The Class can handle names that are either role_{i}.txt or role{i}.txt
    
    The goal is to transform each subdirectory into a JSON object with the subdirectory's name. Each JSON object will contain an array of objects structured as follows:

    ```
    [
        {"role": "role_1_string", "content": "content_1_string"},
        {"role": "role_2_string", "content": "content_2_string"},
        ...
    ]
    ```

    This transformation should be applied to each subdirectory up to `n`. The resulting JSON objects will be saved to a directory specified by the `output_directory` variable.

    The class also supports generating a single JSON file containing all subdirectories' data, structured as follows:

    context.json
    - subdirectory_name
      - description (optional)
      - context
        - role1
        - content1
        - role2
        - content2
    - next_subdirectory_name
    ...
    """

    def __init__(self, input_directory, output_directory, json_mode='single'):
        self.input_directory = input_directory
        self.output_directory = output_directory
        self.json_mode = json_mode

    def convert_directories_to_json(self):
        """
        Converts subdirectories containing 'role_i.txt' and 'content_i.txt' files into JSON objects.

        The method reads 'role_i.txt' and 'content_i.txt' files within each subdirectory of the input directory.
        It constructs JSON objects representing the subdirectory's content, where each object contains 'role' and 'content' keys.
        The JSON objects are then saved as separate files in the output directory.

        Input:
        - None (Operates on the instance's input_directory and output_directory attributes)

        Output:
        - Creates JSON files in the output directory, each representing a subdirectory's content.
          Each JSON file contains an array of objects with 'role' and 'content' keys:
          [
              {"role": "role_1_string", "content": "content_1_string"},
              {"role": "role_2_string", "content": "content_2_string"},
              ...
          ]

        Raises:
        - No explicit exceptions are raised within this method.
        """

        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)

        for subdir in os.listdir(self.input_directory):
            subdir_path = os.path.join(self.input_directory, subdir)
            
            roles_contents = []
            for i in range(1, 1000): # Assuming up to 1000 subdirectories
                role_file_1 = os.path.join(subdir_path, f'role_{i}.txt')
                content_file_1 = os.path.join(subdir_path, f'content_{i}.txt')
                role_file_2 = os.path.join(subdir_path, f'role{i}.txt')
                content_file_2 = os.path.join(subdir_path, f'content{i}.txt')
                
                if not (os.path.exists(role_file_1) and os.path.exists(content_file_1)) and not (os.path.exists(role_file_2) and os.path.exists(content_file_2)):
                    break
                
                role_file = role_file_1 if os.path.exists(role_file_1) else role_file_2
                content_file = content_file_1 if os.path.exists(content_file_1) else content_file_2
                
                with open(role_file, 'r') as role_fp, open(content_file, 'r') as content_fp:
                    role_content = {"role": role_fp.read().strip(), "content": content_fp.read().strip()}
                    roles_contents.append(role_content)
            
            output_json_file = os.path.join(self.output_directory, f'{subdir}.json')
            with open(output_json_file, 'w') as json_fp:
                json.dump(roles_contents, json_fp, indent=4)
            
            print(f"Converted '{subdir}' to JSON and saved to '{output_json_file}'")

    def convert_directories_to_single_json(self):
        """
        Converts subdirectories containing 'role_i.txt' and 'content_i.txt' files into a single JSON object.

        The method reads 'role_i.txt' and 'content_i.txt' files within each subdirectory of the input directory.
        It constructs a single JSON object with directory names as keys and a list of dictionaries as values.
        Each dictionary represents the content of a subdirectory, containing 'role' and 'content' keys.

        Input:
        - None (Operates on the instance's input_directory and output_directory attributes)

        Output:
        - Creates a single JSON file in the output directory, representing all subdirectories.
          The JSON file contains directory names as keys, and each value is an array of objects with 'role' and 'content' keys:
          {
              "subdirectory1": [
                  {"role": "role_1_string", "content": "content_1_string"},
                  {"role": "role_2_string", "content": "content_2_string"},
                  ...
              ],
              "subdirectory2": [
                  ...
              ],
              ...
          }

        Raises:
        - No explicit exceptions are raised within this method.
        """

        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)

        directory_data = {}

        for subdir in os.listdir(self.input_directory):
            subdir_path = os.path.join(self.input_directory, subdir)
            
            subdir_obj = {'context': []}

            description_file = os.path.join(subdir_path, 'description.txt')
            if os.path.exists(description_file):
                with open(description_file, 'r') as desc_fp:
                    subdir_obj['description'] = desc_fp.read().strip()
            
            for i in range(1, 1000): # Assuming up to 1000 subdirectories
                role_file_1 = os.path.join(subdir_path, f'role_{i}.txt')
                content_file_1 = os.path.join(subdir_path, f'content_{i}.txt')
                role_file_2 = os.path.join(subdir_path, f'role{i}.txt')
                content_file_2 = os.path.join(subdir_path, f'content{i}.txt')
                
                if not (os.path.exists(role_file_1) and os.path.exists(content_file_1)) and not (os.path.exists(role_file_2) and os.path.exists(content_file_2)):
                    break
                
                role_file = role_file_1 if os.path.exists(role_file_1) else role_file_2
                content_file = content_file_1 if os.path.exists(content_file_1) else content_file_2
                
                with open(role_file, 'r') as role_fp, open(content_file, 'r') as content_fp:
                    role_content = {"role": role_fp.read().strip(), "content": content_fp.read().strip()}
                    subdir_obj['context'].append(role_content)
            
            directory_data[subdir] = subdir_obj

            print(f"Converted '{subdir}' to JSON and included in the single JSON file")

        output_json_file = os.path.join(self.output_directory, 'context.json')
        with open(output_json_file, 'w') as json_fp:
            json.dump(directory_data, json_fp, indent=4)
        
        print(f"All subdirectories have been converted to a single JSON file saved to '{output_json_file}'")

    def convert_directories_to_json_based_on_mode(self):
        """
        Converts subdirectories containing 'role_i.txt' and 'content_i.txt' files into JSON objects based on the json_mode parameter.

        The method reads 'role_i.txt' and 'content_i.txt' files within each subdirectory of the input directory.
        It constructs JSON objects representing the subdirectory's content, where each object contains 'role' and 'content' keys.
        The JSON objects are then saved as separate files in the output directory if json_mode is 'multiple'.
        If json_mode is 'single', a single JSON file representing all subdirectories will be created.

        Input:
        - json_mode: A string indicating the mode to determine the JSON conversion method ('single' or 'multiple')

        Output:
        - Creates JSON files in the output directory if json_mode is 'multiple', each representing a subdirectory's content.
          Each JSON file contains an array of objects with 'role' and 'content' keys:
          [
              {"role": "role_1_string", "content": "content_1_string"},
              {"role": "role_2_string", "content": "content_2_string"},
              ...
          ]
        - Creates a single JSON file in the output directory if json_mode is 'single', representing all subdirectories.
          The JSON file contains directory names as keys, and each value is an array of objects with 'role' and 'content' keys:
          {
              "subdirectory1": [
                  {"role": "role_1_string", "content": "content_1_string"},
                  {"role": "role_2_string", "content": "content_2_string"},
                  ...
              ],
              "subdirectory2": [
                  ...
              ],
              ...
          }

        Raises:
        - No explicit exceptions are raised within this method.
        """

        if self.json_mode == 'multiple':
            self.convert_directories_to_json()
        elif self.json_mode == 'single':
            self.convert_directories_to_single_json()
        else:
            print("Invalid json_mode. Please use 'single' or 'multiple'.")

# Example usage
if __name__ == '__main__':
    input_directory = 'raw_context'
    output_directory = 'AutoChatBot/context_prompts'
    json_mode = 'single'

    converter = DirectoryToJsonConverter(input_directory, output_directory, json_mode)
    converter.convert_directories_to_json_based_on_mode()
