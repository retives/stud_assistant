from fastapi import FastAPI, Depends
from app.api.endpoints import auth
from fastapi_users import FastAPIUsers
from app.core.models import User
from app.core.users import get_user_manager, auth_backend

import uuid
app = FastAPI()
# app.include_router(signup.router) 

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)
# To add verification add requires_verification=True to get_auth_router()
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/database',
    tags=["auth"],
)


current_active_user = fastapi_users.current_user(active=True)
@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}

