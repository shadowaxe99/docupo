from github import Github
from os import getenv

GITHUB_API_KEY = getenv("GITHUB_API_KEY")

class GithubIntegration:
    def __init__(self):
        self.github = Github(GITHUB_API_KEY)

    def create_github_repo(self, repo_name):
        user = self.github.get_user()
        return user.create_repo(repo_name)

    def commit_and_push(self, repo, file_path, commit_message):
        with open(file_path, 'r') as file:
            content = file.read()

        repo.create_file(file_path, commit_message, content)

    def push_to_github(self, repo_structure, repo_name):
        repo = self.create_github_repo(repo_name)

        for file_path in repo_structure:
            self.commit_and_push(repo, file_path, "Initial commit")

github_integration = GithubIntegration()
```