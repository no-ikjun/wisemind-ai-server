from fastapi import FastAPI
from app.api import content, recommend

app = FastAPI()

app.include_router(content.router, prefix="/content", tags=["Content"])
app.include_router(recommend.router, prefix="/recommend", tags=["Recommend"])
