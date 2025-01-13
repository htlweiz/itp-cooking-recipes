from fastapi import APIRouter, HTTPException
from pydantic_models import IngredientCreate, IngredientUpdate, Ingredient
from crud import ingredients
from typing import List

router = APIRouter(prefix="/ingredients")

@router.post("/", response_model=Ingredient)
async def create_ingredient(ingredient_data: IngredientCreate):
    ingredient = await ingredients.create_ingredient(ingredient_data)
    return ingredient

@router.get("/{ingredient_id}", response_model=Ingredient)
async def get_ingredient(ingredient_id: int):
    ingredient = await ingredients.get_ingredient(ingredient_id)
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return ingredient

@router.get("/", response_model=List[Ingredient])
async def get_all_ingredients():
    ingredients_list = await ingredients.get_all_ingredients()
    return ingredients_list

@router.put("/{ingredient_id}", response_model=Ingredient)
async def update_ingredient(ingredient_id: int, ingredient_data: IngredientUpdate):
    ingredient = await ingredients.update_ingredient(ingredient_id, ingredient_data)
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return ingredient

@router.delete("/{ingredient_id}")
async def delete_ingredient(ingredient_id: int):
    ingredient = await ingredients.delete_ingredient(ingredient_id)
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return {"message": "Ingredient deleted successfully"}
