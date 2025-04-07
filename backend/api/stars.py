from fastapi import APIRouter, HTTPException, Depends
from pydantic_models import Stars, StarsCreate, StarsUpdate
from crud import stars, users
from typing import List
from fastapi_msal import UserInfo
from api.config import msal_auth

router = APIRouter(prefix="/stars")

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

@router.post("/")
async def create_star(star_data: StarsCreate, current_user: UserInfo = Depends(get_current_user)):
    star = await stars.create_star(star_data, current_user.user_id)
    return star

@router.get("/", response_model=List[Stars])
async def get_all_stars(page: int, page_size: int, current_user: UserInfo = Depends(get_current_user)):
    stars_list = await stars.get_all_stars(page=page, page_size=page_size)
    return stars_list

@router.get("/{star_id}", response_model=Stars)
async def get_star(star_id: int, current_user: UserInfo = Depends(get_current_user)):
    star = await stars.get_star(star_id)
    if not star:
        raise HTTPException(status_code=404, detail="Star not found")
    return star

@router.put("/{star_id}")
async def update_star(star_id: int, star_data: StarsUpdate, current_user: UserInfo = Depends(get_current_user)):
    star = await stars.update_star(star_id, star_data)
    if not star:
        raise HTTPException(status_code=404, detail="Star not found")
    return star

@router.delete("/{star_id}")
async def delete_star(star_id: int, current_user: UserInfo = Depends(get_current_user)):
    star = await stars.delete_star(star_id)
    if not star:
        raise HTTPException(status_code=404, detail="Star not found")
    return {"message": "Star deleted successfully"}

@router.get("/{recipe_id}/stars", response_model=float)
async def get_average_stars_per_recipe(recipe_id: int, current_user: UserInfo = Depends(get_current_user)):
    stars_count = await stars.get_average_stars_per_recipe(recipe_id)
    return stars_count