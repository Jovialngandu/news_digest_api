from pydantic import BaseModel, EmailStr
from app.schemas.token import Token


class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str 

class UserRead(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True # Important pour SQLAlchemy
        
class UserRegistrationResponse(BaseModel):
    user: UserRead
    tokens: Token