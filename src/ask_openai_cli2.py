import argparse
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load the API key from the .env file
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

if not api_key:
    raise ValueError("No OpenAI API key found. Please check your .env file.")

# Initialize LangChain's OpenAI interface
llm = ChatOpenAI(
    model_name='gpt-4-1106-preview',
    openai_api_key=api_key
)

def ask_question(question):
    response = llm.invoke(question)
    return response

def main():
    parser = argparse.ArgumentParser(description="Ask a question to OpenAI.")
    parser.add_argument("--question", type=str, help="Question to ask OpenAI")
    parser.add_argument("--f", type=str, help="File containing the question")
    parser.add_argument("--r", type=str, help="File to save the answer")

    args = parser.parse_args()

    if args.question:
        question = args.question
    elif args.f:
        with open(args.f, "r") as file:
            question = file.read()
    else:
        print("Please provide a question using --question or --f options.")
        return

    answer = ask_question(question)

    if args.r:
        with open(args.r, "w") as file:
            file.write(answer.content)
    else:
        print(f"Answer: {answer}")

if __name__ == "__main__":
    main()

