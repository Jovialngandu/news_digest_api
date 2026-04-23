from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.repositories import source_repository

router = APIRouter()

@router.get("/")
def get_sources(db: Session = Depends(get_db)):
    # On délègue tout au repository
    return source_repository.get_all_sources(db)