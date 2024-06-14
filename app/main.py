from fastapi import FastAPI,HTTPException
from starlette.requests import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import time
from . import models
from .database import engine
from .routes import users,recipe

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

#configuration of api rate limit
rate_limit_data = dict()
def rate_limit(identifier: str, rate: int, per_seconds: int) -> bool:
    current_time = time.time()
    request_timestamps = rate_limit_data.get(identifier, [])
    rate_limit_data[identifier] = [
        timestamp for timestamp in request_timestamps
        if current_time - timestamp < per_seconds
    ]
    if len(rate_limit_data[identifier]) < rate:
        rate_limit_data[identifier].append(current_time)
        return True
    return False

#custom middleware to rate limit of api request
async def rate_limit_middleware(request: Request, call_next, rate: int = 5, per_seconds: int = 60):
    identifier = request.client.host  # Using client's IP address for rate limiting
    if not rate_limit(identifier, rate, per_seconds):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    response = await call_next(request)
    return response

#register custom middleware
app.add_middleware(BaseHTTPMiddleware, dispatch=rate_limit_middleware)

#register all routes
app.include_router(users.router,prefix="/user")
app.include_router(recipe.router, prefix="/recipe")

#added global exception handler
@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": f"An error occurred: {str(exc)}"},
    )
