from fastapi import FastAPI, Depends
from app.api.endpoints import signup


app = FastAPI()
app.include_router(signup.router) 



@app.get('/')
async def root():
    return {"message":"hello"}

