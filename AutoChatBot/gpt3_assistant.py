import requests
from dotenv import load_dotenv
import os

class GPT3Assistant:
    def __init__(self, api_key=None, endpoint_url=None):
        if not api_key:
            load_dotenv()
            self.api_key = os.getenv("OPENAI_API_KEY")
        else:
            self.api_key = api_key

        if not endpoint_url:
            self.endpoint_url = 'https://api.openai.com/v1/chat/completions'
        else:
            self.endpoint_url = endpoint_url

    def make_api_request(self, conversation):
        data = {
            "model": "gpt-3.5-turbo",
            "messages": conversation
        }
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        return requests.post(self.endpoint_url, headers=headers, json=data)

    def extract_assistant_reply(self, response):
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"Error: {response.status_code} {response.text}"

    def ask_question(self, question='Default question if none provided.'):
        conversation = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question}
        ]
        
        response = self.make_api_request(conversation)

        return self.extract_assistant_reply(response)

if __name__ == '__main__':
    assistant = GPT3Assistant()
    question = input("Enter a question: ")
    response = assistant.ask_question(question)
    print("Assistant's reply:", response)
