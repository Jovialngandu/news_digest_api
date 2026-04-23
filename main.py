from contextlib import asynccontextmanager
from fastapi import FastAPI,Request
from apscheduler.schedulers.background import BackgroundScheduler
from app.services.news_service import fetch_and_store_news
from app.core.database import engine, Base
from app.api.v1.route import api_router
from app.core.logger import log_requests
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
import asyncio

# Initialisation du scheduler
scheduler = BackgroundScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Démarrage de l'application...")
    Base.metadata.create_all(bind=engine)
    
    scheduler.add_job(fetch_and_store_news, 'interval', minutes=30)
    scheduler.start()
	
    asyncio.create_task(asyncio.to_thread(fetch_and_store_news))    
    yield  # C'est ici que l'application tourne
    
    print("Arrêt de l'application...")
    scheduler.shutdown()

app = FastAPI(title="News Info Center API", lifespan=lifespan)
app.include_router(api_router, prefix="/api/v1")
app.add_middleware(BaseHTTPMiddleware, dispatch=log_requests)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Erreur non gérée sur {request.url.path}: {exc}")
    
    return JSONResponse(
        status_code=500,
        content={"message": "Une erreur interne est survenue, nous avons été prévenus."},
    )

@app.get("/")
def root():
    return {"message": "API opérationnelle avec le gestionnaire lifespan"}




