from models import Ingredients
from pydantic_models import IngredientCreate, IngredientUpdate

class IngredientCrud:
    async def create_ingredient(ingredient_data: IngredientCreate, user_id: str):
        ingredient = await Ingredients.create(name=ingredient_data.name, calories=ingredient_data.calories, fat=ingredient_data.fat, carbs=ingredient_data.carbs, protein=ingredient_data.protein, related_user_id=user_id)
        return ingredient

    async def get_ingredient(ingredient_id: int):
        ingredient = await Ingredients.get(id=ingredient_id)
        return ingredient

    async def get_all_ingredients(page: int, page_size: int):
        ingredients = await Ingredients.all().offset(page * page_size).limit(page_size)
        return ingredients

    async def get_all_ingredients_of_user(page: int, page_size: int, user_id: str):
        ingredients = await Ingredients.filter(related_user_id=user_id).offset(page * page_size).limit(page_size)
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
