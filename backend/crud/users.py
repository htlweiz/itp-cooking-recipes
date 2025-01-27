from models import Users
from pydantic_models import UserCreate, UserUpdate

async def create_user(user_data: UserCreate):
    print(user_data)
    print("\n\n\n\n\n")
    user = await Users.create(username=user_data.username, email=user_data.email)
    return user

async def get_user(user_id: int):
    user = await Users.get(id=user_id)
    return user

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

async def get_all_users():
    users = await Users.all()
    return users
