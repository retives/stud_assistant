from fastapi import FastAPI, Response, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.config import SYSTEM_ID, SYSTEM_PASSWORD
from app.database import SessionLocal
from app.models import User
from app.routes import auth, chat
from fastapi.middleware.cors import CORSMiddleware
from uuid import UUID
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
app.include_router(chat.router)
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

@app.on_event("startup")
def create_ai_user():
    db: Session = SessionLocal()
    try:
        ai_user = db.query(User).filter_by(id=SYSTEM_ID).first()
        if not ai_user:
            ai_user = User(
                id=SYSTEM_ID,
                username="assistant",
                password=SYSTEM_PASSWORD,
                email='{SYSTEM_ID}@stud_assistant.com',
            )
            db.add(ai_user)
            db.commit()
            print("✅ AI user created")
        else:
            print("✅ AI user already exists")
    finally:
        db.close()


if __name__ == "__main__":
    pass