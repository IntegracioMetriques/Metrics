from .APInterface import APInterface
import requests

class api_get_commits(APInterface):
    def get_branches(self,headers,repo_name,owner_name):
        url = f"https://api.github.com/repos/{owner_name}/{repo_name}/branches"
        response = requests.get(url, headers=headers)
        return [branch['name'] for branch in response.json() if response.status_code == 200]
    
    def query_graphql(self,owner_name, repo_name, branch_name, header,data):
        url = "https://api.github.com/graphql"
        cursor = None 
        while True:
            query = """
            {
            repository(owner: "%s", name: "%s") {
                ref(qualifiedName: "refs/heads/%s") {
                target {
                    ... on Commit {
                    history(first: 100%s) {
                        edges {
                            node {
                                oid  
                                author {
                                name 
                                }
                                additions  
                                deletions 
                                changedFiles  
                            }
                            }
                            pageInfo {
                            hasNextPage
                            endCursor
                            }
                        }
                    }
                }
                }
            }
            }
                """ % (owner_name, repo_name, branch_name, f', after: "{cursor}"' if cursor else "")            
            
            response = requests.post(url, json={'query': query}, headers=header)
            data_graphql = response.json()
            
            if 'data' in data_graphql:
                commits_data_graphql = data_graphql['data']['repository']['ref']['target']['history']['edges']
                page_info = data_graphql['data']['repository']['ref']['target']['history']['pageInfo']
                
                for commit_data in commits_data_graphql:
                    commit = commit_data['node']
                    sha = commit['oid']
                    autor = commit['author']['name']
                    additions = commit['additions']
                    deletions = commit['deletions']
                    modified_lines = additions + deletions
                    if sha not in data:
                        data[sha] = {
                            "author": autor,
                            "additions": additions,
                            "deletions": deletions,
                            "modified": modified_lines
                        }

                if page_info['hasNextPage']:
                    cursor = page_info['endCursor']
                else:
                    break
        
        return data

    def execute(self, owner_name, repo_name, headers, members, data):
        branches = self.get_branches(headers,repo_name,owner_name)
        commits_per_member = {member: 0 for member in members}
        modified_lines_per_member = {
                member: {
                    "additions": 0,
                    "deletions": 0,
                    "modified": 0
                }
            for member in members
            }
        anonymous_commits = 0    
        total_commits = 0
        total_additions = 0
        total_deletions = 0
        total_modified = 0
        data = {}
        commits = {}
        for branch in branches:
            commits = self.query_graphql(owner_name, repo_name,branch,headers,commits)
        for _,commit in commits.items():
            if commit['author'] in commits_per_member:
                commits_per_member[commit['author']] +=1
                modified_lines_per_member[commit['author']]['additions'] += commit['additions']
                total_additions += commit['additions'] 
                modified_lines_per_member[commit['author']]['deletions'] += commit['deletions']
                total_deletions += commit['deletions'] 
                modified_lines_per_member[commit['author']]['modified'] += commit['modified']
                total_modified += commit['modified']
                total_commits +=1
            elif commit['author'] != "github-actions[bot]":
                anonymous_commits += 1
                total_commits +=1
        commits_per_member["anonymous"] = anonymous_commits
        commits_per_member["total"] = total_commits
        modified_lines_per_member["total"] = {
                    "additions": total_additions,
                    "deletions": total_deletions,
                    "modified": total_modified
                }
        data["commits"] = commits_per_member
        data["modified_lines"] = modified_lines_per_member
        return data
