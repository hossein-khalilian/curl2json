import shlex


def parse_curl(curl_command: str) -> dict:
    """Enhanced cURL command parser"""
    tokens = shlex.split(curl_command.strip())

    parsed = {
        "method": "GET",
        "url": None,
        "headers": {},
        "cookies": {},
        "data": None,
        "auth": None,
        "verify": True,
    }

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
                if key == "Cookie":
                    tokens[i] = "--cookie"
                    tokens[i + 1] = value
                    continue
                parsed["headers"][key.strip()] = value.strip()
            i += 2
        elif token in ("-b", "--cookie") and i + 1 < len(tokens):
            cookie_str = tokens[i + 1]
            for cookie in cookie_str.split(";"):
                cookie = cookie.strip()
                if "=" in cookie:
                    key, value = cookie.split("=", 1)
                    parsed["cookies"][key.strip()] = value.strip()
            i += 2
        elif token in ("-d", "--data-raw") and i + 1 < len(tokens):
            parsed["data"] = tokens[i + 1]
            i += 2
        elif token in ("-u", "--user") and i + 1 < len(tokens):
            auth_parts = tokens[i + 1].split(":", 1)
            parsed["auth"] = {
                "username": auth_parts[0],
                "password": auth_parts[1] if len(auth_parts) > 1 else "",
            }
            i += 2
        elif token == "-k":
            parsed["verify"] = False
            i += 1
        else:
            i += 1

    return parsed
