def assert_success(response):
    assert response.status_code < 400, response.text


def assert_forbidden(response):
    assert response.status_code == 403, response.text


def assert_unauthorized(response):
    assert response.status_code == 401, response.text