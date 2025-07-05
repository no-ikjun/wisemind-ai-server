from pydantic import BaseModel

class ContentResponse(BaseModel):
    content: str
