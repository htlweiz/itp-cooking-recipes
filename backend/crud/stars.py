from models import Stars
from pydantic_models import StarsCreate, StarsUpdate
from fastapi import HTTPException

async def create_star(star_data: StarsCreate, user_id):
    try:
        star = await Stars.create(
            rating=star_data.rating,
            related_recipe_id=star_data.related_recipe_id,
            related_user_id=user_id
        )
        return star
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))

async def get_star(star_id: int):
    star = await Stars.get(id=star_id)
    return star

async def get_all_stars(page: int, page_size: int):
    stars = await Stars.all().offset(page * page_size).limit(page_size)
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

async def get_average_stars_per_recipe(recipe_id: int):
    stars = await Stars.filter(related_recipe_id=recipe_id)
    if not stars:
        return 0
    stars_count = sum([star.rating for star in stars]) / len(stars)
    return stars_count