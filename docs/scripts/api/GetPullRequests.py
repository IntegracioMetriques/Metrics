from .APInterface import APInterface
import requests

class GetPullRequests(APInterface):
    def query_graphql(self,owner_name, repo_name, headers):
        url = "https://api.github.com/graphql"
        cursor = None
        data = {}

        while True:
            query = """
            {
            repository(owner: "%s", name: "%s") {
                pullRequests(first: 100%s) {
                nodes {
                    id
                    state
                    merged
                    mergedBy {
                    login
                    }
                }
                pageInfo {
                    hasNextPage
                    endCursor
                }
                }
            }
            }
            """ % (owner_name, repo_name, f', after: "{cursor}"' if cursor else "")

            response = requests.post(url, json={'query': query}, headers=headers)
            if response.status_code != 200:
                raise  requests.RequestException(f"Error al fer la trucada a {self.__class__.__name__}: {response.status_code}")
            data_graphql = response.json()

            if 'data' in data_graphql:
                pr_data = data_graphql['data']['repository']['pullRequests']['nodes']
                page_info = data_graphql['data']['repository']['pullRequests']['pageInfo']

                for pr in pr_data:
                    pr_id = pr['id']
                    state = pr['state']
                    merged = pr['merged']
                    merged_by = pr['mergedBy']['login'] if merged else None

                    data[pr_id] = {
                        "state": state,
                        "merged": merged,
                        "merged_by": merged_by
                    }

                if page_info['hasNextPage']:
                    cursor = page_info['endCursor']
                else:
                    break

        return data

    def execute(self, owner_name, repo_name, headers, data: dict) -> dict:
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

        if "issues" in data:
            data["issues"].update(issues)
        else:
            data["issues"] = issues

        if "pull_requests" in data:
            data["pull_requests"].update(pull_requests)
        else:
            data["pull_requests"] = pull_requests
        return data