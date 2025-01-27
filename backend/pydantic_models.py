from pydantic import BaseModel, EmailStr
from typing import List, Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr

class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]

class User(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode: True

class RecipeCreate(BaseModel):
    title: str
    description: Optional[str]
    related_user_id: int

class RecipeUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]

class Recipe(BaseModel):
    id: int
    title: str
    description: Optional[str]
    created_at: str
    related_user_id: int

    class Config:
        orm_mode: True


class IngredientRecipeCreate(BaseModel):
    amount: float
    unit: str
    related_recipe_id: int
    related_ingredient_id: int


class IngredientRecipeUpdate(BaseModel):
    amount: Optional[float]
    unit: Optional[str]

class IngredientRecipe(BaseModel):
    id: int
    amount: float
    unit: str
    related_recipe_id: int
    related_ingredient_id: int

    class Config:
        orm_mode: True



class IngredientCreate(BaseModel):
    name: str
    calories: float
    fat: float
    carbs: float
    protein: float

class IngredientUpdate(BaseModel):
    name: Optional[str]
    calories: Optional[float]
    fat: Optional[float]
    carbs: Optional[float]
    protein: Optional[float]

class Ingredient(BaseModel):
    id: int
    name: str
    calories: float
    fat: float
    carbs: float
    protein: float

    class Config:
        orm_mode: True

class StepCreate(BaseModel):
    step_number: int
    instruction: str
    related_recipe_id: int

class StepUpdate(BaseModel):
    step_number: Optional[int]
    instruction: Optional[str]

class Step(BaseModel):
    id: int
    step_number: int
    instruction: str
    related_recipe_id: int

    class Config:
        orm_mode: True

class StarsCreate(BaseModel):
    rating: int
    related_user_id: int
    related_recipe_id: int

class StarsUpdate(BaseModel):
    rating: Optional[int]

class Stars(BaseModel):
    id: int
    rating: int
    related_user_id: int
    related_recipe_id: int

    class Config:
        orm_mode: True