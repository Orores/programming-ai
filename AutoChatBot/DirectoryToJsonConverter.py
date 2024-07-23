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

    @staticmethod
    def convert_directories_to_json(input_directory, output_directory):
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        for subdir in os.listdir(input_directory):
            subdir_path = os.path.join(input_directory, subdir)
            
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
            
            output_json_file = os.path.join(output_directory, f'{subdir}.json')
            with open(output_json_file, 'w') as json_fp:
                json.dump(roles_contents, json_fp, indent=4)
            
            print(f"Converted '{subdir}' to JSON and saved to '{output_json_file}'")

    @staticmethod
    def convert_directories_to_single_json(input_directory, output_directory):
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        directory_data = {}

        for subdir in os.listdir(input_directory):
            subdir_path = os.path.join(input_directory, subdir)
            
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

        output_json_file = os.path.join(output_directory, 'context.json')
        with open(output_json_file, 'w') as json_fp:
            json.dump(directory_data, json_fp, indent=4)
        
        print(f"All subdirectories have been converted to a single JSON file saved to '{output_json_file}'")

    @staticmethod
    def convert_directories_to_json_based_on_mode(input_directory, output_directory, json_mode):
        if json_mode == 'multiple':
            DirectoryToJsonConverter.convert_directories_to_json(input_directory, output_directory)
        elif json_mode == 'single':
            DirectoryToJsonConverter.convert_directories_to_single_json(input_directory, output_directory)
        else:
            print("Invalid json_mode. Please use 'single' or 'multiple'.")

# Example usage
if __name__ == '__main__':
    input_directory = 'raw_context'
    output_directory = 'AutoChatBot/context_prompts'
    json_mode = 'single'

    DirectoryToJsonConverter.convert_directories_to_json_based_on_mode(input_directory, output_directory, json_mode)
