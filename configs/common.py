import os

# project structure
configs_dir = os.path.abspath(os.path.dirname(__file__))
project_dir = os.path.split(configs_dir)[0]
models_dir = os.path.join(project_dir, "models")
secrets_dir = os.path.join(project_dir, "secrets")
client_dir = os.path.join(project_dir, "client")
logs_dir = os.path.join(project_dir, "logs")

# embeddings options
embedding_model_name = "simcse"
vector_dim = 768

# contract info (do not modify)
default_contract_name = "memosolo_0_0_3"

# memo options
override_memo = True
