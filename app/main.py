from fastapi import FastAPI
from app.routes import translate ,recommend  # later add chatbot, recommend

app = FastAPI(title="AutoOne AI Layer")

# health check (good for testing if app is running)
@app.get("/healthz")
def healthz():
    return {"ok": True}

# include translation routes
app.include_router(translate.router, prefix="/api")


# and for recommendations:
# from app.routes import recommend
app.include_router(recommend.router, prefix="/api")
