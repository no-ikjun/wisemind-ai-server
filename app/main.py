from fastapi import FastAPI
from app.api import content

app = FastAPI()

app.include_router(content.router, prefix="/content", tags=["Content"])
