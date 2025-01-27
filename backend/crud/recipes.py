from models import Recipes
from pydantic_models import RecipeCreate, RecipeUpdate

async def create_recipe(recipe_data: RecipeCreate):
    recipe = await Recipes.create(
        title=recipe_data.title,
        description=recipe_data.description,
        related_user_id=recipe_data.related_user_id
    )
    recipe_dict = {
        "id": recipe.id,
        "title": recipe.title,
        "description": recipe.description,
        "created_at": recipe.created_at.isoformat(),
        "related_user_id": recipe.related_user_id
    }
    return recipe_dict

async def get_recipe(recipe_id: int):
    recipe = await Recipes.get(id=recipe_id)
    recipe_dict = {
        "id": recipe.id,
        "title": recipe.title,
        "description": recipe.description,
        "created_at": recipe.created_at.isoformat(),
        "related_user_id": recipe.related_user_id
    }
    return recipe_dict

async def get_all_recipes():
    recipes = await Recipes.all()
    recipes_list = []
    for recipe in recipes:
        recipe_dict = {
            "id": recipe.id,
            "title": recipe.title,
            "description": recipe.description,
            "created_at": recipe.created_at.isoformat(),
            "related_user_id": recipe.related_user_id
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
