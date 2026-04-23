import time
from fastapi import Request
from loguru import logger
import sys

logger.remove()
logger.add(sys.stdout, format="{time} | {level} | {message}", level="INFO")
logger.add("logs/app.log", rotation="10 days", format="{time} | {level} | {message}", level="INFO", retention="10 days")

async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    path = request.url.path
    method = request.method
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    
    logger.info(f"{method} {path} - Status: {response.status_code} - Duration: {process_time:.4f}s")
    
    return response