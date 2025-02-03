from fastapi import FastAPI, Depends, Request, Response
from api.users import router as users_router
from api.steps import router as steps_router
from api.recipes import router as recipes_router
from api.ingredients_recipes import router as ingredients_recipes_router
from api.ingredients import router as ingredients_router
from api.stars import router as stars_router
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi_msal import UserInfo
from fastapi.responses import JSONResponse

from api.config import msal_auth

router = msal_auth.router


from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise
import dotenv
import os
import aiomysql
import asyncio
import uvicorn
import logging

dotenv.load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
SSH_KEY = os.getenv('SSH_KEY')

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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


app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key=SSH_KEY
)

app.include_router(msal_auth.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/users/me", response_model=UserInfo, response_model_exclude_none=True, response_model_by_alias=False)
async def read_users_me(current_user: UserInfo = Depends(msal_auth.scheme)) -> UserInfo:
    logger.info("Servus")
    return current_user

@app.post("/logout")
async def logout(response: Response, current_user: UserInfo = Depends(msal_auth.scheme)):
    response.set_cookie(key="session", value="", httponly=True)
    response.set_cookie(key="df", value="sdsdff")
    return {"message": "Logout successful"}

@app.get("/docs/oauth2-redirect")
async def oauth2_redirect(request: Request):
    logger.info(f"OAuth2 redirect request: {request.url}")
    return {"message": "OAuth2 redirect successful"}


@app.post("/token")
async def token(request: Request):
    logger.info(f"Token request: {request.url}")
    return {"message": "Token request successful"}


app.include_router(users_router, tags=["Users"])
app.include_router(steps_router, tags=["Steps"])
app.include_router(recipes_router, tags=["Recipes"])
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
