from .APInterface import APInterface
import requests

class api_get_collaborators(APInterface):
    def execute(self, owner_name, repo_name, headers, data):
        url = f"https://api.github.com/repos/{owner_name}/{repo_name}/collaborators"
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            raise  requests.RequestException(f"Error al fer la trucada a {self.__class__.__name__}: {response.status_code}")
        
        collaborators_data = response.json()
        collaborators = [obj['login'] for obj in collaborators_data]
        return collaborators