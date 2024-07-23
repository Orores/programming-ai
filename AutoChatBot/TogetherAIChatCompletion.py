import os
import json
import requests
from dotenv import load_dotenv

class TogetherAIChatCompletion:
    """
    TogetherAIChatCompletion: This class handles TogetherAI API chat completion requests.
    """

    @staticmethod
    def load_api_key():
        load_dotenv()
        return os.getenv("TOGETHERAI_API_KEY")

    @staticmethod
    def make_api_request(conversation, api_key=None, model="cognitivecomputations/dolphin-2.5-mixtral-8x7b", max_tokens=4000, temperature=1.0, top_p=0.7, top_k=50, repetition_penalty=1):
        api_key = api_key if api_key else TogetherAIChatCompletion.load_api_key()
        
        payload = {
            "model": model,
            "messages": conversation,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
            "repetition_penalty": repetition_penalty,
            "stream": False
        }

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }

        response = requests.post('https://api.together.xyz/v1/chat/completions', json=payload, headers=headers)
        return response.json()
