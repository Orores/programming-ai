from langchain_openai import OpenAI
from dotenv import load_dotenv
import os

# Load the API key from the .env file
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

# Check if the API key is available
if not api_key:
    raise ValueError("No OpenAI API key found. Please check your .env file.")

# Initialize LangChain's OpenAI interface
llm = OpenAI(api_key=api_key)

# Ask a question
question = "What is the capital of France?"
response = llm.invoke(question)

# Print the response
print(f"Question: {question}")
print(f"Answer: {response}")

