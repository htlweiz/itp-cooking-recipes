from fastapi import APIRouter, HTTPException
from pydantic_models import UserCreate, UserUpdate, User
from crud import users
from typing import List
from fastapi import Depends
from fastapi_msal import UserInfo
from api.config import msal_auth

router = APIRouter(prefix="/users")

async def get_current_user(current_user: UserInfo = Depends(msal_auth.scheme)):
    try:
        user = await users.get_user(current_user.user_id)
        if not user:
            await users.create_user(username=current_user.display_name, email=current_user.preferred_username, user_id=current_user.user_id)
        if not current_user:
            raise HTTPException(status_code=401, detail="Not authenticated")
        return current_user
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="Invalid token encoding")


@router.get("/", response_model=List[User])
async def get_all_users(page: int, page_size: int, current_user: UserInfo = Depends(get_current_user)):
    users_list = await users.get_all_users(page=page, page_size=page_size)
    return users_list

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: str, current_user: UserInfo = Depends(get_current_user)):
    user = await users.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
