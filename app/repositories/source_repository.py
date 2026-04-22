from sqlalchemy.orm import Session
from app.models.models import Source

def get_all_sources(db: Session):
    return db.query(Source).all()