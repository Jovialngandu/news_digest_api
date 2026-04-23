from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user
from app.schemas.article import ArticleSchema, FeedArticle
from app.repositories import article_repository

router = APIRouter()

@router.get("/", response_model=list[ArticleSchema])
def get_all_articles(db: Session = Depends(get_db)):
    return article_repository.get_all_articles(db)

@router.get("/feed", response_model=list[FeedArticle])
def get_feed(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return article_repository.get_user_feed(db, current_user.id)

@router.get("/{article_id}", response_model=ArticleSchema)
def get_article(article_id: int, db: Session = Depends(get_db)):
    article = article_repository.get_article_by_id(db, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article non trouvé")
    return article
