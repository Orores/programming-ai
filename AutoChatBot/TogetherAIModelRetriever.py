import os
import requests
from dotenv import load_dotenv

class TogetherAIModelRetriever:
    """
    TogetherAIModelRetriever: This class handles retrieving available models from the TogetherAI API.
    """

    def __init__(self, api_key=None):
        load_dotenv()
        self.api_key = api_key if api_key else os.getenv("TOGETHERAI_API_KEY")
        self.endpoint_url = 'https://api.together.xyz/v1/models'

    def get_available_models(self):
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        response = requests.get(self.endpoint_url, headers=headers)
        
        if response.status_code == 200:
            models = response.json()
            return models
        else:
            raise Exception('Failed to retrieve models from TogetherAI API')

# Testing the class (optional)
if __name__ == '__main__':
    retriever = TogetherAIModelRetriever()
    models = retriever.get_available_models()
    print("Available Models for TogetherAI:\n")
    for model in models:
            display_name = model.get('display_name', 'N/A')
            model_type = model.get('type', 'N/A')
            pricing = model.get('pricing', 'N/A')
            print(f"Name: {display_name}, Type: {model_type}, Pricing: {pricing}")

