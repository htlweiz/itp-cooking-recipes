from fastapi import APIRouter, HTTPException
from pydantic_models import RecipeCreate, RecipeUpdate, Recipe
from crud import recipes
from typing import List

router = APIRouter(prefix="/recipes")

@router.post("/", response_model=Recipe)
async def create_recipe(recipe_data: RecipeCreate):
    recipe = await recipes.create_recipe(recipe_data)
    return recipe

@router.get("/", response_model=List[Recipe])
async def get_all_recipes():
    recipes_list = await recipes.get_all_recipes()
    return recipes_list

@router.get("/{recipe_id}", response_model=Recipe)
async def get_recipe(recipe_id: int):
    recipe = await recipes.get_recipe(recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe

@router.put("/{recipe_id}", response_model=Recipe)
async def update_recipe(recipe_id: int, recipe_data: RecipeUpdate):
    recipe = await recipes.update_recipe(recipe_id, recipe_data)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe

@router.delete("/{recipe_id}")
async def delete_recipe(recipe_id: int):
    recipe = await recipes.delete_recipe(recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return {"message": "Recipe deleted successfully"}
