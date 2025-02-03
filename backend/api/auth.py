import uvicorn
from fastapi import FastAPI, Depends, APIRouter
from starlette.middleware.sessions import SessionMiddleware
from fastapi_msal import UserInfo
from api.config import msal_auth

router = msal_auth.router


@router.get("/users/me", response_model=UserInfo, response_model_exclude_none=True, response_model_by_alias=False)
async def read_users_me(current_user: UserInfo = Depends(msal_auth.scheme)) -> UserInfo:
    return current_user

@router.get("/logout")
async def logout(current_user: UserInfo = Depends(msal_auth.scheme)):
    msal_auth.logout(current_user)
    return {"message": "Logged out successfully"}