from app.main import app  
from httpx import AsyncClient
import pytest
from dotenv import load_dotenv
import os


load_dotenv()
BASE_URL = os.getenv("BASE_URL", default="http://localhost:8000")
# tests/test_recipes.py


@pytest.mark.asyncio
async def test_register_and_login():
    async with AsyncClient(app=app, base_url=BASE_URL) as ac:
        # Test Registration
        registration_data = {"username": "testuser",
                             "password": "testpassword"}
        response = await ac.post("/user/register/v1", json=registration_data)
        assert response.status_code == 200

        # Test Login
        login_data = {"username": "testuser", "password": "testpassword"}
        response = await ac.post("/user/login/v1", data=login_data)
        assert response.status_code == 200
        token = response.json()["access_token"]

        # Use the token for authenticated requests
        headers = {"Authorization": f"Bearer {token}"}

        # Example: Test Create Recipe 
        recipe_data = {
            "title": "Test Recipe",
            "description": "This is a test recipe",
            "ingredients": "ingredient1,ingredient2",
            "instructions": "Mix ingredients and cook.",
        }
        response = await ac.post("/recipes/create-recipe/v1", json=recipe_data, headers=headers)
        assert response.status_code == 200
