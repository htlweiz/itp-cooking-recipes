from fastapi import APIRouter, HTTPException
from pydantic_models import UserCreate, UserUpdate, User
from crud import users
from typing import List

router = APIRouter(prefix="/users")

@router.post("/", response_model=User)
async def create_user(user_data: UserCreate):
    user = await users.create_user(user_data)
    return user

@router.get("/", response_model=List[User])
async def get_all_users():
    users_list = await users.get_all_users()
    return users_list

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int):
    user = await users.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=User)
async def update_user(user_id: int, user_data: UserUpdate):
    user = await users.update_user(user_id, user_data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{user_id}")
async def delete_user(user_id: int):
    user = await users.delete_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
