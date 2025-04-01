import os
import json
import api
import metricsCollectors
import concurrent.futures
from api import GetCollaborators,GetMembers

PARALLELISM = True

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
    REPO_OWNER,REPO_NAME = os.getenv("GITHUB_REPOSITORY").split("/")
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
    
    metrics_path = "../metrics.json"
    instances = []
    for class_name, class_obj in api.__dict__.items():
        if isinstance(class_obj, type) and class_name.startswith("Get") and class_name not in ["GetMembers","GetCollaborators"]:
            instances.append(class_obj())
    data = {}
    if config['members'] == "org": instances.append(GetMembers())
    else: instances.append(GetCollaborators())
    if not PARALLELISM:
        pass
        for instance in instances:
            data = instance.execute(REPO_OWNER,REPO_NAME,HEADERS_ORG,data)
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(instance.execute, REPO_OWNER, REPO_NAME, HEADERS_ORG, data) for instance in instances]

            for future in concurrent.futures.as_completed(futures):
                data = future.result()
    instances = []
    for class_name, class_obj in metricsCollectors.__dict__.items():
        if isinstance(class_obj, type) and class_name.startswith('Collect') and not bool(getattr(class_obj, "__abstractmethods__", False)):
            instances.append(class_obj())
    members = data['members']  
    metrics = {}
    for instance in instances:
       metrics = instance.execute(data,metrics,members)
    with open(metrics_path, "w") as f:
        json.dump(metrics, f, indent=4)

if __name__ == "__main__":
    main()