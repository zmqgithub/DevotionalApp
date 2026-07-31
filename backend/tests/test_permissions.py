import os
import pytest

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


# ============================================================
# TEST TOKENS
# ============================================================
#
# Set these before running tests:
#
# export ADMIN_TOKEN="your-admin-token"
# export MODERATOR_TOKEN="your-moderator-token"
# export USER_TOKEN="your-user-token"
#
# ============================================================


ADMIN_TOKEN = os.getenv("ADMIN_TOKEN")
MODERATOR_TOKEN = os.getenv("MODERATOR_TOKEN")
USER_TOKEN = os.getenv("USER_TOKEN")


# ============================================================
# TEST USER IDS
# ============================================================

ADMIN_USER_ID = 15
MODERATOR_USER_ID = 16
USER_USER_ID = 17

# Existing user to test admin/moderator access
OTHER_USER_ID = 17


# ============================================================
# HELPERS
# ============================================================

def auth_header(token):
    return {
        "Authorization": f"Bearer {token}"
    }


def assert_success(response):
    assert response.status_code < 400, (
        f"Expected success but got "
        f"{response.status_code}: {response.text}"
    )


def assert_forbidden(response):
    assert response.status_code == 403, (
        f"Expected 403 but got "
        f"{response.status_code}: {response.text}"
    )


def assert_unauthorized(response):
    assert response.status_code == 401, (
        f"Expected 401 but got "
        f"{response.status_code}: {response.text}"
    )


# ============================================================
# TOKEN VALIDATION
# ============================================================

@pytest.mark.skipif(
    not ADMIN_TOKEN,
    reason="ADMIN_TOKEN environment variable not set",
)
def test_admin_token_is_valid():

    response = client.get(
        "/api/v1/auth/me",
        headers=auth_header(ADMIN_TOKEN),
    )

    assert_success(response)

    data = response.json()

    assert data["id"] == ADMIN_USER_ID


@pytest.mark.skipif(
    not MODERATOR_TOKEN,
    reason="MODERATOR_TOKEN environment variable not set",
)
def test_moderator_token_is_valid():

    response = client.get(
        "/api/v1/auth/me",
        headers=auth_header(MODERATOR_TOKEN),
    )

    assert_success(response)

    data = response.json()

    assert data["id"] == MODERATOR_USER_ID


@pytest.mark.skipif(
    not USER_TOKEN,
    reason="USER_TOKEN environment variable not set",
)
def test_user_token_is_valid():

    response = client.get(
        "/api/v1/auth/me",
        headers=auth_header(USER_TOKEN),
    )

    assert_success(response)

    data = response.json()

    assert data["id"] == USER_USER_ID


# ============================================================
# UNAUTHENTICATED ACCESS
# ============================================================

def test_users_list_requires_authentication():

    response = client.get(
        "/api/v1/users",
    )

    assert_unauthorized(response)


def test_user_profile_requires_authentication():

    response = client.get(
        "/api/v1/users/me",
    )

    assert_unauthorized(response)


def test_update_my_profile_requires_authentication():

    response = client.put(
        "/api/v1/users/me",
        json={
            "name": "Unauthenticated User"
        },
    )

    assert_unauthorized(response)


# ============================================================
# USER PROFILE APIs
#
# ADMIN      -> ALLOWED
# MODERATOR  -> ALLOWED
# USER       -> ALLOWED
# ============================================================

@pytest.mark.parametrize(
    "token",
    [
        pytest.param(
            ADMIN_TOKEN,
            marks=pytest.mark.skipif(
                not ADMIN_TOKEN,
                reason="ADMIN_TOKEN not set",
            ),
        ),
        pytest.param(
            MODERATOR_TOKEN,
            marks=pytest.mark.skipif(
                not MODERATOR_TOKEN,
                reason="MODERATOR_TOKEN not set",
            ),
        ),
        pytest.param(
            USER_TOKEN,
            marks=pytest.mark.skipif(
                not USER_TOKEN,
                reason="USER_TOKEN not set",
            ),
        ),
    ],
)
def test_all_roles_can_get_own_profile(token):

    response = client.get(
        "/api/v1/users/me",
        headers=auth_header(token),
    )

    assert_success(response)


@pytest.mark.parametrize(
    "token",
    [
        pytest.param(
            ADMIN_TOKEN,
            marks=pytest.mark.skipif(
                not ADMIN_TOKEN,
                reason="ADMIN_TOKEN not set",
            ),
        ),
        pytest.param(
            MODERATOR_TOKEN,
            marks=pytest.mark.skipif(
                not MODERATOR_TOKEN,
                reason="MODERATOR_TOKEN not set",
            ),
        ),
        pytest.param(
            USER_TOKEN,
            marks=pytest.mark.skipif(
                not USER_TOKEN,
                reason="USER_TOKEN not set",
            ),
        ),
    ],
)
def test_all_roles_can_update_own_profile(token):

    response = client.put(
        "/api/v1/users/me",
        headers=auth_header(token),
        json={
            "name": "Permission Test User"
        },
    )

    assert_success(response)


# ============================================================
# LIST USERS
#
# ADMIN      -> ALLOWED
# MODERATOR  -> ALLOWED
# USER       -> FORBIDDEN
# ============================================================

def test_admin_can_list_users(admin_headers):

    r = client.get(
        "/api/v1/users",
        headers=admin_headers,
    )

    assert_success(r)


def test_moderator_can_list_users(moderator_headers):

    r = client.get(
        "/api/v1/users",
        headers=moderator_headers,
    )

    assert_success(r)


def test_user_cannot_list_users(user_headers):

    r = client.get(
        "/api/v1/users",
        headers=user_headers,
    )

    assert_forbidden(r)

def test_admin_can_create_user(admin_headers):

    r = client.post(
        "/api/v1/users",
        headers=admin_headers,
        json={
            "name":"Temp",
            "email":"temp123@test.com",
            "password":"Password123!",
        },
    )

    assert r.status_code in [201,409]

def test_moderator_cannot_create_user(moderator_headers):

    r = client.post(
        "/api/v1/users",
        headers=moderator_headers,
        json={
            "name":"Temp",
            "email":"temp2@test.com",
            "password":"Password123!",
        },
    )

    assert_forbidden(r)

def test_user_cannot_create_user(user_headers):

    r = client.post(
        "/api/v1/users",
        headers=user_headers,
        json={
            "name":"Temp",
            "email":"temp3@test.com",
            "password":"Password123!",
        },
    )

    assert_forbidden(r)

# ============================================================
# GET USER BY ID
#
# ADMIN      -> ALLOWED
# MODERATOR  -> ALLOWED
# USER       -> FORBIDDEN
# ============================================================

def test_admin_can_get_user():

    response = client.get(
        f"/api/v1/users/{OTHER_USER_ID}",
        headers=auth_header(ADMIN_TOKEN),
    )

    assert_success(response)


def test_moderator_can_get_user():

    response = client.get(
        f"/api/v1/users/{OTHER_USER_ID}",
        headers=auth_header(MODERATOR_TOKEN),
    )

    assert_success(response)


def test_user_cannot_get_user():

    response = client.get(
        f"/api/v1/users/{OTHER_USER_ID}",
        headers=auth_header(USER_TOKEN),
    )

    assert_forbidden(response)


# ============================================================
# CREATE USER
#
# ADMIN      -> ALLOWED
# MODERATOR  -> FORBIDDEN
# USER       -> FORBIDDEN
# ============================================================

def test_moderator_cannot_create_user():

    response = client.post(
        "/api/v1/users",
        headers=auth_header(MODERATOR_TOKEN),
        json={
            "name": "Permission Test Moderator",
            "email": "permission_moderator_test@example.com",
            "password": "TestPassword123!",
        },
    )

    assert_forbidden(response)


def test_user_cannot_create_user():

    response = client.post(
        "/api/v1/users",
        headers=auth_header(USER_TOKEN),
        json={
            "name": "Permission Test User",
            "email": "permission_user_test@example.com",
            "password": "TestPassword123!",
        },
    )

    assert_forbidden(response)


# ============================================================
# UPDATE USER
#
# ADMIN      -> ALLOWED
# MODERATOR  -> ALLOWED
# USER       -> FORBIDDEN
# ============================================================

def test_admin_can_update_user():

    response = client.put(
        f"/api/v1/users/{OTHER_USER_ID}",
        headers=auth_header(ADMIN_TOKEN),
        json={
            "name": "Admin Updated User"
        },
    )

    assert_success(response)


def test_moderator_can_update_user():

    response = client.put(
        f"/api/v1/users/{OTHER_USER_ID}",
        headers=auth_header(MODERATOR_TOKEN),
        json={
            "name": "Moderator Updated User"
        },
    )

    assert_success(response)


def test_user_cannot_update_other_user():

    response = client.put(
        f"/api/v1/users/{OTHER_USER_ID}",
        headers=auth_header(USER_TOKEN),
        json={
            "name": "User Trying To Update"
        },
    )

    assert_forbidden(response)


# ============================================================
# DELETE USER
#
# ADMIN      -> ALLOWED
# MODERATOR  -> FORBIDDEN
# USER       -> FORBIDDEN
# ============================================================

def test_moderator_cannot_delete_user():

    response = client.delete(
        f"/api/v1/users/{OTHER_USER_ID}",
        headers=auth_header(MODERATOR_TOKEN),
    )

    assert_forbidden(response)


def test_user_cannot_delete_user():

    response = client.delete(
        f"/api/v1/users/{OTHER_USER_ID}",
        headers=auth_header(USER_TOKEN),
    )

    assert_forbidden(response)


# ============================================================
# CHANGE USER STATUS
#
# ADMIN      -> ALLOWED
# MODERATOR  -> FORBIDDEN
# USER       -> FORBIDDEN
# ============================================================

def test_moderator_cannot_change_user_status():

    response = client.patch(
        f"/api/v1/users/{OTHER_USER_ID}/status",
        headers=auth_header(MODERATOR_TOKEN),
        json={
            "is_active": True
        },
    )

    assert_forbidden(response)


def test_user_cannot_change_user_status():

    response = client.patch(
        f"/api/v1/users/{OTHER_USER_ID}/status",
        headers=auth_header(USER_TOKEN),
        json={
            "is_active": True
        },
    )

    assert_forbidden(response)


# ============================================================
# CHANGE USER PASSWORD
#
# ADMIN      -> ALLOWED
# MODERATOR  -> FORBIDDEN
# USER       -> FORBIDDEN
# ============================================================

def test_moderator_cannot_change_user_password():

    response = client.put(
        f"/api/v1/users/{OTHER_USER_ID}/password",
        headers=auth_header(MODERATOR_TOKEN),
        json={
            "current_password": "WrongPassword123!",
            "new_password": "NewPassword123!",
        },
    )

    assert_forbidden(response)


def test_user_cannot_change_other_user_password():

    response = client.put(
        f"/api/v1/users/{OTHER_USER_ID}/password",
        headers=auth_header(USER_TOKEN),
        json={
            "current_password": "WrongPassword123!",
            "new_password": "NewPassword123!",
        },
    )

    assert_forbidden(response)


# ============================================================
# ADMIN-ONLY ENDPOINT
# ============================================================

def test_admin_only_endpoint_allows_admin():

    response = client.get(
        "/api/v1/admin/admin-only",
        headers=auth_header(ADMIN_TOKEN),
    )

    assert_success(response)


def test_admin_only_endpoint_blocks_moderator():

    response = client.get(
        "/api/v1/admin/admin-only",
        headers=auth_header(MODERATOR_TOKEN),
    )

    assert_forbidden(response)


def test_admin_only_endpoint_blocks_user():

    response = client.get(
        "/api/v1/admin/admin-only",
        headers=auth_header(USER_TOKEN),
    )

    assert_forbidden(response)


# ============================================================
# ADMIN ROLES API
#
# ADMIN      -> ALLOWED
# MODERATOR  -> FORBIDDEN
# USER       -> FORBIDDEN
# ============================================================

def test_admin_can_get_roles():

    response = client.get(
        "/api/v1/admin/roles",
        headers=auth_header(ADMIN_TOKEN),
    )

    assert_success(response)


def test_moderator_cannot_get_admin_roles():

    response = client.get(
        "/api/v1/admin/roles",
        headers=auth_header(MODERATOR_TOKEN),
    )

    assert_forbidden(response)


def test_user_cannot_get_admin_roles():

    response = client.get(
        "/api/v1/admin/roles",
        headers=auth_header(USER_TOKEN),
    )

    assert_forbidden(response)


# ============================================================
# ROLE APIs
#
# ADMIN      -> ALLOWED
# MODERATOR  -> FORBIDDEN
# USER       -> FORBIDDEN
# ============================================================

def test_admin_can_list_roles():

    response = client.get(
        "/api/v1/roles",
        headers=auth_header(ADMIN_TOKEN),
    )

    assert_success(response)


def test_moderator_cannot_list_roles():

    response = client.get(
        "/api/v1/roles",
        headers=auth_header(MODERATOR_TOKEN),
    )

    assert_forbidden(response)


def test_user_cannot_list_roles():

    response = client.get(
        "/api/v1/roles",
        headers=auth_header(USER_TOKEN),
    )

    assert_forbidden(response)


# ============================================================
# ADMIN ROLE ASSIGNMENT
#
# ADMIN      -> ALLOWED
# MODERATOR  -> FORBIDDEN
# USER       -> FORBIDDEN
# ============================================================

def test_moderator_cannot_assign_role():

    response = client.post(
        "/api/v1/admin/users/11/roles",
        headers=auth_header(MODERATOR_TOKEN),
        json={
            "role_id": 2
        },
    )

    assert_forbidden(response)


def test_user_cannot_assign_role():

    response = client.post(
        "/api/v1/admin/users/11/roles",
        headers=auth_header(USER_TOKEN),
        json={
            "role_id": 2
        },
    )

    assert_forbidden(response)


# ============================================================
# HEALTH CHECK
#
# PUBLIC
# ============================================================

def test_health_check_is_public():

    response = client.get(
        "/api/v1/health",
    )

    assert_success(response)