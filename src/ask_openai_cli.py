import argparse
import os
from dotenv import load_dotenv
from langchain_openai import OpenAI

# Load the API key from the .env file
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

if not api_key:
    raise ValueError("No OpenAI API key found. Please check your .env file.")

# Initialize LangChain's OpenAI interface
llm = OpenAI(api_key=api_key)

def ask_question(question):
    response = llm.invoke(question)
    return response

def main():
    parser = argparse.ArgumentParser(description="Ask a question to OpenAI.")
    parser.add_argument("--question", type=str, required=True, help="Question to ask OpenAI")

    args = parser.parse_args()
    answer = ask_question(args.question)
    print(f"Answer: {answer}")

if __name__ == "__main__":
    main()
