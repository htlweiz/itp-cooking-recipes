from models import Steps
from pydantic_models import StepCreate, StepUpdate

async def create_step(step_data: StepCreate):
    step = await Steps.create(**step_data.dict())
    return step

async def get_step(step_id: int):
    step = await Steps.get(id=step_id)
    return step

async def get_all_steps():
    steps = await Steps.all()
    return steps

async def update_step(step_id: int, step_data: StepUpdate):
    step = await Steps.get(id=step_id)
    step_data_dict = step_data.dict(exclude_unset=True)
    for key, value in step_data_dict.items():
        setattr(step, key, value)
    await step.save()
    return step

async def delete_step(step_id: int):
    step = await Steps.get(id=step_id)
    await step.delete()
    return step
