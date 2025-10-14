import os
import httpx
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")
# use api-free.deepl.com if you are on the Free plan
DEEPL_URL = "https://api-free.deepl.com/v2/translate"

async def translate_text(text: str, target: str, source: str | None = None) -> str:
    """Translate text using DeepL API"""
    if not DEEPL_API_KEY:
        raise RuntimeError("DEEPL_API_KEY not configured")

    params = {
        "auth_key": DEEPL_API_KEY,
        "text": text,
        "target_lang": target.upper(),
    }
    if source:
        params["source_lang"] = source.upper()

    async with httpx.AsyncClient(timeout=15) as client:
        response = await client.post(DEEPL_URL, data=params)
    response.raise_for_status()

    data = response.json()
    return data["translations"][0]["text"]
