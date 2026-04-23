from fastapi import APIRouter, Depends, HTTPException, status, Header
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user
from app.repositories import user_repository
from app.schemas.user import UserCreate, UserRead
from app.schemas.token import Token
from app.core.security import (
    create_access_token, 
    create_refresh_token, 
    verify_password
)
from app.core.config import settings
from jose import jwt
from app.schemas.user import UserRegistrationResponse 

router = APIRouter()

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = user_repository.get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")
    
    # Payload commun
    token_data = {"sub": user.email}
    
    return {
        "access_token": create_access_token(token_data),
        "refresh_token": create_refresh_token(token_data),
        "token_type": "bearer"
    }

@router.post("/refresh")
def refresh_token(refresh_token: str = Header(...), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Jeton invalide")
            
        email = payload.get("sub")
        user = user_repository.get_user_by_email(db, email)
        if not user:
            raise HTTPException(status_code=401, detail="Utilisateur non trouvé")
            
        new_access_token = create_access_token({"sub": email})
        
        return {"access_token": new_access_token, "token_type": "bearer"}
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expiré")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Refresh token invalide")
    

@router.post("/register", response_model=UserRegistrationResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = user_repository.get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email déjà utilisé")
    
    new_user = user_repository.create_user(db, user_data.model_dump())
    
    token_data = {"sub": new_user.email}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)
    
    return {
        "user": new_user,
        "tokens": {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    }

@router.get("/me", response_model=UserRead)
def read_current_user(current_user: UserRead = Depends(get_current_user)):
	return current_user