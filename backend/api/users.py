from fastapi import APIRouter, HTTPException
from pydantic_models import UserCreate, UserUpdate, User
from crud import users
from typing import List
from fastapi import Depends
from fastapi_msal import UserInfo
from api.config import msal_auth

router = APIRouter(prefix="/users")


@router.get("/", response_model=List[User])
async def get_all_users(page: int, page_size: int, current_user: UserInfo = Depends(msal_auth.scheme)):
    users_list = await users.get_all_users(page=page, page_size=page_size)
    return users_list

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int, current_user: UserInfo = Depends(msal_auth.scheme)):
    user = await users.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
