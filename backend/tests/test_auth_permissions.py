# ============================================================
# FILE:
# backend/tests/test_auth_permissions.py
# ============================================================


# ============================================================
# ADMIN TOKEN
# ============================================================

def test_admin_token_is_valid(
    client,
    admin_headers,
    admin_user_id,
    assert_success,
):
    response = client.get(
        "/api/v1/auth/me",
        headers=admin_headers,
    )

    assert_success(response)

    data = response.json()

    assert data["id"] == admin_user_id


# ============================================================
# MODERATOR TOKEN
# ============================================================

def test_moderator_token_is_valid(
    client,
    moderator_headers,
    moderator_user_id,
    assert_success,
):
    response = client.get(
        "/api/v1/auth/me",
        headers=moderator_headers,
    )

    assert_success(response)

    data = response.json()

    assert data["id"] == moderator_user_id


# ============================================================
# USER TOKEN
# ============================================================

def test_user_token_is_valid(
    client,
    user_headers,
    user_user_id,
    assert_success,
):
    response = client.get(
        "/api/v1/auth/me",
        headers=user_headers,
    )

    assert_success(response)

    data = response.json()

    assert data["id"] == user_user_id


# ============================================================
# USERS LIST
#
# No authentication
# Expected: 401
# ============================================================

def test_users_list_requires_authentication(
    client,
    assert_unauthorized,
):
    response = client.get(
        "/api/v1/users",
    )

    assert_unauthorized(response)


# ============================================================
# MY PROFILE
#
# No authentication
# Expected: 401
# ============================================================

def test_user_profile_requires_authentication(
    client,
    assert_unauthorized,
):
    response = client.get(
        "/api/v1/users/me",
    )

    assert_unauthorized(response)


# ============================================================
# UPDATE MY PROFILE
#
# No authentication
# Expected: 401
# ============================================================

def test_update_profile_requires_authentication(
    client,
    assert_unauthorized,
):
    response = client.put(
        "/api/v1/users/me",
        json={
            "name": "Unauthenticated User",
        },
    )

    assert_unauthorized(response)


# ============================================================
# INVALID TOKEN
#
# Expected: 401
# ============================================================

def test_invalid_token_is_rejected(
    client,
    assert_unauthorized,
):
    response = client.get(
        "/api/v1/users/me",
        headers={
            "Authorization": "Bearer invalid-token",
        },
    )

    assert_unauthorized(response)


# ============================================================
# MISSING BEARER TOKEN
#
# Expected: 401
# ============================================================

def test_missing_bearer_token_is_rejected(
    client,
    assert_unauthorized,
):
    response = client.get(
        "/api/v1/users/me",
        headers={
            "Authorization": "",
        },
    )

    assert_unauthorized(response)