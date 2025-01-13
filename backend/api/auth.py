from fastapi import APIRouter, Depends, HTTPException
from fastapi.security.oauth2 import OAuth2AuthorizationCodeBearer
import httpx
from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

router = APIRouter()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
AUTHORIZATION_URL = os.getenv("AUTHORIZATION_URL")
TOKEN_URL = os.getenv("TOKEN_URL")
SCOPE = os.getenv("SCOPE")
REDIRECT_URI = os.getenv("REDIRECT_URI")
TENANT_ID = os.getenv("TENANT_ID")

if not all([CLIENT_ID, CLIENT_SECRET, AUTHORIZATION_URL, TOKEN_URL, SCOPE, REDIRECT_URI, TENANT_ID]):
    raise ValueError("One or more environment variables are missing or invalid")

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=AUTHORIZATION_URL,
    tokenUrl=TOKEN_URL,
    scopes={"User.Read": "Read user information"}
)

@router.get("/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    token_url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
    
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": token,
        "scope": SCOPE,
        "redirect_uri": REDIRECT_URI
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, data=data)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch user info")
        user_data = response.json()

        print(user_data)
        return user_data


