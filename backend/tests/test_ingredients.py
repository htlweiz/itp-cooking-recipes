import json
from fastapi import status
from fastapi_msal import UserInfo

from crud.ingredients import IngredientCrud
from api.ingredients import Security


def test_get_ingredients(test_app, monkeypatch):
    print("test_get_todos called")

    test_data = [
        {
            "id": 1,
            "name": "Chicken Breast",
            "calories": 165.0,
            "fat": 3.6,
            "carbs": 0.0,
            "protein": 31.0,
            "related_user": "test_user_id"
        },
        {
            "id": 2,
            "name": "Broccoli",
            "calories": 55.0,
            "fat": 0.6,
            "carbs": 11.2,
            "protein": 3.7,
            "related_user": "test_user_id"
        }
    ]

    async def mock_get(page: int, page_size: int):
        print("mock_get called")
        return test_data

    def mock_auth():
        print("mock_auth called")
        return UserInfo(
            preferred_username="test_user",
            display_name="Test User",
            user_id="test_user_id"
        )
    monkeypatch.setattr(Security, "auth", mock_auth)
    monkeypatch.setattr(IngredientCrud, "get_all_ingredients", mock_get)
    print("Mocked get_all_ingredients")


    response = test_app.get("/ingredients/?page=1&page_size=10")

    print("Response:", response.json())

    assert response.status_code == status.HTTP_200_OK