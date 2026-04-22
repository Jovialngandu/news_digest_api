from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user
from app.models.models import UserInteraction
from app.schemas.interaction import InteractionSchema, InteractionUpdate

router = APIRouter()

def get_or_create_interaction(db: Session, user_id: int, article_id: int):
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

@router.patch("/{article_id}", response_model=InteractionSchema)
def update_interaction(
    article_id: int, 
    data: InteractionUpdate,
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    interaction = get_or_create_interaction(db, current_user["id"], article_id)
    
    # Mise à jour dynamique des champs fournis
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(interaction, key, value)
        
    db.commit()
    db.refresh(interaction)
    return interaction

@router.get("/", response_model=list[InteractionSchema])
def get_all_my_interactions(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return db.query(UserInteraction).filter(UserInteraction.user_id == current_user["id"]).all()