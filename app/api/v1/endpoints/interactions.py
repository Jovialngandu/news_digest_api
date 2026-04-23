from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user
from app.schemas.interaction import InteractionSchema, InteractionUpdate
from app.repositories import interaction_repository

router = APIRouter()

@router.patch("/{article_id}", response_model=InteractionSchema)
def update_interaction(
    article_id: int, 
    data: InteractionUpdate,
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    # On transforme le schema en dict propre
    update_data = data.model_dump(exclude_unset=True)
    
    # On délègue au repository
    return interaction_repository.update(db, current_user.id, article_id, update_data)

@router.get("/", response_model=list[InteractionSchema])
def get_all_my_interactions(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    # On délègue au repository
    return interaction_repository.get_by_user(db, current_user.id)