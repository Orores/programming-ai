import argparse
import requests
from dotenv import load_dotenv
import os
import time

def load_api_key():
    load_dotenv()
    return os.getenv("OPENAI_API_KEY")

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
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code} {response.text}"

def ask_question(question):
    api_key = load_api_key()

    conversation = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": question}
    ]

    response = make_api_request(api_key, conversation)
    assistant_reply = extract_assistant_reply(response)

    return assistant_reply  # Return the response instead of printing it

def main():
    parser = argparse.ArgumentParser(description="Ask a question to OpenAI's GPT-3 model.")
    parser.add_argument("--question", type=str, help="The question to ask the assistant.")
    args = parser.parse_args()

    if args.question:
        # Called from command line with --question argument
        assistant_reply = ask_question(args.question)
        print("Assistant's reply:", assistant_reply)
    else:
        # No arguments provided, display help message
        parser.print_help()

if __name__ == '__main__':
    main()
