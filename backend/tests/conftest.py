# ============================================================
# FILE:
# backend/tests/conftest.py
# ============================================================

import os

import pytest
from fastapi.testclient import TestClient

from app.main import app


# ============================================================
# FASTAPI CLIENT
# ============================================================

@pytest.fixture(scope="session")
def client():
    """
    Shared FastAPI TestClient.

    Available to every test automatically.
    """

    with TestClient(app) as test_client:
        yield test_client


# ============================================================
# TOKENS
# ============================================================

@pytest.fixture(scope="session")
def admin_token():
    """
    ADMIN JWT token.

    Set using:

        export ADMIN_TOKEN="..."
    """

    return os.getenv("ADMIN_TOKEN")


@pytest.fixture(scope="session")
def moderator_token():
    """
    MODERATOR JWT token.

    Set using:

        export MODERATOR_TOKEN="..."
    """

    return os.getenv("MODERATOR_TOKEN")


@pytest.fixture(scope="session")
def user_token():
    """
    USER JWT token.

    Set using:

        export USER_TOKEN="..."
    """

    return os.getenv("USER_TOKEN")


# ============================================================
# USER IDS
# ============================================================

@pytest.fixture(scope="session")
def admin_user_id():
    """
    Database ID of the ADMIN test user.
    """

    return 15


@pytest.fixture(scope="session")
def moderator_user_id():
    """
    Database ID of the MODERATOR test user.
    """

    return 16


@pytest.fixture(scope="session")
def user_user_id():
    """
    Database ID of the normal USER test user.
    """

    return 17


@pytest.fixture(scope="session")
def other_user_id():
    """
    Existing user used for permission tests.
    """

    return 17


# ============================================================
# AUTH HEADERS
# ============================================================

@pytest.fixture
def admin_headers(admin_token):
    """
    Authorization header for ADMIN.
    """

    if not admin_token:
        pytest.skip(
            "ADMIN_TOKEN environment variable not set"
        )

    return {
        "Authorization": f"Bearer {admin_token}"
    }


@pytest.fixture
def moderator_headers(moderator_token):
    """
    Authorization header for MODERATOR.
    """

    if not moderator_token:
        pytest.skip(
            "MODERATOR_TOKEN environment variable not set"
        )

    return {
        "Authorization": f"Bearer {moderator_token}"
    }


@pytest.fixture
def user_headers(user_token):
    """
    Authorization header for USER.
    """

    if not user_token:
        pytest.skip(
            "USER_TOKEN environment variable not set"
        )

    return {
        "Authorization": f"Bearer {user_token}"
    }


# ============================================================
# RESPONSE ASSERTION HELPERS
# ============================================================

@pytest.fixture
def assert_success():
    """
    Assert that an API response is successful.
    """

    def _assert(response):
        assert response.status_code < 400, (
            f"Expected success but got "
            f"{response.status_code}: "
            f"{response.text}"
        )

    return _assert


@pytest.fixture
def assert_forbidden():
    """
    Assert HTTP 403 Forbidden.
    """

    def _assert(response):
        assert response.status_code == 403, (
            f"Expected 403 but got "
            f"{response.status_code}: "
            f"{response.text}"
        )

    return _assert


@pytest.fixture
def assert_unauthorized():
    """
    Assert HTTP 401 Unauthorized.
    """

    def _assert(response):
        assert response.status_code == 401, (
            f"Expected 401 but got "
            f"{response.status_code}: "
            f"{response.text}"
        )

    return _assert


@pytest.fixture
def assert_not_found():
    """
    Assert HTTP 404 Not Found.
    """

    def _assert(response):
        assert response.status_code == 404, (
            f"Expected 404 but got "
            f"{response.status_code}: "
            f"{response.text}"
        )

    return _assert


@pytest.fixture
def assert_conflict():
    """
    Assert HTTP 409 Conflict.
    """

    def _assert(response):
        assert response.status_code == 409, (
            f"Expected 409 but got "
            f"{response.status_code}: "
            f"{response.text}"
        )

    return _assert