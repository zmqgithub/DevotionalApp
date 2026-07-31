from .conftest import (
    client,
    assert_success,
    assert_forbidden,
)


def test_admin_only(admin_headers):

    r = client.get(
        "/api/v1/admin/admin-only",
        headers=admin_headers,
    )

    assert_success(r)


def test_moderator_blocked(moderator_headers):

    r = client.get(
        "/api/v1/admin/admin-only",
        headers=moderator_headers,
    )

    assert_forbidden(r)


def test_user_blocked(user_headers):

    r = client.get(
        "/api/v1/admin/admin-only",
        headers=user_headers,
    )

    assert_forbidden(r)