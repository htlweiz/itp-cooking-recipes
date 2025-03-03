from models import Users
from pydantic_models import UserCreate, UserUpdate

async def create_user(user_id: str, username: str, email: str):
    user = await Users.create(id=user_id, username=username, email=email)
    return user

async def get_user(user_id: int):
    try:
        user = await Users.get(id=user_id)
        return user
    except:
        return None

async def update_user(user_id: int, user_data: UserUpdate):
    user = await Users.get(id=user_id)
    user_data_dict = user_data.dict(exclude_unset=True)
    for key, value in user_data_dict.items():
        setattr(user, key, value)
    await user.save()
    return user

async def delete_user(user_id: int):
    user = await Users.get(id=user_id)
    await user.delete()
    return user

async def get_all_users(page: int, page_size: int):
    users = await Users.all().offset(page * page_size).limit(page_size)
    return users
