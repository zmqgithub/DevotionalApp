# ============================================================
# USER PROFILE PERMISSIONS
#
# ADMIN      -> ALLOWED
# MODERATOR  -> ALLOWED
# USER       -> ALLOWED
# ============================================================


def test_admin_can_get_own_profile(
    client,
    admin_headers,
    assert_success,
):
    response = client.get(
        "/api/v1/users/me",
        headers=admin_headers,
    )

    assert_success(response)


def test_moderator_can_get_own_profile(
    client,
    moderator_headers,
    assert_success,
):
    response = client.get(
        "/api/v1/users/me",
        headers=moderator_headers,
    )

    assert_success(response)


def test_user_can_get_own_profile(
    client,
    user_headers,
    assert_success,
):
    response = client.get(
        "/api/v1/users/me",
        headers=user_headers,
    )

    assert_success(response)


# ============================================================
# UPDATE OWN PROFILE
#
# ADMIN      -> ALLOWED
# MODERATOR  -> ALLOWED
# USER       -> ALLOWED
# ============================================================


def test_admin_can_update_own_profile(
    client,
    admin_headers,
    assert_success,
):
    response = client.put(
        "/api/v1/users/me",
        headers=admin_headers,
        json={
            "name": "Admin Permission Test",
        },
    )

    assert_success(response)


def test_moderator_can_update_own_profile(
    client,
    moderator_headers,
    assert_success,
):
    response = client.put(
        "/api/v1/users/me",
        headers=moderator_headers,
        json={
            "name": "Moderator Permission Test",
        },
    )

    assert_success(response)


def test_user_can_update_own_profile(
    client,
    user_headers,
    assert_success,
):
    response = client.put(
        "/api/v1/users/me",
        headers=user_headers,
        json={
            "name": "User Permission Test",
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


def test_admin_can_list_users(
    client,
    admin_headers,
    assert_success,
):
    response = client.get(
        "/api/v1/users",
        headers=admin_headers,
    )

    assert_success(response)


def test_moderator_can_list_users(
    client,
    moderator_headers,
    assert_success,
):
    response = client.get(
        "/api/v1/users",
        headers=moderator_headers,
    )

    assert_success(response)


def test_user_cannot_list_users(
    client,
    user_headers,
    assert_forbidden,
):
    response = client.get(
        "/api/v1/users",
        headers=user_headers,
    )

    assert_forbidden(response)


# ============================================================
# GET USER BY ID
#
# ADMIN      -> ALLOWED
# MODERATOR  -> ALLOWED
# USER       -> FORBIDDEN
# ============================================================


def test_admin_can_get_user(
    client,
    admin_headers,
    other_user_id,
    assert_success,
):
    response = client.get(
        f"/api/v1/users/{other_user_id}",
        headers=admin_headers,
    )

    assert_success(response)


def test_moderator_can_get_user(
    client,
    moderator_headers,
    other_user_id,
    assert_success,
):
    response = client.get(
        f"/api/v1/users/{other_user_id}",
        headers=moderator_headers,
    )

    assert_success(response)


def test_user_cannot_get_other_user(
    client,
    user_headers,
    other_user_id,
    assert_forbidden,
):
    response = client.get(
        f"/api/v1/users/{other_user_id}",
        headers=user_headers,
    )

    assert_forbidden(response)


# ============================================================
# CREATE USER
#
# ADMIN      -> ALLOWED
# MODERATOR  -> FORBIDDEN
# USER       -> FORBIDDEN
# ============================================================


def test_admin_can_create_user(
    client,
    admin_headers,
):
    response = client.post(
        "/api/v1/users",
        headers=admin_headers,
        json={
            "name": "Permission Test Admin Created",
            "email": "permission_admin_created@example.com",
            "password": "TestPassword123!",
        },
    )

    # 201 = created
    # 409 = already exists from a previous test run
    assert response.status_code in [201, 409], (
        f"Expected 201 or 409 but got "
        f"{response.status_code}: {response.text}"
    )


def test_moderator_cannot_create_user(
    client,
    moderator_headers,
    assert_forbidden,
):
    response = client.post(
        "/api/v1/users",
        headers=moderator_headers,
        json={
            "name": "Permission Test Moderator",
            "email": "permission_moderator@example.com",
            "password": "TestPassword123!",
        },
    )

    assert_forbidden(response)


def test_user_cannot_create_user(
    client,
    user_headers,
    assert_forbidden,
):
    response = client.post(
        "/api/v1/users",
        headers=user_headers,
        json={
            "name": "Permission Test User",
            "email": "permission_user@example.com",
            "password": "TestPassword123!",
        },
    )

    assert_forbidden(response)


# ============================================================
# UPDATE ANOTHER USER
#
# ADMIN      -> ALLOWED
# MODERATOR  -> FORBIDDEN
# USER       -> FORBIDDEN
# ============================================================


def test_admin_can_update_user(
    client,
    admin_headers,
    other_user_id,
    assert_success,
):
    response = client.put(
        f"/api/v1/users/{other_user_id}",
        headers=admin_headers,
        json={
            "name": "Admin Updated User",
        },
    )

    assert_success(response)


def test_moderator_cannot_update_user(
    client,
    moderator_headers,
    other_user_id,
    assert_forbidden,
):
    response = client.put(
        f"/api/v1/users/{other_user_id}",
        headers=moderator_headers,
        json={
            "name": "Moderator Trying Update",
        },
    )

    assert_forbidden(response)


def test_user_cannot_update_other_user(
    client,
    user_headers,
    other_user_id,
    assert_forbidden,
):
    response = client.put(
        f"/api/v1/users/{other_user_id}",
        headers=user_headers,
        json={
            "name": "User Trying Update",
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


def test_moderator_cannot_delete_user(
    client,
    moderator_headers,
    other_user_id,
    assert_forbidden,
):
    response = client.delete(
        f"/api/v1/users/{other_user_id}",
        headers=moderator_headers,
    )

    assert_forbidden(response)


def test_user_cannot_delete_user(
    client,
    user_headers,
    other_user_id,
    assert_forbidden,
):
    response = client.delete(
        f"/api/v1/users/{other_user_id}",
        headers=user_headers,
    )

    assert_forbidden(response)


# ============================================================
# CHANGE USER STATUS
#
# ADMIN      -> ALLOWED
# MODERATOR  -> FORBIDDEN
# USER       -> FORBIDDEN
# ============================================================


def test_moderator_cannot_change_user_status(
    client,
    moderator_headers,
    other_user_id,
    assert_forbidden,
):
    response = client.patch(
        f"/api/v1/users/{other_user_id}/status",
        headers=moderator_headers,
        json={
            "is_active": True,
        },
    )

    assert_forbidden(response)


def test_user_cannot_change_user_status(
    client,
    user_headers,
    other_user_id,
    assert_forbidden,
):
    response = client.patch(
        f"/api/v1/users/{other_user_id}/status",
        headers=user_headers,
        json={
            "is_active": True,
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


def test_moderator_cannot_change_user_password(
    client,
    moderator_headers,
    other_user_id,
    assert_forbidden,
):
    response = client.put(
        f"/api/v1/users/{other_user_id}/password",
        headers=moderator_headers,
        json={
            "current_password": "WrongPassword123!",
            "new_password": "NewPassword123!",
        },
    )

    assert_forbidden(response)


def test_user_cannot_change_other_user_password(
    client,
    user_headers,
    other_user_id,
    assert_forbidden,
):
    response = client.put(
        f"/api/v1/users/{other_user_id}/password",
        headers=user_headers,
        json={
            "current_password": "WrongPassword123!",
            "new_password": "NewPassword123!",
        },
    )

    assert_forbidden(response)