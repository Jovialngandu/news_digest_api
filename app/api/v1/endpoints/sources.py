from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models.models import Source

router = APIRouter()

@router.get("/")
def get_sources(db: Session = Depends(get_db)):
    return db.query(Source).all()