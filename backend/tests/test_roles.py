from .conftest import (
    client,
    assert_success,
    assert_forbidden,
)


def test_admin_can_list_roles(admin_headers):

    r = client.get(
        "/api/v1/roles",
        headers=admin_headers,
    )

    assert_success(r)


def test_moderator_cannot_list_roles(moderator_headers):

    r = client.get(
        "/api/v1/roles",
        headers=moderator_headers,
    )

    assert_forbidden(r)


def test_user_cannot_list_roles(user_headers):

    r = client.get(
        "/api/v1/roles",
        headers=user_headers,
    )

    assert_forbidden(r)