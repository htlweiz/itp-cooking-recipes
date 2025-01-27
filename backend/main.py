from fastapi import FastAPI
from api.users import router as users_router
from api.steps import router as steps_router
from api.recipes import router as recipes_router
from api.ingredients_recipes import router as ingredients_recipes_router
from api.auth import router as auth_router
from api.ingredients import router as ingredients_router
from api.stars import router as stars_router

from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise
import dotenv
import os
import aiomysql
import asyncio
import uvicorn

dotenv.load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')


async def create_database():
    conn = await aiomysql.connect(user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'), host='db')
    async with conn.cursor() as cursor:
        try:
            await cursor.execute(f'CREATE DATABASE `{os.getenv("DB_NAME")}`')
        except aiomysql.Error as e:
            if e.args[0] != 1007:
                raise
    conn.close()

async def init():
    await create_database()
    await Tortoise.init(
        db_url=DATABASE_URL,
        modules={'models': ["models"]},
    )
    await Tortoise.generate_schemas(safe=True)


app = FastAPI(
    title="Your API",
    description="API description",
    version="1.0.0",
    openapi_tags=[{"name": "example", "description": "Example endpoints"}],
    swagger_ui_oauth2_redirect_url="/oauth2-redirect", 
    swagger_ui_parameters={
        "oauth2RedirectUrl": "https://localhost:8002/oauth2-redirect", 
    },
)

app.include_router(users_router, tags=["Users"])
app.include_router(steps_router, tags=["Steps"])
app.include_router(recipes_router, tags=["Recipes"])
app.include_router(ingredients_router, tags=["Ingredients"])
app.include_router(auth_router, tags=["Auth"])
app.include_router(ingredients_router, tags=["Ingredients"])
app.include_router(ingredients_recipes_router, tags=["Ingredients_Recipes"])
app.include_router(stars_router, tags=["Stars"])

register_tortoise(
    app,
    db_url=DATABASE_URL,
    modules={'models': ['models']},
    generate_schemas=True,
    add_exception_handlers=True,
)

if __name__ == "__main__":
    asyncio.run(init())
    uvicorn.run(app, host="0.0.0.0", port=8002)
