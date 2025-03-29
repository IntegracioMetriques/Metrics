import os
import json
import api
from api import api_get_members, api_get_collaborators

required_fields = {
    "metrics_scope": str,
    "members": str,
    "excluded_members": list,
    "excluded_repos":list
}

valid_metrics_scope = ["org","repo"]
valid_members = ["org","repo"]

class ConfigError(Exception):
    pass

def load_env_local(path):
    with open(path, 'r') as f:
        variables = json.load(f)
        for key, value in variables.items():
            os.environ[key] = value

def validar_config(config):
    for field,data_type in required_fields.items():
        if field not in config:
            raise ConfigError(f"Error: Falta el camp obligatori '{field}' a config.json")
        if not isinstance(config[field],data_type):
            raise ConfigError(f"Error: El camp obligatori '{field}' de config.json ha de ser de tipus {data_type.__name__}")

    if config["metrics_scope"] not in valid_metrics_scope:
        raise ConfigError(f"Error: El camp obligatori 'metrics_scope' de config.json no té un valor vàlid. Valors vàlids: {valid_metrics_scope}")
    if config["members"] not in valid_members:
        raise ConfigError(f"Error: El camp obligatori 'members' de config.json no té un valor vàlid. Valors vàlids: {valid_members}")


def main():
    env_path = "env.json"
    if os.path.exists(env_path):
        load_env_local(env_path)
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    ORG_TOKEN = os.getenv("ORG_TOKEN")
    REPO = os.getenv("GITHUB_REPOSITORY")
    REPO_OWMER,REPO_NAME = os.getenv("GITHUB_REPOSITORY").split("/")
    HEADERS_REPO = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Content-Type": "application/json"
        }
    HEADERS_ORG = {
        "Authorization": f"token {ORG_TOKEN}",
        "Content-Type": "application/json"
        }

    config_path = "../config.json"
    if os.path.exists(config_path):
        with open(config_path,'r') as f:
            config = json.load(f)
    else:
        raise FileNotFoundError("Arxiu config.json no trobat.")
    validar_config(config)

    members = []
    if config['members'] == "org":
        instance = api_get_members()
        members = instance.execute(REPO_OWMER,REPO_NAME,HEADERS_ORG,[],{})
    else: 
        instance = api_get_collaborators()
        members = instance.execute(REPO_OWMER,REPO_NAME,HEADERS_ORG,[],{})
    metrics_path = "../metrics.json"
    if os.path.exists(metrics_path):
        with open(metrics_path,'r') as f:
            data = json.load(f)
    else:
        data = {}

    instances = []
    for class_name, class_obj in api.__dict__.items():
        if isinstance(class_obj, type) and class_name.startswith("api") and class_name not in ["api_get_collaborators","api_get_members"]:
            instances.append(class_obj())

    for instance in instances:
       data = instance.execute(REPO_OWMER,REPO_NAME,HEADERS_ORG,members,data)
    
    with open(metrics_path, "w") as f:
        json.dump(data, f, indent=4)
if __name__ == "__main__":
    main()