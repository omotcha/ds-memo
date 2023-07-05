import os
import faiss

# project structure
configs_dir = os.path.abspath(os.path.dirname(__file__))
project_dir = os.path.split(configs_dir)[0]
models_dir = os.path.join(project_dir, "models")
secrets_dir = os.path.join(project_dir, "secrets")
crypto_config_dir = os.path.join(secrets_dir, "crypto-config")

# embeddings option
embedding_model_name = "simcse"
vector_dim = 768
