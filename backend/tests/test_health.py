from .conftest import client, assert_success


def test_health_check():

    response = client.get(
        "/api/v1/health"
    )

    assert_success(response)