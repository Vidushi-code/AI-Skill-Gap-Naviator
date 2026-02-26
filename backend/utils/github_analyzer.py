import requests

def get_github_summary(username):
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)

    if response.status_code != 200:
        return {"error": "GitHub user not found"}

    repos = response.json()

    return {
        "repo_count": len(repos),
        "repos": [repo["name"] for repo in repos[:5]]
    }