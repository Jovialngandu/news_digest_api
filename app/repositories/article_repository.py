from sqlalchemy.orm import Session
from app.models.models import Article, Source, UserInteraction
from datetime import datetime


def save_article(db: Session, article_data: dict, source_data: dict): # Renommé en source_data
    existing_article = db.query(Article).filter(Article.url == article_data['url']).first()
    
    if existing_article:
        return existing_article 
    
    source_obj = db.query(Source).filter(Source.name == source_data.get('name')).first()
  
    if not source_obj:
        source_obj = Source(name=source_data.get('name'), url=source_data.get('url', ''))
        db.add(source_obj)
        db.commit()
        db.refresh(source_obj)

    raw_date = article_data.get('published_at')
    published_date = None
    if raw_date:
        published_date = datetime.fromisoformat(raw_date.replace('Z', '+00:00'))
            
		    
    new_article = Article(
        title=article_data['title'],
        url=article_data['url'],
        content=article_data.get('content', ''),
        source_id=source_obj.id, # Utilisation de l'objet trouvé ou créé
        published_at=published_date,
        image_url=article_data.get('image_url'),
        description=article_data.get('description', ''),
        lang=article_data.get('lang', '')
    )
    db.add(new_article)
    db.commit()
    return new_article

def get_all_articles(db: Session):
    return db.query(Article).all()

def get_article_by_id(db: Session, article_id: int):
    return db.query(Article).filter(Article.id == article_id).first()

def get_user_feed(db: Session, user_id: int):
    # Logique pour construire le feed
    articles = db.query(Article).all()
    user_interactions = db.query(UserInteraction).filter(
        UserInteraction.user_id == user_id
    ).all()
    
    interaction_map = {i.article_id: i for i in user_interactions}
    
    feed_data = []
    for article in articles:
        feed_data.append({
            **article.__dict__,
            "source": article.source,
            "interaction": interaction_map.get(article.id)
        })
    return feed_data