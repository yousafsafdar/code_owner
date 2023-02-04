import base64
import json
import requests
import os


def github_read_file(username, repository_name, file_path, github_token=None):
    headers = {}
    if github_token:
        headers['Authorization'] = 'token ' + github_token

    url = f"https://api.github.com/repos/{username}/{repository_name}/contents/{file_path}"
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    data = r.json()
    file_content = data['content']
    file_content_encoding = data.get('encoding')
    if file_content_encoding == 'base64':
        file_content = base64.b64decode(file_content).decode()

    return file_content


def main():
    github_token = os.environ['GITHUB_TOKEN']
    username = 'yousafsafdar1'
    repository_name = 'test-github'
    file_path = 'datalake-customers/'
    file_content = github_read_file(username, repository_name, file_path, github_token=github_token)
    data = json.loads(file_content)
    print(data['name'])


if __name__ == '__main__':
    main()
