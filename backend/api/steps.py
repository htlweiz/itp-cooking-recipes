from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from pydantic_models import StepCreate, StepUpdate, Step
from crud import steps
from typing import List
from fastapi_msal import UserInfo
from api.config import msal_auth
import os

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


@router.get("/{step_id}/pic/")
async def get_picture_of_step(step_id: int, current_user: UserInfo = Depends(msal_auth.scheme)):
    return await steps.get_picture_of_step(step_id)

@router.post("/{step_id}/upload_pic/")
async def upload_picture(step_id: int, file: UploadFile = File(...), current_user: UserInfo = Depends(msal_auth.scheme)):
    allowed_extensions = {"jpg", "jpeg", "png"}
    file_extension = file.filename.split(".")[-1].lower()
    if file_extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Invalid file type. Only jpg, jpeg, and png are allowed.")
    
    file_location = f"pics/{step_id}/{file.filename}"
    os.makedirs(os.path.dirname(file_location), exist_ok=True)
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    await steps.save_step_picture_path(step_id, file_location)
    return {"info": "File uploaded successfully", "file_path": file_location}