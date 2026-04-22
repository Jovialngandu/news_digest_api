# app/models/models.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Enum, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum
from datetime import datetime

class ArticleStatus(enum.Enum):
    UNREAD = "unread"
    READING = "reading"
    ARCHIVED = "archived"
    TRASH = "trash"

class Source(Base):
    __tablename__ = "sources"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    url = Column(String)
    articles = relationship("Article", back_populates="source")

class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey("sources.id"))
    title = Column(String, nullable=False)
    url = Column(String, unique=True, nullable=False)
    content = Column(Text)
    image_url = Column(String)
    published_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    lang = Column(String(10),nullable=True)
    description=Column(String, nullable=True)
    
    source = relationship("Source", back_populates="articles")
    interactions = relationship("UserInteraction", back_populates="article")

class UserInteraction(Base):
    __tablename__ = "user_interactions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True) # On simplifie pour le moment
    article_id = Column(Integer, ForeignKey("articles.id"))
    
    status = Column(Enum(ArticleStatus), default=ArticleStatus.UNREAD)
    is_liked = Column(Boolean, default=False)
    note = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    article = relationship("Article", back_populates="interactions")