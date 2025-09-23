import requests
import os
from dotenv import load_dotenv

load_dotenv()


url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
api_key = os.getenv("GEMINI_API_KEY")

headers = {
    "Content-Type": "application/json",
    "X-goog-api-key": api_key,
}



def generate(query):
    data = {
        "contents": [
            {
                "parts": [
                    {"text": f'Answer to the user query in one to three sentencess. User query {query}'}
                ]
            }
        ]
    }


    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        try:
            text_output = result["candidates"][0]["content"]["parts"][0]["text"]
            return {
                "status": "success",
                "output": text_output
            }
        except (KeyError, IndexError):
            return {
                "status": "error",
                "details": "error in parsing"
            }
    else:
        return {
            "status": "error",
            "error_code": response.status_code
        }