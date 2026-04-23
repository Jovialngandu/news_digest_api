import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from app.core.config import settings
from app.core.database import SessionLocal
from app.repositories.article_repository import save_article
from loguru import logger


session = requests.Session()


retry_strategy = Retry(
    total=3,
    backoff_factor=1,  # Attend 1s, 2s, 4s entre les tentatives
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"]
)

adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("https://", adapter)
session.mount("http://", adapter)

def fetch_and_store_news():
    params = {
        "category": "technology",
        "lang": "fr",
        "max": 30,
        "apikey": settings.GNEWS_API_KEY
    }
    
    try:
        # On utilise session.get au lieu de requests.get
        response = session.get(settings.GNEWS_BASE_URL, params=params, timeout=2)
        response.raise_for_status()
        
        data = response.json()
        articles = data.get('articles', [])
        
        db = SessionLocal()
        try:
            for item in articles:
                save_article(db, {
                    "title": item.get('title'),
                    "url": item.get('url'),
                    "content": item.get('description'),
                    "published_at": item.get('publishedAt'),
					"image_url": item.get('image'),
                    "lang": item.get('lang'),
                    "description": item.get('description'),
                    
                }, item.get('source', {}))
        finally:
            db.close()
            
    except requests.exceptions.RequestException as e:
        # Ici, on log l'erreur proprement sans faire planter le scheduler
        logger.critical(f"Le fetch des news a échoué après retries: {e}")