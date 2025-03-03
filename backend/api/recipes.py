from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from pydantic_models import RecipeCreate, RecipeUpdate, Recipe
from crud import recipes, users
from typing import List
from fastapi_msal import UserInfo
from api.config import msal_auth
import os

router = APIRouter(prefix="/recipes")

async def get_current_user(current_user: UserInfo = Depends(msal_auth.scheme)):
    try:
        print(f"Preferred Username: {current_user.preferred_username}, Display Name: {current_user.display_name}, Id: {current_user.user_id}")
        user = await users.get_user(current_user.user_id)
        print(f"User: {user}")
        if not user:
            print(f"Creating user: {current_user.display_name}")
            await users.create_user(username=current_user.display_name, email=current_user.preferred_username, user_id=current_user.user_id)
            print(f"User created: {current_user.display_name}")
        if not current_user:
            raise HTTPException(status_code=401, detail="Not authenticated")
        return current_user
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="Invalid token encoding")

@router.post("/")
async def create_recipe(recipe_data: RecipeCreate, current_user: UserInfo = Depends(get_current_user)):
    print(current_user)
    recipe = await recipes.create_recipe(recipe_data, current_user.user_id)
    return recipe

@router.get("/", response_model=List[Recipe])
async def get_all_recipes(page: int, page_size: int, user_id: str = None, order_by: str = None, current_user: UserInfo = Depends(get_current_user)):
    recipes_list = await recipes.get_all_recipes(page=page, page_size=page_size, user_id=user_id, order_by=order_by)
    return recipes_list

@router.get("/{recipe_id}", response_model=Recipe)
async def get_recipe(recipe_id: int, current_user: UserInfo = Depends(get_current_user)):
    recipe = await recipes.get_recipe(recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe

@router.put("/{recipe_id}")
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

@router.get("/{recipe_id}/pic/")
async def get_picture_of_recipe(recipe_id: int, current_user: UserInfo = Depends(msal_auth.scheme)):
    return await recipes.get_picture_of_recipe(recipe_id)

@router.post("/{recipe_id}/upload_pic/")
async def upload_picture(recipe_id: int, file: UploadFile = File(...), current_user: UserInfo = Depends(get_current_user)):
    allowed_extensions = {"jpg", "jpeg", "png"}
    file_extension = file.filename.split(".")[-1].lower()
    if file_extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Invalid file type. Only jpg, jpeg, and png are allowed.")
    
    file_location = f"pics/{recipe_id}/{file.filename}"
    os.makedirs(os.path.dirname(file_location), exist_ok=True)
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    await recipes.save_recipe_picture_path(recipe_id, file_location)
    return {"info": "File uploaded successfully", "file_path": file_location}
