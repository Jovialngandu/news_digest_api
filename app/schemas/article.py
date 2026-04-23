
from pydantic import BaseModel
from typing import Optional, Generic, TypeVar, List
from app.schemas.source import SourceSchema
from app.schemas.interaction import InteractionSchema
from datetime import datetime



class ArticleSchema(BaseModel):
    id: int
    title: str
    url: str
    description: Optional[str]	
    content: Optional[str]
    image_url: Optional[str]
    lang: Optional[str]
    source: SourceSchema
    published_at:datetime
    created_at: datetime

    
    class Config:
        from_attributes = True

class FeedArticle(ArticleSchema):
    interaction: Optional[InteractionSchema] = None
    

T = TypeVar("T")

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    next_cursor: Optional[int] = None

    class Config:
        from_attributes = True