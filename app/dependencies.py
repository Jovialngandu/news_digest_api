# app/dependencies.py
from app.core.database import SessionLocal
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Cette fonction sera injectée dans tes endpoints ou services
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        


def get_current_user(token: str = Depends(oauth2_scheme)):
    # Ici, tu vérifies le token dans ta DB
    # Pour l'instant, on retourne un user mocké
    return {"id": 1, "username": "test_user"}