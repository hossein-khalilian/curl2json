from .parser import parse_curl


def convert_curl_to_json(curl_command: str) -> dict:
    """Convert cURL command to JSON structure"""
    if not curl_command.startswith("curl "):
        raise ValueError("Not a valid cURL command")

    parsed = parse_curl(curl_command)

    if not parsed["url"]:
        raise ValueError("Missing URL in cURL command")

    return {
        "url": parsed["url"],
        "method": parsed["method"],
        "headers": parsed["headers"],
        "data": parsed["data"],
    }
