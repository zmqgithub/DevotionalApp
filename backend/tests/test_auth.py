import pytest

from .conftest import (
    client,
    ADMIN_TOKEN,
    MODERATOR_TOKEN,
    USER_TOKEN,
    ADMIN_USER_ID,
    MODERATOR_USER_ID,
    USER_USER_ID,
    auth_header,
    assert_success,
    assert_unauthorized,
)


@pytest.mark.skipif(not ADMIN_TOKEN, reason="ADMIN_TOKEN missing")
def test_admin_token_valid():

    response = client.get(
        "/api/v1/auth/me",
        headers=auth_header(ADMIN_TOKEN),
    )

    assert_success(response)

    assert response.json()["id"] == ADMIN_USER_ID


@pytest.mark.skipif(not MODERATOR_TOKEN, reason="MODERATOR_TOKEN missing")
def test_moderator_token_valid():

    response = client.get(
        "/api/v1/auth/me",
        headers=auth_header(MODERATOR_TOKEN),
    )

    assert_success(response)

    assert response.json()["id"] == MODERATOR_USER_ID


@pytest.mark.skipif(not USER_TOKEN, reason="USER_TOKEN missing")
def test_user_token_valid():

    response = client.get(
        "/api/v1/auth/me",
        headers=auth_header(USER_TOKEN),
    )

    assert_success(response)

    assert response.json()["id"] == USER_USER_ID


def test_users_requires_auth():
    response = client.get("/api/v1/users")
    assert_unauthorized(response)


def test_profile_requires_auth():
    response = client.get("/api/v1/users/me")
    assert_unauthorized(response)


@pytest.mark.parametrize(
    "token",
    [ADMIN_TOKEN, MODERATOR_TOKEN, USER_TOKEN]
)
def test_all_roles_can_get_profile(token):

    if not token:
        pytest.skip()

    response = client.get(
        "/api/v1/users/me",
        headers=auth_header(token),
    )

    assert_success(response)


@pytest.mark.parametrize(
    "token",
    [ADMIN_TOKEN, MODERATOR_TOKEN, USER_TOKEN]
)
def test_all_roles_can_update_profile(token):

    if not token:
        pytest.skip()

    response = client.put(
        "/api/v1/users/me",
        headers=auth_header(token),
        json={
            "name": "Updated Name"
        },
    )

    assert_success(response)