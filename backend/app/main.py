from fastapi import FastAPI, Response, Request
from fastapi.responses import JSONResponse
from app.routes import auth
from fastapi.middleware.cors import CORSMiddleware
from . import database

# Main app instance
app = FastAPI()

# CORS handling
# Origins of requests
origins = [
    "http://localhost:5173",   
    "http://127.0.0.1:5173",
]
# Adding middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*']
)

# Routes
app.include_router(auth.router)
app.include_router(database.router)

# Index route
@app.get('/')
def start_page():
    return {"message":"working"}
@app.exception_handler(Exception)
async def all_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"}
    )



if __name__ == "__main__":
    pass