from fastapi import FastAPI
from pydantic import BaseModel, Field

from .chatbot import DiabetesChatbot

app = FastAPI(title="Diabetes Patient Query Chatbot", version="0.1.0")
bot = DiabetesChatbot()


class ChatRequest(BaseModel):
    session_id: str = Field(..., min_length=1, max_length=64)
    message: str = Field(..., min_length=1, max_length=2000)


class ChatResponse(BaseModel):
    answer: str
    sources: list[str]
    escalated: bool


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    return bot.respond(req.session_id, req.message)
