from fastapi import APIRouter
from app.api.v1.endpoints import articles,interactions,sources,auth

api_router = APIRouter()
api_router.include_router(articles.router, prefix="/articles", tags=["articles"])
api_router.include_router(interactions.router, prefix="/interactions", tags=["interactions"])	
api_router.include_router(sources.router, prefix="/sources", tags=["sources"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
