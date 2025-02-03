from fastapi import APIRouter, HTTPException, Depends
from pydantic_models import StepCreate, StepUpdate, Step
from crud import steps
from typing import List
from fastapi_msal import UserInfo
from api.config import msal_auth

router = APIRouter(prefix="/steps")

@router.post("/", response_model=Step)
async def create_step(step_data: StepCreate, current_user: UserInfo = Depends(msal_auth.scheme)):
    step = await steps.create_step(step_data)
    return step

@router.get("/", response_model=List[Step])
async def get_all_steps(current_user: UserInfo = Depends(msal_auth.scheme)):
    steps_list = await steps.get_all_steps()
    return steps_list

@router.get("/{step_id}", response_model=Step)
async def get_step(step_id: int, current_user: UserInfo = Depends(msal_auth.scheme)):
    step = await steps.get_step(step_id)
    if not step:
        raise HTTPException(status_code=404, detail="Step not found")
    return step

@router.put("/{step_id}", response_model=Step)
async def update_step(step_id: int, step_data: StepUpdate, current_user: UserInfo = Depends(msal_auth.scheme)):
    step = await steps.update_step(step_id, step_data)
    if not step:
        raise HTTPException(status_code=404, detail="Step not found")
    return step

@router.delete("/{step_id}")
async def delete_step(step_id: int, current_user: UserInfo = Depends(msal_auth.scheme)):
    step = await steps.delete_step(step_id)
    if not step:
        raise HTTPException(status_code=404, detail="Step not found")
    return {"message": "Step deleted successfully"}
