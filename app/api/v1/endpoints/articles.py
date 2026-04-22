from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models.models import Article
from app.schemas.article import ArticleSchema,FeedArticle
from app.dependencies import get_current_user
from app.models.models import UserInteraction

router = APIRouter()

@router.get("/", response_model=list[ArticleSchema])
def get_all_articles(db: Session = Depends(get_db)):
    return db.query(Article).all()

@router.get("/{article_id}", response_model=ArticleSchema)
def get_article(article_id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article non trouvé")
    return article


@router.get("/feed", response_model=list[FeedArticle])
def get_feed(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    articles = db.query(Article).all()    
    user_interactions = db.query(UserInteraction).filter(
        UserInteraction.user_id == current_user["id"]
    ).all()
    
    interaction_map = {i.article_id: i for i in user_interactions}
    
    feed = []
    for article in articles:
        feed.append(FeedArticle(
            **article.__dict__,
            source=article.source, 
            interaction=interaction_map.get(article.id)
        ))
    return feed