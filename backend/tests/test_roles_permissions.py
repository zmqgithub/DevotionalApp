# ============================================================
# LIST ROLES
#
# ADMIN      -> ALLOWED
# MODERATOR  -> FORBIDDEN
# USER       -> FORBIDDEN
# ============================================================


def test_admin_can_list_roles(
    client,
    admin_headers,
    assert_success,
):
    response = client.get(
        "/api/v1/roles",
        headers=admin_headers,
    )

    assert_success(response)


def test_moderator_cannot_list_roles(
    client,
    moderator_headers,
    assert_forbidden,
):
    response = client.get(
        "/api/v1/roles",
        headers=moderator_headers,
    )

    assert_forbidden(response)


def test_user_cannot_list_roles(
    client,
    user_headers,
    assert_forbidden,
):
    response = client.get(
        "/api/v1/roles",
        headers=user_headers,
    )

    assert_forbidden(response)


# ============================================================
# GET ROLE
# ============================================================


def test_admin_can_get_role(
    client,
    admin_headers,
    assert_success,
):
    response = client.get(
        "/api/v1/roles/1",
        headers=admin_headers,
    )

    # Role may or may not exist.
    # Permission is the important part.
    assert response.status_code in [200, 404], (
        f"Unexpected response: "
        f"{response.status_code}: {response.text}"
    )


def test_moderator_cannot_get_role(
    client,
    moderator_headers,
    assert_forbidden,
):
    response = client.get(
        "/api/v1/roles/1",
        headers=moderator_headers,
    )

    assert_forbidden(response)


def test_user_cannot_get_role(
    client,
    user_headers,
    assert_forbidden,
):
    response = client.get(
        "/api/v1/roles/1",
        headers=user_headers,
    )

    assert_forbidden(response)


# ============================================================
# CREATE ROLE
# ============================================================


def test_moderator_cannot_create_role(
    client,
    moderator_headers,
    assert_forbidden,
):
    response = client.post(
        "/api/v1/roles",
        headers=moderator_headers,
        json={
            "name": "permission_test_role",
        },
    )

    assert_forbidden(response)


def test_user_cannot_create_role(
    client,
    user_headers,
    assert_forbidden,
):
    response = client.post(
        "/api/v1/roles",
        headers=user_headers,
        json={
            "name": "permission_test_user_role",
        },
    )

    assert_forbidden(response)


# ============================================================
# UPDATE ROLE
# ============================================================


def test_moderator_cannot_update_role(
    client,
    moderator_headers,
    assert_forbidden,
):
    response = client.put(
        "/api/v1/roles/1",
        headers=moderator_headers,
        json={
            "name": "updated_role",
        },
    )

    assert_forbidden(response)


def test_user_cannot_update_role(
    client,
    user_headers,
    assert_forbidden,
):
    response = client.put(
        "/api/v1/roles/1",
        headers=user_headers,
        json={
            "name": "updated_role",
        },
    )

    assert_forbidden(response)


# ============================================================
# DELETE ROLE
# ============================================================


def test_moderator_cannot_delete_role(
    client,
    moderator_headers,
    assert_forbidden,
):
    response = client.delete(
        "/api/v1/roles/1",
        headers=moderator_headers,
    )

    assert_forbidden(response)


def test_user_cannot_delete_role(
    client,
    user_headers,
    assert_forbidden,
):
    response = client.delete(
        "/api/v1/roles/1",
        headers=user_headers,
    )

    assert_forbidden(response)