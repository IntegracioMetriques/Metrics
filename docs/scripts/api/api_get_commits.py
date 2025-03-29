from .APInterface import APInterface
import requests
from collections import defaultdict

class api_get_commits(APInterface):
    def get_branches(self,headers,repo_name,owner_name):
        url = f"https://api.github.com/repos/{owner_name}/{repo_name}/branches"
        response = requests.get(url, headers=headers)
        return [branch['name'] for branch in response.json() if response.status_code == 200]


    def execute(self, owner_name, repo_name, headers, members, data):
        branches = self.get_branches(headers,repo_name,owner_name)
        commits = set()
        commits_per_member = {member: 0 for member in members}   
        anonymous_commits = 0    
        total_commits = 0
        for branch in branches:
            page = 1
            while True:
                url = f"https://api.github.com/repos/{owner_name}/{repo_name}/commits?sha={branch}&per_page=100&page={page}"
                response = requests.get(url, headers=headers)

                if response.status_code != 200 or not response.json():
                    break 

                for commit in response.json():
                    sha = commit['sha']
                    autor = commit['commit']['author']['name']

                    if sha not in commits:
                        commits.add(sha)
                        if autor in members:
                            commits_per_member[autor] += 1
                        else:
                            anonymous_commits += 1
                        total_commits += 1 
                        
                page += 1 
            commits_per_member["anonymous"] = anonymous_commits
            commits_per_member["total"] = total_commits
        data["commits"] = commits_per_member
        return data
