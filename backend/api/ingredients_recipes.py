from fastapi import APIRouter, HTTPException, Depends
from pydantic_models import IngredientRecipeCreate, IngredientRecipeUpdate, IngredientRecipe
from crud import ingredients_recipes, users
from typing import List
from fastapi_msal import UserInfo
from api.config import msal_auth

router = APIRouter(prefix="/ingredients_recipes")

async def get_current_user(current_user: UserInfo = Depends(msal_auth.scheme)):
    try:
        user = await users.get_user(current_user.user_id)
        if not user:
            await users.create_user(username=current_user.display_name, email=current_user.preferred_username, user_id=current_user.user_id)
        if not current_user:
            raise HTTPException(status_code=401, detail="Not authenticated")
        return current_user
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="Invalid token encoding")


@router.post("/", response_model=IngredientRecipe)
async def create_ingredient_recipe(ingredient_recipe_data: IngredientRecipeCreate, current_user: UserInfo = Depends(get_current_user)):
    ingredient_recipe = await ingredients_recipes.create_ingredient_recipe(ingredient_recipe_data)
    return ingredient_recipe

@router.get("/{ingredient_recipe_id}", response_model=IngredientRecipe)
async def get_ingredient_recipe(ingredient_recipe_id: int, current_user: UserInfo = Depends(get_current_user)):
    ingredient_recipe = await ingredients_recipes.get_ingredient_recipe(ingredient_recipe_id)
    if not ingredient_recipe:
        raise HTTPException(status_code=404, detail="Ingredient recipe not found")
    return ingredient_recipe

@router.get("/", response_model=List[IngredientRecipe])
async def get_all_ingredient_recipes(page: int, page_size: int, current_user: UserInfo = Depends(get_current_user)):
    ingredient_recipes_list = await ingredients_recipes.get_all_ingredient_recipes(page=page, page_size=page_size)
    return ingredient_recipes_list

@router.put("/{ingredient_recipe_id}", response_model=IngredientRecipe)
async def update_ingredient_recipe(ingredient_recipe_id: int, ingredient_recipe_data: IngredientRecipeUpdate, current_user: UserInfo = Depends(get_current_user)):
    ingredient_recipe = await ingredients_recipes.update_ingredient_recipe(ingredient_recipe_id, ingredient_recipe_data)
    if not ingredient_recipe:
        raise HTTPException(status_code=404, detail="Ingredient recipe not found")
    return ingredient_recipe

@router.delete("/{ingredient_recipe_id}")
async def delete_ingredient_recipe(ingredient_recipe_id: int, current_user: UserInfo = Depends(get_current_user)):
    ingredient_recipe = await ingredients_recipes.delete_ingredient_recipe(ingredient_recipe_id)
    if not ingredient_recipe:
        raise HTTPException(status_code=404, detail="Ingredient recipe not found")
    return {"message": "Ingredient recipe deleted successfully"}
