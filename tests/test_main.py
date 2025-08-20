import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
from main import app  # Assuming your FastAPI app instance is in main.py
import uuid

# Use the TestClient for synchronous tests for simplicity here
# For a fully async test suite, httpx.AsyncClient would be used with pytest-asyncio
client = TestClient(app)

# --- Test Data ---
ADMIN_EMAIL = "admin@vess.com"
ADMIN_PASSWORD = "adminpass"
USER_EMAIL = "testuser@vess.com"
USER_PASSWORD = "userpass"

# --- State ---
# In a real test suite, you'd use fixtures to manage state and dependencies
# For this script, we'll use global-like variables for simplicity
test_state = {
    "admin_token": None,
    "user_token": None,
    "artist_id": None
}

# Helper to get a header
def auth_header(token):
    return {"Authorization": f"Bearer {token}"}

# === PHASE 1.3.3: Authentication Tests ===

def test_1_create_admin_user():
    # This is a workaround to create an admin user first.
    # In a real app, this would be a CLI command or a seeded user.
    from vessapi import crud, schemas
    from vessapi.models import UserRole
    import asyncio
    admin_user = schemas.UserCreate(email=ADMIN_EMAIL, password=ADMIN_PASSWORD)
    # We need to manually set the role
    db_admin = asyncio.run(crud.create_user(user=admin_user, role=UserRole.ADMIN))
    assert db_admin.email == ADMIN_EMAIL
    assert db_admin.role == UserRole.ADMIN

def test_2_create_standard_user():
    response = client.post("/v1/users/", json={"email": USER_EMAIL, "password": USER_PASSWORD})
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == USER_EMAIL
    assert data["role"] == "user"

def test_3_create_duplicate_user_fails():
    response = client.post("/v1/users/", json={"email": USER_EMAIL, "password": "anotherpassword"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_4_login_admin_user():
    response = client.post("/token", data={"username": ADMIN_EMAIL, "password": ADMIN_PASSWORD})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    test_state["admin_token"] = data["access_token"]

def test_5_login_standard_user():
    response = client.post("/token", data={"username": USER_EMAIL, "password": USER_PASSWORD})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    test_state["user_token"] = data["access_token"]

def test_6_login_wrong_password_fails():
    response = client.post("/token", data={"username": USER_EMAIL, "password": "wrongpassword"})
    assert response.status_code == 401

# === PHASE 1.3.4: Authorization Tests ===

def test_7_standard_user_cannot_list_users():
    response = client.get("/v1/users/", headers=auth_header(test_state["user_token"]))
    assert response.status_code == 403
    assert response.json()["detail"] == "Not enough permissions"

def test_8_admin_can_list_users():
    response = client.get("/v1/users/", headers=auth_header(test_state["admin_token"]))
    assert response.status_code == 200
    assert len(response.json()) >= 2 # Admin and standard user

def test_9_standard_user_cannot_create_artist():
    response = client.post(
        "/v1/artists/", 
        json={"name": "Test Artist by User", "bio": "Should not be created"},
        headers=auth_header(test_state["user_token"])
    )
    assert response.status_code == 403

def test_10_admin_can_create_artist():
    response = client.post(
        "/v1/artists/", 
        json={"name": "Test Artist by Admin", "bio": "Should be created"},
        headers=auth_header(test_state["admin_token"])
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Artist by Admin"
    test_state["artist_id"] = data["artist_id"]

def test_11_standard_user_cannot_delete_artist():
    response = client.delete(
        f"/v1/artists/{test_state['artist_id']}",
        headers=auth_header(test_state["user_token"])
    )
    assert response.status_code == 403

def test_12_admin_can_delete_artist():
    response = client.delete(
        f"/v1/artists/{test_state['artist_id']}",
        headers=auth_header(test_state["admin_token"])
    )
    assert response.status_code == 204
