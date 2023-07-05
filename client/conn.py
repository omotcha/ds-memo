from utils.crypto_config_util import *
from chainmaker.chain_client import ChainClient
from chainmaker.node import Node
from chainmaker.user import User
from chainmaker.utils import file_utils


class SimpleConn:
    """
    SimpleConn is a simple configuration consisting of 1 organization, 1 node and 1 user
    """
    def __init__(self, org: str, user: str):
        """
        initiate a simple chainmaker connection instance
        :param org: organization name, choose one using {project dir}/utils/crypto_config_util.py
        :param user: user name, choose one using {project dir}/utils/crypto_config_util.py
        """
        self._user = None
        self._org_name = org
        self._user_name = user
        self._cas_path = get_cas_path()
        self._user_certs_path = get_user_certs_path(org, user)

    def init_client(self):
        self._user = User(self._org_name,
                          sign_key_bytes=file_utils.read_file_bytes(self._user_certs_path["sign.key"]),
                          sign_cert_bytes=file_utils.read_file_bytes(self._user_certs_path["sign.crt"]),
                          tls_key_bytes=file_utils.read_file_bytes(self._user_certs_path["tls.key"]),
                          tls_cert_bytes=file_utils.read_file_bytes(self._user_certs_path["tls.crt"]))

    def test_simple_conn(self):
        print(self._cas_path)
        print(self._user_certs_path)


def test():
    test_org = get_orgs_name()[0]
    test_user = get_users_name(test_org)[0]
    conn = SimpleConn(test_org, test_user)
    conn.test_simple_conn()


if __name__ == '__main__':
    test()
