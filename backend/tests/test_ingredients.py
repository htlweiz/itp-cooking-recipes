import json
import pytest
from fastapi import status
from fastapi_msal import UserInfo

from crud.ingredients import IngredientCrud
from api.ingredients import Security


@pytest.fixture
def mock_user(monkeypatch):
    def mock_auth():
        return UserInfo(
            preferred_username="test_user",
            display_name="Test User",
            user_id="test_user_id"
        )
    monkeypatch.setattr(Security, "auth", mock_auth)


def test_get_ingredients(test_app, monkeypatch, mock_user):
    test_data = [
        {
            "id": 1,
            "name": "Chicken Breast",
            "calories": 165.0,
            "fat": 3.6,
            "carbs": 0.0,
            "protein": 31.0
        },
        {
            "id": 2,
            "name": "Broccoli",
            "calories": 55.0,
            "fat": 0.6,
            "carbs": 11.2,
            "protein": 3.7
        }
    ]

    async def mock_get(page: int, page_size: int):
        return test_data

    monkeypatch.setattr(IngredientCrud, "get_all_ingredients", mock_get)

    response = test_app.get("/ingredients/?page=1&page_size=10")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == test_data


def test_get_ingredient_by_id(test_app, monkeypatch, mock_user):
    test_item = {
        "id": 1,
        "name": "Chicken Breast",
        "calories": 165.0,
        "fat": 3.6,
        "carbs": 0.0,
        "protein": 31.0
    }

    async def mock_get(ingredient_id: int):
        return test_item

    monkeypatch.setattr(IngredientCrud, "get_ingredient", mock_get)

    response = test_app.get("/ingredients/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == test_item


def test_get_ingredient_by_id_not_found(test_app, monkeypatch, mock_user):
    async def mock_get(ingredient_id: int):
        return None

    monkeypatch.setattr(IngredientCrud, "get_ingredient", mock_get)

    response = test_app.get("/ingredients/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Ingredient not found"


def test_create_ingredient(test_app, monkeypatch, mock_user):
    ingredient_data = {
        "name": "Avocado",
        "calories": 160.0,
        "fat": 15.0,
        "carbs": 9.0,
        "protein": 2.0
    }

    expected_result = {
        "id": 3,
        **ingredient_data
    }

    async def mock_create(ingredient_data, user_id):
        return expected_result

    monkeypatch.setattr(IngredientCrud, "create_ingredient", mock_create)

    response = test_app.post("/ingredients/", json=ingredient_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_result


def test_update_ingredient(test_app, monkeypatch, mock_user):
    updated_data = {
        "name": "Updated Chicken Breast",
        "calories": 170.0,
        "fat": 4.0,
        "carbs": 0.0,
        "protein": 32.0
    }

    expected_result = {
        "id": 1,
        **updated_data
    }

    async def mock_update(ingredient_id, ingredient_data):
        return expected_result

    monkeypatch.setattr(IngredientCrud, "update_ingredient", mock_update)

    response = test_app.put("/ingredients/1", json=updated_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_result


def test_update_ingredient_not_found(test_app, monkeypatch, mock_user):
    async def mock_update(ingredient_id, ingredient_data):
        return None

    monkeypatch.setattr(IngredientCrud, "update_ingredient", mock_update)

    response = test_app.put("/ingredients/999", json={
        "name": "X",
        "calories": 0,
        "fat": 0,
        "carbs": 0,
        "protein": 0
    })
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Ingredient not found"


def test_delete_ingredient(test_app, monkeypatch, mock_user):
    async def mock_delete(ingredient_id: int):
        return True

    monkeypatch.setattr(IngredientCrud, "delete_ingredient", mock_delete)

    response = test_app.delete("/ingredients/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Ingredient deleted successfully"


def test_delete_ingredient_not_found(test_app, monkeypatch, mock_user):
    async def mock_delete(ingredient_id: int):
        return None

    monkeypatch.setattr(IngredientCrud, "delete_ingredient", mock_delete)

    response = test_app.delete("/ingredients/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Ingredient not found"


def test_get_user_ingredients(test_app, monkeypatch, mock_user):
    test_data = [
        {
            "id": 1,
            "name": "Chicken Breast",
            "calories": 165.0,
            "fat": 3.6,
            "carbs": 0.0,
            "protein": 31.0
        }
    ]

    async def mock_get_user_ingredients(page, page_size, user_id):
        return test_data

    monkeypatch.setattr(IngredientCrud, "get_all_ingredients_of_user", mock_get_user_ingredients)

    response = test_app.get("/ingredients/self/?page=1&page_size=10")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == test_data
