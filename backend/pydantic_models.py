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

class IngredientCreate(BaseModel):
    name: str
    amount: float
    unit: str
    related_recipe_id: int

class IngredientUpdate(BaseModel):
    name: Optional[str]
    amount: Optional[float]
    unit: Optional[str]

class Ingredient(BaseModel):
    id: int
    name: str
    amount: float
    unit: str
    related_recipe_id: int

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
