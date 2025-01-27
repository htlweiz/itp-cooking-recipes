from models import Stars
from pydantic_models import StarsCreate, StarsUpdate
from fastapi import HTTPException

async def create_star(star_data: StarsCreate):
    try:
        star = await Stars.create(**star_data.dict())
        return star
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))

async def get_star(star_id: int):
    star = await Stars.get(id=star_id)
    return star

async def get_all_stars():
    stars = await Stars.all()
    return stars

async def update_star(star_id: int, star_data: StarsUpdate):
    try:
        star = await Stars.get(id=star_id)
        star_data_dict = star_data.dict(exclude_unset=True)
        for key, value in star_data_dict.items():
            setattr(star, key, value)
        await star.save()
        return star
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))

async def delete_star(star_id: int):
    star = await Stars.get(id=star_id)
    await star.delete()
    return star