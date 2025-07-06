# app/routers/chatbot_router.py

from fastapi import APIRouter, Body
from app.services.chatbot_service import get_chatbot_response
from app.services.chatbot_service import reset_chatbot_session

router = APIRouter()

@router.post("/message")
def chatbot_message(payload: dict = Body(...)):
    user_message = payload.get("message", "")
    session_id = payload.get("session_id", "")

    if not user_message or not session_id:
        return {"error": "필수 값 누락"}

    response = get_chatbot_response(session_id, user_message)
    return {"response": response}
    
@router.post("/reset")
def reset_session(payload: dict = Body(...)):
    session_id = payload.get("session_id", "")
    if not session_id:
        return {"error": "세션 ID가 필요합니다."}
    success = reset_chatbot_session(session_id)
    if success: 
        return {"message": "세션이 초기화되었습니다."}
    else:
        return {"error": "세션 초기화 실패. 세션 ID가 존재하지 않습니다."}
    