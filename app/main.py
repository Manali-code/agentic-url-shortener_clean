from fastapi import FastAPI

from app.api.routes import router as api_router
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Agentic URL Shortener", version="1.0.0")
app.include_router(api_router)


@app.get("/")
def read_root():
    return {"message": "Agentic URL Shortener API is running"}
