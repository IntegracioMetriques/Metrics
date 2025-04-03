from .CollectorBase import CollectorBase

class CollectCommitsMetrics(CollectorBase):
    def execute(self, data: dict, metrics: dict, members) -> dict:
        commits = data['commits']
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
        metrics["commits"] = commits_per_member
        metrics["modified_lines"] = modified_lines_per_member
        return metrics