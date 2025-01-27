from models import Ingredients_Recipes
from pydantic_models import IngredientRecipeCreate, IngredientRecipeUpdate

async def create_ingredient_recipe(ingredient_recipe_data: IngredientRecipeCreate):
    ingredient_recipe = await Ingredients_Recipes.create(**ingredient_recipe_data.dict())
    return ingredient_recipe

async def get_ingredient_recipe(ingredient_recipe_id: int):
    ingredient_recipe = await Ingredients_Recipes.get(id=ingredient_recipe_id)
    return ingredient_recipe

async def get_all_ingredient_recipes():
    ingredient_recipes = await Ingredients_Recipes.all()
    return ingredient_recipes

async def update_ingredient_recipe(ingredient_recipe_id: int, ingredient_recipe_data: IngredientRecipeUpdate):
    ingredient_recipe = await Ingredients_Recipes.get(id=ingredient_recipe_id)
    ingredient_recipe_data_dict = ingredient_recipe_data.dict(exclude_unset=True)
    for key, value in ingredient_recipe_data_dict.items():
        setattr(ingredient_recipe, key, value)
    await ingredient_recipe.save()
    return ingredient_recipe

async def delete_ingredient_recipe(ingredient_recipe_id: int):
    ingredient_recipe = await Ingredients_Recipes.get(id=ingredient_recipe_id)
    await ingredient_recipe.delete()
    return ingredient_recipe
