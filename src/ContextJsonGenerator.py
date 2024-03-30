import os
import json

class ContextJsonGenerator:
    def __init__(self, directory):
        self.directory = directory

    def generate_json(self, output_directory=None):
        if output_directory is None:
            output_directory = "context_prompts"

        json_data = []  # Initialize list to store JSON data

        for i in range(1, len(os.listdir(self.directory)) // 2 + 1):  # Adjust the range based on the number of files
            role_filename = f"role_{i}.txt"
            content_filename = f"content_{i}.txt"

            # Extract role and content data for each pair of files
            with open(os.path.join(self.directory, role_filename), 'r') as role_file, open(os.path.join(self.directory, content_filename), 'r') as content_file:
                role = role_file.readline().strip()
                content = content_file.readline().strip()

                # Construct and append the JSON data in the specified order
                data = {
                    "role": role,
                    "content": content
                }
                json_data.append(data)

        # Construct the output file path
        output_file = os.path.join(output_directory, f"{self.directory}.json")

        # Create the output directory if it does not exist
        os.makedirs(output_directory, exist_ok=True)

        with open(output_file, 'w') as json_file:
            json.dump(json_data, json_file, indent=4)

if __name__ == "__main__":
    # Example Usage specifying output directory
    directory = "test1"
    output_directory = "context_prompts"  # Specify your output directory here
    json_generator = ContextJsonGenerator(directory)
    json_generator.generate_json(output_directory)
