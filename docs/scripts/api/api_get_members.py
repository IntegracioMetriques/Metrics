from .APInterface import APInterface
import requests

class api_get_members(APInterface):
    def execute(self, owner_name, repo_name, headers, members, data):
        url = f" https://api.github.com/orgs/{owner_name}/members"
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            raise  requests.RequestException(f"Error al fer la trucada a {self.__class__.__name__}: {response.status_code}")
        members_data = response.json()
        members = [obj['login'] for obj in members_data]
        return members