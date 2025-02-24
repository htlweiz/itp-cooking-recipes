from fastapi import APIRouter, HTTPException, Depends
from pydantic_models import IngredientCreate, IngredientUpdate, Ingredient
from crud import ingredients
from typing import List
from fastapi_msal import UserInfo
from api.config import msal_auth

router = APIRouter(prefix="/ingredients")

@router.post("/", response_model=Ingredient)
async def create_ingredient(ingredient_data: IngredientCreate, current_user: UserInfo = Depends(msal_auth.scheme)):
    ingredient = await ingredients.create_ingredient(ingredient_data, current_user.user_id)
    return ingredient

@router.get("/{ingredient_id}", response_model=Ingredient)
async def get_ingredient(ingredient_id: int, current_user: UserInfo = Depends(msal_auth.scheme)):
    ingredient = await ingredients.get_ingredient(ingredient_id)
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return ingredient

@router.get("/", response_model=List[Ingredient])
async def get_all_ingredients(current_user: UserInfo = Depends(msal_auth.scheme)):
    ingredients_list = await ingredients.get_all_ingredients()
    return ingredients_list

@router.put("/{ingredient_id}", response_model=Ingredient)
async def update_ingredient(ingredient_id: int, ingredient_data: IngredientUpdate, current_user: UserInfo = Depends(msal_auth.scheme)):
    ingredient = await ingredients.update_ingredient(ingredient_id, ingredient_data)
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return ingredient

@router.delete("/{ingredient_id}")
async def delete_ingredient(ingredient_id: int, current_user: UserInfo = Depends(msal_auth.scheme)):
    ingredient = await ingredients.delete_ingredient(ingredient_id)
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return {"message": "Ingredient deleted successfully"}
