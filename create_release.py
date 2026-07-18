import os
import re
import sys
import requests

REPO = "railingshell/Playerok-Auto-Placement-v2.0"


def get_version():
    with open("__init__.py", "r", encoding="utf-8") as f:
        content = f.read()
    match = re.search(r'VERSION\s*=\s*"([^"]+)"', content)
    if not match:
        raise ValueError("VERSION not found in __init__.py")
    return match.group(1)


def get_token():
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        return token
    token = input("Enter GitHub Personal Access Token: ").strip()
    if not token:
        print("Token is required.")
        sys.exit(1)
    return token


def release_exists(token, tag):
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json"
    }
    url = f"https://api.github.com/repos/{REPO}/releases/tags/{tag}"
    response = requests.get(url, headers=headers, timeout=10)
    return response.status_code == 200


def create_release(token, tag, name, body):
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json"
    }
    url = f"https://api.github.com/repos/{REPO}/releases"
    data = {
        "tag_name": tag,
        "target_commitish": "main",
        "name": name,
        "body": body,
        "draft": False,
        "prerelease": False
    }
    response = requests.post(url, headers=headers, json=data, timeout=10)
    response.raise_for_status()
    return response.json()


def main():
    version = get_version()
    tag = version if version.startswith("v") else f"v{version}"

    print(f"Current version: {version}")
    print(f"Release tag: {tag}")

    token = get_token()

    if release_exists(token, tag):
        print(f"Release {tag} already exists.")
        sys.exit(0)

    name = input(f"Release title [Playerok Auto Placement {tag}]: ").strip()
    if not name:
        name = f"Playerok Auto Placement {tag}"

    body = input("Release description [Auto release]: ").strip()
    if not body:
        body = "Auto release"

    print(f"Creating release {tag}...")
    release = create_release(token, tag, name, body)

    print(f"Release created: {release['html_url']}")


if __name__ == "__main__":
    main()
