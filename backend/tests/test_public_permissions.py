# ============================================================
# HEALTH CHECK
#
# PUBLIC
# No authentication required.
# ============================================================


def test_health_check_is_public(
    client,
    assert_success,
):
    response = client.get(
        "/api/v1/health",
    )

    assert_success(response)


# ============================================================
# HEALTH CHECK WITH AUTHENTICATION
# ============================================================


def test_health_check_works_for_admin(
    client,
    admin_headers,
    assert_success,
):
    response = client.get(
        "/api/v1/health",
        headers=admin_headers,
    )

    assert_success(response)


def test_health_check_works_for_moderator(
    client,
    moderator_headers,
    assert_success,
):
    response = client.get(
        "/api/v1/health",
        headers=moderator_headers,
    )

    assert_success(response)


def test_health_check_works_for_user(
    client,
    user_headers,
    assert_success,
):
    response = client.get(
        "/api/v1/health",
        headers=user_headers,
    )

    assert_success(response)