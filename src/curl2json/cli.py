import argparse
import json

from .core import convert_curl_to_json


def main():
    parser = argparse.ArgumentParser(
        description="Convert cURL commands to JSON",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "command", nargs="?", help="cURL command string (wrap in quotes)"
    )
    parser.add_argument("-f", "--file", help="Input file containing cURL command")

    args = parser.parse_args()

    try:
        if args.file:
            with open(args.file, "r") as f:
                curl_command = f.read().strip()
        else:
            curl_command = args.command

        result = convert_curl_to_json(curl_command)
        print(json.dumps(result, indent=2))

    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)
