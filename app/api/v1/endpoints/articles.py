from fastapi import APIRouter, Depends, HTTPException,Query
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user
from app.schemas.article import ArticleSchema, FeedArticle,PaginatedResponse
from app.repositories import article_repository
from typing import Optional 

router = APIRouter()


@router.get("/feed", response_model=PaginatedResponse[FeedArticle])
def get_feed(
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user),
    cursor: Optional[int] = Query(None),
    limit: int = Query(10, le=50)
):
    articles = article_repository.get_user_feed(db, current_user.id, cursor, limit)
    
    # Calcul du prochain curseur
    next_cursor = articles[-1]['id'] if articles else None
    
    return {
        "items": articles,
        "next_cursor": next_cursor
    }

@router.get("/{article_id}", response_model=ArticleSchema)
def get_article(article_id: int, db: Session = Depends(get_db)):
    article = article_repository.get_article_by_id(db, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article non trouvé")
    return article


@router.get("/", response_model=PaginatedResponse[ArticleSchema])
def get_all_articles(
    db: Session = Depends(get_db),
    cursor: Optional[int] = Query(None),
    limit: int = Query(10, le=50)
):
    articles = article_repository.get_all_articles(db, cursor, limit)
    
    # Calcul du prochain curseur
    next_cursor = articles[-1].id if articles else None
    
    return {
        "items": articles,
        "next_cursor": next_cursor
    }
