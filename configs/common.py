import os

configs_dir = os.path.abspath(os.path.dirname(__file__))
project_dir = os.path.split(configs_dir)[0]
models_dir = os.path.join(project_dir, "models")
model_name = "simcse"
