from pydantic import BaseModel
from typing import Optional
from app.models.models import ArticleStatus

class InteractionBase(BaseModel):
    status: ArticleStatus = ArticleStatus.UNREAD
    is_liked: bool = False
    note: Optional[str] = None

class InteractionCreate(InteractionBase):
    article_id: int

class InteractionUpdate(BaseModel):
    is_liked: Optional[bool] = None
    note: Optional[str] = None
    status: Optional[ArticleStatus] = None

class InteractionSchema(InteractionBase):
    id: int
    article_id: int
    user_id: int

    class Config:
        from_attributes = True