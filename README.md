# curl2json

Convert cURL commands to JSON requests

## Installation

```bash
pip install git+https://github.com/hossein-khalilian/curl2json.git
```

## Basic Usage

```bash
curl2json "curl https://api.example.com"

# Test authentication
curl2json "curl -u myuser:mypass https://auth.example.com"

# Test SSL verification disable
curl2json "curl -k https://self-signed.example.com"

# Test complex command
curl2json "curl -X PATCH https://api.example.com -H 'X-Custom: value' -d 'data' -u admin:123 -k"
```

[More documentation coming soon]
