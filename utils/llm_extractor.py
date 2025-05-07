import requests
import os
from dotenv import load_dotenv

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def query_openrouter(context):
    messages = [
        {
            "role": "system",
            "content": (
                "You are an AI assistant with access to full website documentation.\n"
                "Given the content below, extract the documentation structure into:\n"
                "- Modules\n"
                "- Submodules\n"
                "- Descriptions\n"
                "Format it in clear bullet points to help product managers understand the product quickly.\n\n"
                f"{context[:12000]}"
            )
        },
        {
            "role": "user",
            "content": "Please extract the documentation structure."
        }
    ]

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek/deepseek-r1:free",
        "messages": messages
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)

    if response.status_code == 200:
        try:
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Failed to parse LLM response: {e}"
    else:
        return f"OpenRouter Error {response.status_code}: {response.text}"
