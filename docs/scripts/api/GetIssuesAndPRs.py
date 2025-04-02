from .APInterface import APInterface
import requests
import json

class GetIssuesAndPRs(APInterface):
    def execute(self, owner_name, repo_name, headers, data):
        page = 1
        issues = {}
        pull_requests = {}
        while True:
            url = f"https://api.github.com/repos/{owner_name}/{repo_name}/issues?state=all&per_page=100&page={page}"
            response = requests.get(url, headers=headers)

            if response.status_code != 200:
                raise  requests.RequestException(f"Error al fer la trucada a {self.__class__.__name__}: {response.status_code}")

            issues_data = response.json()

            if not issues_data:
                break
            for issue_data in issues_data:
                assignees = []
                for assignee in issue_data['assignees']:
                    assignees.append(assignee['login'])
                if 'pull_request' in issue_data:
                    pull_requests[issue_data['id']] = {
                        "author": issue_data['user']['login'],
                        "assignee":issue_data['assignee']['login'] if issue_data['assignee'] is not None else None,
                        "assignees": assignees,
                        "state": issue_data['state'],
                        "merged" : issue_data['pull_request']['merged_at'] != None,
                        "merged_by": issue_data['closed_by']['login'] if issue_data['closed_by'] is not None and issue_data['pull_request']['merged_at'] != None else None
                    }
                else: 
                    issues[issue_data['id']] = {
                        "author": issue_data['user']['login'],
                        "assignee":issue_data['assignee']['login'] if issue_data['assignee'] is not None else None,
                        "assignees": assignees,
                        "state": issue_data['state']
                        }
            page += 1     
        data['issues'] = issues
        data['pull_requests'] = pull_requests
        return data