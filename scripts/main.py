# scripts/main.py
import os
import csv
import openai
from github import Github

GITHUB_TOKEN = os.getenv("GH_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
g = Github(GITHUB_TOKEN)
openai.api_key = OPENAI_API_KEY

def generate_comment(title, body, repo_name):
    prompt = f"""
You are moksh1tha, a friendly and skilled open source contributor.
Your skills: MERN stack, React, Next.js, Node, Express, MongoDB, HTML, CSS, UI/UX design.

Generate a short, personalized comment asking to be assigned this GitHub issue.

Repo: {repo_name}
Issue title: {title}
Issue body: {body[:500]}
"""
    res = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt}],
        temperature=0.7
    )
    return res.choices[0].message.content.strip()

def main():
    with open("data/repos.csv") as f:
        repos = [row["repo"] for row in csv.DictReader(f)]

    for repo_name in repos:
        try:
            repo = g.get_repo(repo_name)
            issues = repo.get_issues(state="open")
            for issue in issues:
                if issue.pull_request is None and issue.comments == 0:
                    comment = generate_comment(issue.title, issue.body or "", repo_name)
                    issue.create_comment(comment)
                    print(f"✅ Commented on {repo_name} #{issue.number}")
        except Exception as e:
            print(f"❌ Error processing {repo_name}: {e}")

if __name__ == "__main__":
    main()
