import os
import json
import requests

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO = os.getenv("GITHUB_REPOSITORY")


def main():
    with open("../config.json",'r') as f:
        config = json.load(f)
    print(config)

if __name__ == "__main__":
    main()