from fastapi import FastAPI
from app.routes.translate import router as translate_router

app = FastAPI(title="AutoOne AI")

@app.get("/healthz")
def healthz():
    return {"ok": True}

app.include_router(translate_router, prefix="/api")
