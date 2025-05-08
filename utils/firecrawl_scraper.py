import requests
import os
from dotenv import load_dotenv

load_dotenv()

FIRECRAWL_API_KEY = "fc-2bf9bbba79eb45e4a102aac779010516" 
def firecrawl_scrape(url: str, depth: int = 3):
    headers = {
        "Authorization": f"Bearer {FIRECRAWL_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "url": url,
        "options": {
            "crawl": True,
            "discoverPages": True,
            "maxDepth": depth,
            "extractText": True,
            "render": True
        }
    }

    response = requests.post("https://api.firecrawl.dev/v0/scrape", headers=headers, json=payload)

    if response.status_code == 200:
        try:
            result = response.json()
            pages = result.get("pages", [])
            combined_text = "\n\n".join([
                f"[{page.get('url')}]\n{page.get('text', '')}" for page in pages
            ])
            return combined_text
        except Exception as e:
            return f"Error parsing Firecrawl response: {e}"
    else:
        return f"Firecrawl Error {response.status_code}: {response.text}"
