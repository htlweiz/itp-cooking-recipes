from fastapi import APIRouter, HTTPException, Depends
from pydantic_models import IngredientCreate, IngredientUpdate, Ingredient
from crud.ingredients import IngredientCrud
from crud import users
from typing import List
from fastapi_msal import UserInfo
from api.config import msal_auth

router = APIRouter(prefix="/ingredients")

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


class Security:
    def auth(current_user: UserInfo = Depends(get_current_user)):
        print(f"Preferred Username: {current_user.preferred_username}, Display Name: {current_user.display_name}, Id: {current_user.user_id}")
        print("\n\nHello")
        return current_user

@router.post("/", response_model=Ingredient)
async def create_ingredient(ingredient_data: IngredientCreate, current_user: UserInfo = Depends(Security.auth)):
    ingredient = await IngredientCrud.create_ingredient(ingredient_data, current_user.user_id)
    return ingredient

@router.get("/{ingredient_id}", response_model=Ingredient)
async def get_ingredient(ingredient_id: int, current_user: UserInfo = Depends(Security.auth)):
    ingredient = await IngredientCrud.get_ingredient(ingredient_id)
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return ingredient

@router.get("/", response_model=List[Ingredient])
async def get_all_ingredients(page: int, page_size: int, current_user: UserInfo = Depends(Security.auth)):
    ingredients_list = await IngredientCrud.get_all_ingredients(page=page, page_size=page_size)
    return ingredients_list

@router.get("/self/", response_model=List[Ingredient])
async def get_all_ingredients(page: int, page_size: int, current_user: UserInfo = Depends(Security.auth)):
    ingredients_list = await IngredientCrud.get_all_ingredients_of_user(page=page, page_size=page_size, user_id=current_user.user_id)
    return ingredients_list

@router.put("/{ingredient_id}", response_model=Ingredient)
async def update_ingredient(ingredient_id: int, ingredient_data: IngredientUpdate, current_user: UserInfo = Depends(Security.auth)):
    ingredient = await IngredientCrud.update_ingredient(ingredient_id, ingredient_data)
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return ingredient

@router.delete("/{ingredient_id}")
async def delete_ingredient(ingredient_id: int, current_user: UserInfo = Depends(Security.auth)):
    ingredient = await IngredientCrud.delete_ingredient(ingredient_id)
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return {"message": "Ingredient deleted successfully"}
