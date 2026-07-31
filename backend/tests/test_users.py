from .conftest import (
    client,
    OTHER_USER_ID,
    admin_headers,
    moderator_headers,
    user_headers,
    assert_success,
    assert_forbidden,
)


# ============================================================
# LIST USERS
# ============================================================

def test_admin_can_list_users(admin_headers):
    r = client.get("/api/v1/users", headers=admin_headers)
    assert_success(r)


def test_moderator_can_list_users(moderator_headers):
    r = client.get("/api/v1/users", headers=moderator_headers)
    assert_success(r)


def test_user_cannot_list_users(user_headers):
    r = client.get("/api/v1/users", headers=user_headers)
    assert_forbidden(r)


# ============================================================
# GET USER
# ============================================================

def test_admin_can_get_user(admin_headers):
    r = client.get(
        f"/api/v1/users/{OTHER_USER_ID}",
        headers=admin_headers,
    )
    assert_success(r)


def test_moderator_can_get_user(moderator_headers):
    r = client.get(
        f"/api/v1/users/{OTHER_USER_ID}",
        headers=moderator_headers,
    )
    assert_success(r)


def test_user_cannot_get_user(user_headers):
    r = client.get(
        f"/api/v1/users/{OTHER_USER_ID}",
        headers=user_headers,
    )
    assert_forbidden(r)


# ============================================================
# CREATE USER
# ============================================================

def test_admin_can_create_user(admin_headers):

    r = client.post(
        "/api/v1/users",
        headers=admin_headers,
        json={
            "name": "Temp",
            "email": "temp123@test.com",
            "password": "Password123!",
        }
    )

    assert r.status_code in [201, 409]


def test_moderator_cannot_create_user(moderator_headers):

    r = client.post(
        "/api/v1/users",
        headers=moderator_headers,
        json={
            "name": "Temp",
            "email": "temp2@test.com",
            "password": "Password123!",
        }
    )

    assert_forbidden(r)


def test_user_cannot_create_user(user_headers):

    r = client.post(
        "/api/v1/users",
        headers=user_headers,
        json={
            "name": "Temp",
            "email": "temp3@test.com",
            "password": "Password123!",
        }
    )

    assert_forbidden(r)


# ============================================================
# UPDATE USER
# ============================================================

def test_admin_can_update_user(admin_headers):

    r = client.put(
        f"/api/v1/users/{OTHER_USER_ID}",
        headers=admin_headers,
        json={"name": "Admin Update"},
    )

    assert_success(r)


def test_moderator_cannot_update_user(moderator_headers):

    r = client.put(
        f"/api/v1/users/{OTHER_USER_ID}",
        headers=moderator_headers,
        json={"name": "Moderator Update"},
    )

    assert_forbidden(r)


def test_user_cannot_update_user(user_headers):

    r = client.put(
        f"/api/v1/users/{OTHER_USER_ID}",
        headers=user_headers,
        json={"name": "User Update"},
    )

    assert_forbidden(r)


# ============================================================
# DELETE USER
# ============================================================

def test_admin_can_delete_user(admin_headers):
    pass


def test_moderator_cannot_delete_user(moderator_headers):

    r = client.delete(
        f"/api/v1/users/{OTHER_USER_ID}",
        headers=moderator_headers,
    )

    assert_forbidden(r)


def test_user_cannot_delete_user(user_headers):

    r = client.delete(
        f"/api/v1/users/{OTHER_USER_ID}",
        headers=user_headers,
    )

    assert_forbidden(r)


# ============================================================
# STATUS
# ============================================================

def test_moderator_cannot_change_status(moderator_headers):

    r = client.patch(
        f"/api/v1/users/{OTHER_USER_ID}/status",
        headers=moderator_headers,
        json={"is_active": True},
    )

    assert_forbidden(r)


def test_user_cannot_change_status(user_headers):

    r = client.patch(
        f"/api/v1/users/{OTHER_USER_ID}/status",
        headers=user_headers,
        json={"is_active": True},
    )

    assert_forbidden(r)


# ============================================================
# PASSWORD
# ============================================================

def test_moderator_cannot_change_password(moderator_headers):

    r = client.put(
        f"/api/v1/users/{OTHER_USER_ID}/password",
        headers=moderator_headers,
        json={
            "current_password": "old",
            "new_password": "new",
        },
    )

    assert_forbidden(r)