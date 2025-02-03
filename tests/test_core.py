import pytest

from curl2json.core import convert_curl_to_json


def test_basic_get():
    curl = "curl https://example.com"
    result = convert_curl_to_json(curl)
    assert result == {
        "url": "https://example.com",
        "method": "GET",
        "headers": {},
        "data": None,
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
