from pydantic import BaseModel
from typing import Optional
from app.schemas.source import SourceSchema
from app.schemas.article import ArticleSchema
from app.schemas.interaction import InteractionSchema


class ArticleSchema(BaseModel):
    id: int
    title: str
    url: str
    description: Optional[str]	
    content: Optional[str]
    published_at: Optional[str]
    image_url: Optional[str]
    lang: Optional[str]
    source: SourceSchema

    
    class Config:
        from_attributes = True

class FeedArticle(ArticleSchema):
    interaction: Optional[InteractionSchema] = None