import os

project_dir = os.path.abspath(os.path.dirname(__file__))
models_dir = os.path.join(project_dir, "models")
secret_dir = os.path.join(project_dir, "secrets")
secret_config_dir = os.path.join(secret_dir, "secret-config")


def setup_project():
    # setup models
    if "models" not in os.listdir(project_dir):
        os.mkdir(models_dir)
    # setup secrets
    if "secrets" not in os.listdir(project_dir):
        os.mkdir(secret_dir)
    # setup secret-config
    if "secret-config" not in os.listdir(secret_dir):
        os.mkdir(secret_config_dir)


def setup_secrets(chain_id: str, url: str):
    if chain_id not in os.listdir(secret_config_dir):
        with open(os.path.join(secret_config_dir, chain_id), "w") as f:
            f.writelines(url)


if __name__ == '__main__':
    setup_project()
    setup_secrets("test", "127.0.0.1:8888")

