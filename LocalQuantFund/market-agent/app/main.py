from fastapi import FastAPI
from app.routes import webhook

app = FastAPI()
app.include_router(webhook.router)

@app.get("/health")
async def health():
    return {"status": "ok"}
