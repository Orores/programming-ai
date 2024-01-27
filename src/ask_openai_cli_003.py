import requests
import json
import os
from dotenv import load_dotenv

def load_api_key():
    load_dotenv()
    return os.getenv("OPENAI_API_KEY")

def create_conversation():
    return [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
        {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        {"role": "user", "content": "Where was it played?"}
    ]

def make_api_request(api_key, conversation):
    endpoint_url = 'https://api.openai.com/v1/chat/completions'
    data = {
        "model": "gpt-3.5-turbo",
        "messages": conversation
    }
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    return requests.post(endpoint_url, headers=headers, json=data)

def extract_assistant_reply(response):
    if response.status_code == 200:
        return json.loads(response.text)['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code} {response.text}"

def main():
    api_key = load_api_key()
    conversation = create_conversation()
    response = make_api_request(api_key, conversation)
    assistant_reply = extract_assistant_reply(response)
    print("Assistant's reply:", assistant_reply)

if __name__ == "__main__":
    main()
