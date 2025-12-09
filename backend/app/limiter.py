"""
Rate limiting configuration for FastAPI application.
Uses slowapi for flexible rate limiting on specific endpoints.
"""
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

# Initialize limiter with remote address key
limiter = Limiter(key_func=get_remote_address)


def add_rate_limit_error_handler(app: FastAPI) -> None:
    """
    Add rate limit exception handler to the FastAPI application.
    
    Args:
        app: FastAPI application instance
    """
    @app.exception_handler(RateLimitExceeded)
    async def rate_limit_exception_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
        return JSONResponse(
            status_code=429,
            content={
                "detail": "Rate limit exceeded. Too many requests.",
                "retry_after": exc.detail.split("over ")[-1] if "over" in exc.detail else "1 minute"
            }
        )
