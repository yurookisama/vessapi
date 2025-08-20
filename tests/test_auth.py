import pytest
from httpx import AsyncClient
from fastapi import status

# A sample user for testing
user_data = {
    "username": "testauthuser",
    "email": "auth@example.com",
    "password": "a_very_secure_password",
    "full_name": "Auth Test User"
}

@pytest.mark.asyncio
async def test_create_user_success(client: AsyncClient):
    """Test that a new user can be created successfully."""
    response = await client.post("/v1/users/", json=user_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["username"] == user_data["username"]
    assert "password" not in data
    assert data["role"] == "user"

@pytest.mark.asyncio
async def test_create_user_duplicate_email(client: AsyncClient):
    """Test that creating a user with an already registered email fails."""
    # First, create the user
    await client.post("/v1/users/", json=user_data)
    # Then, try to create it again
    response = await client.post("/v1/users/", json=user_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Email already registered" in response.json()["detail"]

@pytest.mark.asyncio
async def test_login_success(client: AsyncClient):
    """Test that a registered user can successfully log in and get a token."""
    await client.post("/v1/users/", json=user_data)
    login_data = {
        "username": user_data["email"],
        "password": user_data["password"]
    }
    response = await client.post("/token", data=login_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient):
    """Test that logging in with an incorrect password fails."""
    await client.post("/v1/users/", json=user_data)
    login_data = {
        "username": user_data["email"],
        "password": "wrong_password"
    }
    response = await client.post("/token", data=login_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Incorrect email or password" in response.json()["detail"]

@pytest.mark.asyncio
async def test_read_current_user(client: AsyncClient):
    """Test that the /users/me endpoint returns the correct user data with a valid token."""
    await client.post("/v1/users/", json=user_data)
    login_data = {
        "username": user_data["email"],
        "password": user_data["password"]
    }
    login_response = await client.post("/token", data=login_data)
    token = login_response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    me_response = await client.get("/v1/users/me/", headers=headers)
    
    assert me_response.status_code == status.HTTP_200_OK
    data = me_response.json()
    assert data["email"] == user_data["email"]