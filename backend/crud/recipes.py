from models import Recipes, Users, Ingredients
from pydantic_models import RecipeCreate, RecipeUpdate
from fastapi.responses import FileResponse
from crud.stars import get_average_stars_per_recipe

async def create_recipe(recipe_data: RecipeCreate, current_user_id: str):
    user = await Users.get(id=current_user_id)
    if not user:
        raise ValueError("User does not exist")
    recipe = await Recipes.create(
        title=recipe_data.title,
        description=recipe_data.description,
        related_user_id=current_user_id
    )
    recipe_dict = {
        "id": recipe.id,
        "title": recipe.title,
        "description": recipe.description,
        "created_at": recipe.created_at.isoformat(),
        "related_user_id": current_user_id
    }
    return recipe_dict

async def get_recipe(recipe_id: int):
    recipe = await Recipes.get(id=recipe_id).prefetch_related("ingredient_recipes").prefetch_related("steps")
    ingredients_recipe = await recipe.ingredient_recipes.all().prefetch_related("related_ingredient")
    steps_list = [
        {
            "id": step.id,
            "title": step.title,
            "step_number": step.step_number,
            "instruction": step.instruction
        }
        for step in recipe.steps
    ]
    ingredients_list = [
        {
            "id": ingredient_recipe.id,
            "name": ingredient_recipe.related_ingredient.name,
            "amount": ingredient_recipe.amount,
            "unit": ingredient_recipe.unit,
            "carbs": ingredient_recipe.related_ingredient.carbs,
            "fat": ingredient_recipe.related_ingredient.fat,
            "calories": ingredient_recipe.related_ingredient.calories,
            "protein": ingredient_recipe.related_ingredient.protein
        }
        for ingredient_recipe in ingredients_recipe
    ]
    recipe_dict = {
        "id": recipe.id,
        "title": recipe.title,
        "description": recipe.description,
        "created_at": recipe.created_at.isoformat(),
        "related_user_id": recipe.related_user_id,
        "ingredients": ingredients_list,
        "steps": steps_list,
        "average_stars": await get_average_stars_per_recipe(recipe_id=recipe.id)
    }
    return recipe_dict

async def get_all_recipes():
    recipes = await Recipes.all().prefetch_related("ingredient_recipes").prefetch_related("steps")
    recipes_list = []
    for recipe in recipes:
        ingredients_recipe = await recipe.ingredient_recipes.all().prefetch_related("related_ingredient")
        steps_list = [
            {
                "id": step.id,
                "step_number": step.step_number,
                "title": step.title,
                "instruction": step.instruction
            }
            for step in recipe.steps
            ]
        ingredients_list = [
            {
                "id": ingredient_recipe.id,
                "name": ingredient_recipe.related_ingredient.name,
                "amount": ingredient_recipe.amount,
                "unit": ingredient_recipe.unit,
                "carbs": ingredient_recipe.related_ingredient.carbs,
                "fat": ingredient_recipe.related_ingredient.fat,
                "calories": ingredient_recipe.related_ingredient.calories,
                "protein": ingredient_recipe.related_ingredient.protein
            }
            for ingredient_recipe in ingredients_recipe
        ]
        recipe_dict = {
            "id": recipe.id,
            "title": recipe.title,
            "description": recipe.description,
            "created_at": recipe.created_at.isoformat(),
            "related_user_id": recipe.related_user_id,
            "ingredients": ingredients_list,
            "steps": steps_list,
            "average_stars": await get_average_stars_per_recipe(recipe_id=recipe.id)
        }
        recipes_list.append(recipe_dict)
    return recipes_list

async def update_recipe(recipe_id: int, recipe_data: RecipeUpdate):
    recipe = await Recipes.get(id=recipe_id)
    recipe_data_dict = recipe_data.dict(exclude_unset=True)
    for key, value in recipe_data_dict.items():
        setattr(recipe, key, value)
    await recipe.save()
    recipe_dict = {
        "id": recipe.id,
        "title": recipe.title,
        "description": recipe.description,
        "created_at": recipe.created_at.isoformat(),
        "related_user_id": recipe.related_user_id
    }
    return recipe_dict

async def delete_recipe(recipe_id: int):
    recipe = await Recipes.get(id=recipe_id)
    await recipe.delete()
    return recipe

async def get_picture_of_recipe(recipe_id: int):
    recipe = await Recipes.get(id=recipe_id)
    if recipe.pic_path is None:
        return None
    return FileResponse(recipe.pic_path)

async def save_recipe_picture_path(recipe_id: int, pic_path: str):
    recipe = await Recipes.get(id=recipe_id)
    await recipe.update_pic_path(pic_path)
    return recipe