import re
import shlex


def parse_curl(curl_command: str) -> dict:
    """Basic cURL command parser"""
    tokens = shlex.split(curl_command.strip())

    parsed = {"method": "GET", "url": None, "headers": {}, "data": None}

    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token == "curl":
            i += 1
        elif token.startswith("http"):
            parsed["url"] = token
            i += 1
        elif token == "-X" and i + 1 < len(tokens):
            parsed["method"] = tokens[i + 1].upper()
            i += 2
        elif token == "-H" and i + 1 < len(tokens):
            header = tokens[i + 1]
            if ":" in header:
                key, value = header.split(":", 1)
                parsed["headers"][key.strip()] = value.strip()
            i += 2
        elif token in ("-d", "--data-raw") and i + 1 < len(tokens):
            parsed["data"] = tokens[i + 1]
            i += 2
        else:
            i += 1

    return parsed
