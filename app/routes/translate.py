# from fastapi import APIRouter
# from pydantic import BaseModel

# router = APIRouter()

# class TranslateReq(BaseModel):
#     text: str
#     target: str
#     source: str | None = None

# @router.post("/translate")
# def translate(req: TranslateReq):
#     # temporary stub: just echoes back so we can test the contract
#     return {"translated_text": f"[stub->{req.target}] {req.text}", "provider": "stub"}

import os, httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()
DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")
DEEPL_URL = "https://api.deepl.com/v2/translate"  # if you're on Free plan: https://api-free.deepl.com/v2/translate

class TranslateReq(BaseModel):
    text: str
    target: str            # "en" | "de" | "ar"
    source: str | None = None

@router.post("/translate")
async def translate(req: TranslateReq):
    if not DEEPL_API_KEY:
        raise HTTPException(500, "DEEPL_API_KEY not configured")
    params = {
        "auth_key": DEEPL_API_KEY,
        "text": req.text,
        "target_lang": req.target.upper(),
    }
    if req.source:
        params["source_lang"] = req.source.upper()

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.post(DEEPL_URL, data=params)
        r.raise_for_status()
        data = r.json()
        return {"translated_text": data["translations"][0]["text"], "provider": "deepl"}
    except httpx.HTTPError as e:
        raise HTTPException(502, f"Translation provider error: {e}")
