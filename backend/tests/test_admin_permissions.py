# ============================================================
# ADMIN ONLY ENDPOINT
# ============================================================


def test_admin_only_endpoint_allows_admin(
    client,
    admin_headers,
    assert_success,
):
    response = client.get(
        "/api/v1/admin/admin-only",
        headers=admin_headers,
    )

    assert_success(response)


def test_admin_only_endpoint_blocks_moderator(
    client,
    moderator_headers,
    assert_forbidden,
):
    response = client.get(
        "/api/v1/admin/admin-only",
        headers=moderator_headers,
    )

    assert_forbidden(response)


def test_admin_only_endpoint_blocks_user(
    client,
    user_headers,
    assert_forbidden,
):
    response = client.get(
        "/api/v1/admin/admin-only",
        headers=user_headers,
    )

    assert_forbidden(response)


# ============================================================
# ADMIN ROLES API
# ============================================================


def test_admin_can_get_admin_roles(
    client,
    admin_headers,
    assert_success,
):
    response = client.get(
        "/api/v1/admin/roles",
        headers=admin_headers,
    )

    assert_success(response)


def test_moderator_cannot_get_admin_roles(
    client,
    moderator_headers,
    assert_forbidden,
):
    response = client.get(
        "/api/v1/admin/roles",
        headers=moderator_headers,
    )

    assert_forbidden(response)


def test_user_cannot_get_admin_roles(
    client,
    user_headers,
    assert_forbidden,
):
    response = client.get(
        "/api/v1/admin/roles",
        headers=user_headers,
    )

    assert_forbidden(response)


# ============================================================
# ADMIN ROLE ASSIGNMENT
# ============================================================


def test_moderator_cannot_assign_role(
    client,
    moderator_headers,
    assert_forbidden,
):
    response = client.post(
        "/api/v1/admin/users/11/roles",
        headers=moderator_headers,
        json={
            "role_id": 2,
        },
    )

    assert_forbidden(response)


def test_user_cannot_assign_role(
    client,
    user_headers,
    assert_forbidden,
):
    response = client.post(
        "/api/v1/admin/users/11/roles",
        headers=user_headers,
        json={
            "role_id": 2,
        },
    )

    assert_forbidden(response)