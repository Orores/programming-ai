import os
import requests
from dotenv import load_dotenv

class TogetherAIModelRetriever:
    """
    TogetherAIModelRetriever: This class handles retrieving available models from the TogetherAI API.
    """

    @staticmethod
    def get_api_key():
        load_dotenv()
        return os.getenv("TOGETHERAI_API_KEY")

    @staticmethod
    def get_available_models(api_key=None):
        api_key = api_key if api_key else TogetherAIModelRetriever.get_api_key()
        endpoint_url = 'https://api.together.xyz/v1/models'
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {api_key}",
        }

        response = requests.get(endpoint_url, headers=headers)
        
        if response.status_code == 200:
            models = response.json()
            return models
        else:
            raise Exception('Failed to retrieve models from TogetherAI API')

    @staticmethod
    def print_models_table(models):
        # Define the header and row format
        headers = ["ID", "Type", "Pricing (Hourly)", "Pricing (Input)", "Pricing (Output)", "Pricing (Base)"]
        row_format = "{:<40} {:<10} {:<8} {:<8} {:<8} {:<8}"
        
        # Print the header
        print(row_format.format(*headers))
        print("-" * 120)
        
        # Print each model
        for model in models:
            model_id = model.get('id', 'N/A')
            model_type = model.get('type', 'N/A')
            pricing = model.get('pricing', {})
            hourly = pricing.get('hourly', 'N/A')
            input_cost = pricing.get('input', 'N/A')
            output_cost = pricing.get('output', 'N/A')
            base_cost = pricing.get('base', 'N/A')
            
            print(row_format.format(model_id, model_type, hourly, input_cost, output_cost, base_cost))

# Testing the class (optional)
if __name__ == '__main__':
    api_key = TogetherAIModelRetriever.get_api_key()
    models = TogetherAIModelRetriever.get_available_models(api_key)
    print("Available Models for TogetherAI:\n")
    TogetherAIModelRetriever.print_models_table(models)
