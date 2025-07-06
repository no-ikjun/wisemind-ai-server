from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import content, recommend, chatbot

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://analyst.ikjun.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(content.router, prefix="/content", tags=["Content"])
app.include_router(recommend.router, prefix="/recommend", tags=["Recommend"])
app.include_router(chatbot.router, prefix="/chatbot", tags=["Chatbot"])