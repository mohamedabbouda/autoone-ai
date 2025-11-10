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








# import os, httpx
# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# from dotenv import load_dotenv

# # load variables from .env file
# load_dotenv()
# router = APIRouter()
# DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")
# DEEPL_URL = "https://api.deepl.com/v2/translate"  

# class TranslateReq(BaseModel):
#     text: str
#     target: str            # "en" | "de" | "ar"
#     source: str | None = None

# @router.post("/translate")
# async def translate(req: TranslateReq):
#     if not DEEPL_API_KEY:
#         raise HTTPException(500, "DEEPL_API_KEY not configured")
#     params = {
#         "auth_key": DEEPL_API_KEY,
#         "text": req.text,
#         "target_lang": req.target.upper(),
#     }
#     if req.source:
#         params["source_lang"] = req.source.upper()

#     try:
#         async with httpx.AsyncClient(timeout=15) as client:
#             r = await client.post(DEEPL_URL, data=params)
#         r.raise_for_status()
#         data = r.json()
#         return {"translated_text": data["translations"][0]["text"], "provider": "deepl"}
#     except httpx.HTTPError as e:
#         raise HTTPException(502, f"Translation provider error: {e}")


from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, validator
from app.services.translate_service import translate_text

router = APIRouter()

SUPPORTED_LANGS = {"EN", "DE", "AR"}  # you can extend this later

class TranslateReq(BaseModel):
    text: str
    target: str
    source: str | None = None

    @validator("target")
    def validate_target(cls, v):
        v = v.upper()
        if v not in SUPPORTED_LANGS:
            raise ValueError(f"Unsupported target language '{v}'. Use one of {SUPPORTED_LANGS}")
        return v

    # validate source if provided
    @validator("source")
    def validate_source(cls, v):
        if v:
            v = v.upper()
            if v not in SUPPORTED_LANGS:
                raise ValueError(f"Unsupported source language '{v}'. Use one of {SUPPORTED_LANGS}")
        return v
    

@router.post("/translate")
async def translate(req: TranslateReq):
    try:
        translated = await translate_text(req.text, req.target, req.source)
        return {"translated_text": translated, "provider": "deepl"}
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))
        