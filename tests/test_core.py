import pytest

from curl2json.core import convert_curl_to_json


def test_basic_get():
    curl = "curl https://example.com"
    result = convert_curl_to_json(curl)
    assert result == {
        "url": "https://example.com",
        "method": "GET",
        "headers": {},
        "cookies": {},
        "data": None,
        "verify": True,
    }


def test_post_with_headers():
    curl = """curl -X POST https://api.example.com/data \\
        -H 'Content-Type: application/json' \\
        -d '{"key": "value"}'"""

    result = convert_curl_to_json(curl)
    assert result["method"] == "POST"
    assert result["headers"]["Content-Type"] == "application/json"
    assert result["data"] == '{"key": "value"}'


def test_invalid_command():
    with pytest.raises(ValueError):
        convert_curl_to_json("wget https://example.com")


def test_missing_url():
    with pytest.raises(ValueError):
        convert_curl_to_json("curl -X POST")


def test_basic_auth():
    curl = "curl -u user:pass https://secured.example.com"
    result = convert_curl_to_json(curl)
    assert result["auth"] == {"username": "user", "password": "pass"}
    assert result["verify"] is True


def test_ssl_verification_disabled():
    curl = "curl -k https://insecure.example.com"
    result = convert_curl_to_json(curl)
    assert result["verify"] is False


def test_complex_case():
    curl = """curl -X PUT https://api.example.com/resources/1 \\
        -H 'Content-Type: application/json' \\
        -H 'Authorization: Bearer token' \\
        -d '{"update": "data"}' \\
        -u admin:secret \\
        -k"""

    result = convert_curl_to_json(curl)
    assert result["method"] == "PUT"
    assert result["headers"]["Authorization"] == "Bearer token"
    assert result["auth"]["username"] == "admin"
    assert result["verify"] is False


def test_single_cookie():
    curl = "curl -b 'session=abc123' https://cookies.example.com"
    result = convert_curl_to_json(curl)
    assert result["cookies"] == {"session": "abc123"}


def test_multiple_cookies():
    curl = "curl --cookie 'user=john; token=xyz789' https://auth.example.com"
    result = convert_curl_to_json(curl)
    assert result["cookies"] == {"user": "john", "token": "xyz789"}


def test_cookies_with_special_chars():
    curl = (
        "curl -b 'name=John%20Doe; preference=dark_theme' https://profile.example.com"
    )
    result = convert_curl_to_json(curl)
    assert result["cookies"] == {"name": "John%20Doe", "preference": "dark_theme"}


def test_cookie_and_header_together():
    curl = """curl https://api.example.com \\
        -H 'Cookie: extra=value' \\
        -b 'session=main'"""
    result = convert_curl_to_json(curl)
    assert result["cookies"] == {"extra": "value", "session": "main"}
