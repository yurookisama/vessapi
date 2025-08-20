import pytest
from httpx import AsyncClient
from fastapi import status

@pytest.mark.asyncio
async def create_user_and_login(client: AsyncClient, user_data: dict) -> dict:
    await client.post("/v1/users/", json=user_data)
    login_payload = {"username": user_data["email"], "password": user_data["password"]}
    response = await client.post("/token", data=login_payload)
    return response.json()

@pytest.mark.asyncio
async def test_user_cannot_access_other_user_data(client: AsyncClient):
    """A normal user should not be able to get another user's data by ID."""
    user1_data = {"username": "user1", "email": "user1@test.com", "password": "pass1"}
    token1_data = await create_user_and_login(client, user1_data)
    headers1 = {"Authorization": f"Bearer {token1_data['access_token']}"}

    user2_data = {"username": "user2", "email": "user2@test.com", "password": "pass2"}
    user2_response = await client.post("/v1/users/", json=user2_data)
    user2_id = user2_response.json()["user_id"]

    response = await client.get(f"/v1/users/{user2_id}", headers=headers1)
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.asyncio
async def test_normal_user_cannot_list_all_users(client: AsyncClient):
    """A normal user should not be able to list all users."""
    user_data = {"username": "user3", "email": "user3@test.com", "password": "pass3"}
    token_data = await create_user_and_login(client, user_data)
    headers = {"Authorization": f"Bearer {token_data['access_token']}"}

    response = await client.get("/v1/users/", headers=headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.asyncio
async def test_normal_user_cannot_create_artist(client: AsyncClient):
    """A normal user should not be able to create an artist."""
    user_data = {"username": "user4", "email": "user4@test.com", "password": "pass4"}
    token_data = await create_user_and_login(client, user_data)
    headers = {"Authorization": f"Bearer {token_data['access_token']}"}

    artist_data = {"name": "Test Artist by normal user"}
    response = await client.post("/v1/artists/", json=artist_data, headers=headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.asyncio
async def test_user_cannot_delete_another_users_playlist(client: AsyncClient):
    """A user should not be able to delete a playlist owned by another user."""
    user5_data = {"username": "user5", "email": "user5@test.com", "password": "pass5"}
    token5_data = await create_user_and_login(client, user5_data)
    headers5 = {"Authorization": f"Bearer {token5_data['access_token']}"}
    user5_id_resp = await client.get("/v1/users/me/", headers=headers5)
    user5_id = user5_id_resp.json()["user_id"]
    playlist_data = {"name": "User5s Playlist", "user_id": user5_id}
    playlist_response = await client.post("/v1/playlists/", json=playlist_data, headers=headers5)
    playlist_id = playlist_response.json()["playlist_id"]

    user6_data = {"username": "user6", "email": "user6@test.com", "password": "pass6"}
    token6_data = await create_user_and_login(client, user6_data)
    headers6 = {"Authorization": f"Bearer {token6_data['access_token']}"}

    response = await client.delete(f"/v1/playlists/{playlist_id}", headers=headers6)
    assert response.status_code == status.HTTP_403_FORBIDDEN