import os
from configs.common import secrets_dir

crypto_config_dir = os.path.join(secrets_dir, "crypto-config")
secret_config_dir = os.path.join(secrets_dir, "secret-config")

chain_id = os.listdir(secret_config_dir)[0]

with open(os.path.join(secret_config_dir, chain_id), 'r') as f:
    conn_url = f.readline()

conf = os.path.join(secrets_dir, "sdk_config.yml")
