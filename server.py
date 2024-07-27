from fastapi import FastAPI, Request
import requests

app = FastAPI()

@app.post("/events/pull-request")
async def handle_pull_request(request: Request):
    payload = await request.json()
    action = payload.get("action")
    pull_request = payload.get("pull_request", {})
    repo = payload.get("repository", {})
    repo_name = repo.get("name")
    pr_number = pull_request.get("number")
    pr_title = pull_request.get("title")
    pr_creator = pull_request.get("user", {}).get("login")

    if action == "opened":
        comment = f"Hello @{pr_creator}, thank you for creating this pull request: {pr_title}"
        # Configure the following values with your repository details and token
        repo_owner = "ankitaritgithub"
        access_token = "ghp_11A5FD4LY0x7z2JqnJ7mTl_3drb81L2aIWqTPoTvtsY2EAWdiQIgvmLP0C9pSjssNa6KUY4S2BN2Z8AaDM"
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues/{pr_number}/comments"
        headers = {
            "Authorization": f"token {access_token}",
            "Accept": "application/vnd.github.v3+json",
        }
        data = {
            "body": comment
        }
        response = requests.post(url, headers=headers, json=data)
        return {"status": "success", "response": response.json()}
    return {"status": "ignored"}
