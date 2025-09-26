from fastapi import FastAPI
from app.routes import auth
app = FastAPI()

app.include_router(auth.router)

@app.get('/')
def start_page():
    return {"message":"working"}



if __name__ == "__main__":
    pass