"""Auth flow tests: register → login → protected endpoint."""

from httpx import AsyncClient


async def _register(client: AsyncClient, email: str = "a@example.com", password: str = "password123") -> dict:
    response = await client.post("/users", json={"email": email, "password": password})
    assert response.status_code == 201, response.text
    return response.json()


async def _login(client: AsyncClient, email: str, password: str) -> str:
    response = await client.post("/auth/login", json={"email": email, "password": password})
    assert response.status_code == 200, response.text
    return response.json()["access_token"]


async def test_register_never_returns_the_password(client: AsyncClient) -> None:
    user = await _register(client)
    assert "password" not in user
    assert "hashed_password" not in user
    assert user["is_active"] is True


async def test_duplicate_email_conflicts(client: AsyncClient) -> None:
    await _register(client)
    again = await client.post(
        "/users", json={"email": "a@example.com", "password": "password123"}
    )
    assert again.status_code == 409


async def test_short_password_rejected(client: AsyncClient) -> None:
    response = await client.post("/users", json={"email": "b@example.com", "password": "short"})
    assert response.status_code == 422


async def test_login_returns_a_usable_token(client: AsyncClient) -> None:
    await _register(client)
    token = await _login(client, "a@example.com", "password123")

    me = await client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200, me.text
    assert me.json()["email"] == "a@example.com"

    users_me = await client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert users_me.status_code == 200


async def test_wrong_password_is_401(client: AsyncClient) -> None:
    await _register(client)
    response = await client.post("/auth/login", json={"email": "a@example.com", "password": "nope"})
    assert response.status_code == 401


async def test_protected_endpoints_require_a_token(client: AsyncClient) -> None:
    assert (await client.get("/auth/me")).status_code == 401
    bad = await client.get("/auth/me", headers={"Authorization": "Bearer garbage"})
    assert bad.status_code == 401
