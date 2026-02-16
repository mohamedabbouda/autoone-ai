from fastapi import FastAPI
from app.routes import translate ,recommend ,spare_parts # later add chatbot, recommend
import uvicorn


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



app.include_router(spare_parts.router, prefix="/api")



















# if __name__ == "__main__":
#     uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
