from sqlalchemy.orm import Session
from app.models.models import UserInteraction

def get_or_create(db: Session, user_id: int, article_id: int):
    interaction = db.query(UserInteraction).filter(
        UserInteraction.article_id == article_id,
        UserInteraction.user_id == user_id
    ).first()
    
    if not interaction:
        interaction = UserInteraction(user_id=user_id, article_id=article_id)
        db.add(interaction)
        db.commit()
        db.refresh(interaction)
    return interaction

def update(db: Session, user_id: int, article_id: int, update_data: dict):
    interaction = get_or_create(db, user_id, article_id)
    
    # Mise à jour dynamique
    for key, value in update_data.items():
        setattr(interaction, key, value)
        
    db.commit()
    db.refresh(interaction)
    return interaction

def get_by_user(db: Session, user_id: int):
    return db.query(UserInteraction).filter(UserInteraction.user_id == user_id).all()