from fastapi import APIRouter
from app.models.content import ContentResponse

router = APIRouter()

@router.get("/test", response_model=ContentResponse)
async def test_content():
    return {"content": "Financial Content 생성 테스트"}
