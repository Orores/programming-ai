import os
import json
import requests
from dotenv import load_dotenv

class TogetherAIChatCompletion:
    """
    TogetherAIChatCompletion: This class handles TogetherAI API chat completion requests.
    """

    def __init__(self, api_key=None, model="cognitivecomputations/dolphin-2.5-mixtral-8x7b", max_tokens=4000, temperature=1.0, top_p=0.7, top_k=50, repetition_penalty=1):
        load_dotenv()
        self.api_key = api_key if api_key else os.getenv("TOGETHERAI_API_KEY")
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.top_k = top_k
        self.repetition_penalty = repetition_penalty
        self.endpoint_url = 'https://api.together.xyz/v1/chat/completions'
        
    def make_api_request(self, conversation):
        # Construct the payload
        payload = {
            "model": self.model,
            "messages": conversation,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "top_k": self.top_k,
            "repetition_penalty": self.repetition_penalty,
            "stream": False
        }

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        response = requests.post(self.endpoint_url, json=payload, headers=headers)
        return response.json()
