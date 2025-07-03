import os
import requests
from datetime import datetime, timezone, timedelta
from utils.line import push_to_line

GITHUB_REPO = "apache/airflow"

def get_latest_issue(repo):
    url = f"https://api.github.com/repos/{repo}/issues"
    resp = requests.get(url, params={"per_page": 1, "state": "open"})
    resp.raise_for_status()
    issues = resp.json()

    if not issues:
        return None

    issue = issues[0]
    return {
        "title": issue["title"],
        "url": issue["html_url"],
        "number": issue["number"],
        "created_at": issue["created_at"],
    }

if __name__ == "__main__":
    print("🔍 Checking for new issues...")

    latest = get_latest_issue(GITHUB_REPO)
    if latest:
        created_at = datetime.strptime(latest["created_at"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        now = datetime.utcnow().replace(tzinfo=timezone.utc)
        delta = now - created_at

        if delta < timedelta(minutes=5):
            msg = f"🚨 New Airflow Issue #{latest['number']}:\n{latest['title']}\n{latest['url']}"
            push_to_line(msg)
        else:
            print("✅ No issues created in the last 5 minutes.")