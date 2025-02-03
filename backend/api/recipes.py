from fastapi import APIRouter, HTTPException, Depends
from pydantic_models import RecipeCreate, RecipeUpdate, Recipe
from crud import recipes
from typing import List
from fastapi_msal import UserInfo
from api.config import msal_auth

router = APIRouter(prefix="/recipes")

def get_current_user(current_user: UserInfo = Depends(msal_auth.scheme)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return current_user

@router.post("/", response_model=Recipe)
async def create_recipe(recipe_data: RecipeCreate, current_user: UserInfo = Depends(get_current_user)):
    recipe = await recipes.create_recipe(recipe_data)
    return recipe

@router.get("/", response_model=List[Recipe])
async def get_all_recipes(current_user: UserInfo = Depends(get_current_user)):
    recipes_list = await recipes.get_all_recipes()
    return recipes_list

@router.get("/{recipe_id}", response_model=Recipe)
async def get_recipe(recipe_id: int, current_user: UserInfo = Depends(get_current_user)):
    recipe = await recipes.get_recipe(recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe

@router.put("/{recipe_id}", response_model=Recipe)
async def update_recipe(recipe_id: int, recipe_data: RecipeUpdate, current_user: UserInfo = Depends(get_current_user)):
    recipe = await recipes.update_recipe(recipe_id, recipe_data)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe

@router.delete("/{recipe_id}")
async def delete_recipe(recipe_id: int, current_user: UserInfo = Depends(get_current_user)):
    recipe = await recipes.delete_recipe(recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return {"message": "Recipe deleted successfully"}
