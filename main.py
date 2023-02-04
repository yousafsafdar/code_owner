import requests
import os


def add_to_codeowners(filename):
    try:
        with open(".github/CODEOWNERS", "a") as codeowners_file:
            codeowners_file.write("/datalake-customers/{}\n".format(filename))
    except IOError as e:
        print(f"Error writing to .github/CODEOWNERS: {e}")


def get_directory_files(repo_owner, repo_name, directory_path, headers):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{directory_path}"
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return [f["name"] for f in response.json()]
        else:
            print(f"Error getting files from Github API: {response.json()['message']}")
    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
    return []


def process_directory_files(repo_owner, repo_name, directory_path):
    existing_files = []
    pat = os.environ.get("GITHUB_PAT")
    if pat is None:
        print("GITHUB_PAT environment variable not set.")
        exit(1)
    headers = {
        "Authorization": f"Token {pat}"
    }

    files = get_directory_files(repo_owner, repo_name, directory_path, headers)
    for filename in files:
        if filename not in existing_files:
            # Add the new file to codeowners
            add_to_codeowners(filename)
            existing_files.append(filename)


if __name__ == '__main__':
    # Replace with your Github repository information
    repo_owner = "yousafsafdar"
    repo_name = "code_owner"
    directory_path = "datalake-customers/"

    process_directory_files(repo_owner, repo_name, directory_path)
