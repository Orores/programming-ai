class ChatCompletionSaver:
    """
    ChatCompletionSaver: This class handles saving chat completion responses to a specified file.

    Init parameters:
    - save_path (str): The path to the file where the message content will be saved.

    Main method:
    - save_to_file(response): Saves the message content from the provided response to the specified file.

    Example of response data:
    {
        'id': 'chatcmpl-98SUfXPKMoIF4iIge0cjrXUapUzC6',
        'object': 'chat.completion',
        'created': 1711803181,
        'model': 'gpt-3.5-turbo-0125',
        'choices': [{
            'index': 0,
            'message': {'role': 'assistant', 'content': 'Hello! How can I assist you today?'},
            'logprobs': None,
            'finish_reason': 'stop'
        }],
        'usage': {'prompt_tokens': 18, 'completion_tokens': 9, 'total_tokens': 27},
        'system_fingerprint': 'fp_3bc1b5746c'
    }
    """

    @staticmethod
    def save_to_file(response, save_path):
        """
        Saves the message content from the provided response to the specified file.

        Args:
        - response (dict): The chat completion response containing the message content.
        """
        message_content = response['choices'][0]['message']['content']
        with open(save_path, 'w') as file:
            file.write(message_content)
        print(f"Message content saved to '{save_path}'.")

if __name__ == '__main__':
    response_data = {
        'id': 'chatcmpl-98SUfXPKMoIF4iIge0cjrXUapUzC6',
        'object': 'chat.completion',
        'created': 1711803181,
        'model': 'gpt-3.5-turbo-0125',
        'choices': [{
            'index': 0,
            'message': {'role': 'assistant', 'content': 'Hello! How can I assist you today?'},
            'logprobs': None,
            'finish_reason': 'stop'
        }],
        'usage': {'prompt_tokens': 18, 'completion_tokens': 9, 'total_tokens': 27},
        'system_fingerprint': 'fp_3bc1b5746c'
    }

    # Example usage
    save_path = 'saved_message.txt'  # Change file extension if necessary
    completion_saver = ChatCompletionSaver(save_path)
    completion_saver.save_to_file(response_data)

