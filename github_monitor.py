import time
import requests
from utils.line import push_to_line

GITHUB_REPO = "apache/airflow"
ISSUE_TRACK_FILE = "last_issue.txt"

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
    }

def load_last_issue_id():
    try:
        with open(ISSUE_TRACK_FILE, "r") as f:
            return int(f.read().strip())
    except:
        return 0

def save_last_issue_id(issue_id):
    with open(ISSUE_TRACK_FILE, "w") as f:
        f.write(str(issue_id))

if __name__ == "__main__":
    while True:
        print("🔍 Checking for new issues...")
        latest = get_latest_issue(GITHUB_REPO)
        if latest:
            last_id = load_last_issue_id()
            if latest["number"] > last_id:
                msg = f"🚨 New Airflow Issue #{latest['number']}:\n{latest['title']}\n{latest['url']}"
                push_to_line(msg)
                save_last_issue_id(latest["number"])
            else:
                print("✅ No new issues.")
        time.sleep(300)  # 每 5 分鐘查一次（300 秒）