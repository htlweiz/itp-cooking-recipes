from models import Ingredients
from pydantic_models import IngredientCreate, IngredientUpdate

async def create_ingredient(ingredient_data: IngredientCreate):
    ingredient = await Ingredients.create(**ingredient_data.dict())
    return ingredient

async def get_ingredient(ingredient_id: int):
    ingredient = await Ingredients.get(id=ingredient_id)
    return ingredient

async def get_all_ingredients():
    ingredients = await Ingredients.all()
    return ingredients

async def update_ingredient(ingredient_id: int, ingredient_data: IngredientUpdate):
    ingredient = await Ingredients.get(id=ingredient_id)
    ingredient_data_dict = ingredient_data.dict(exclude_unset=True)
    for key, value in ingredient_data_dict.items():
        setattr(ingredient, key, value)
    await ingredient.save()
    return ingredient

async def delete_ingredient(ingredient_id: int):
    ingredient = await Ingredients.get(id=ingredient_id)
    await ingredient.delete()
    return ingredient
