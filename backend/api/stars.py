from fastapi import APIRouter, HTTPException
from pydantic_models import Stars, StarsCreate, StarsUpdate
from crud import stars
from typing import List

router = APIRouter(prefix="/stars")

@router.post("/")
async def create_star(star_data: StarsCreate):
    star = await stars.create_star(star_data)
    return star

@router.get("/", response_model=List[Stars])
async def get_all_stars():
    stars_list = await stars.get_all_stars()
    return stars_list

@router.get("/{star_id}", response_model=Stars)
async def get_star(star_id: int):
    star = await stars.get_star(star_id)
    if not star:
        raise HTTPException(status_code=404, detail="Star not found")
    return star

@router.put("/{star_id}")
async def update_star(star_id: int, star_data: StarsUpdate):
    star = await stars.update_star(star_id, star_data)
    if not star:
        raise HTTPException(status_code=404, detail="Star not found")
    return star

@router.delete("/{star_id}")
async def delete_star(star_id: int):
    star = await stars.delete_star(star_id)
    if not star:
        raise HTTPException(status_code=404, detail="Star not found")
    return {"message": "Star deleted successfully"}