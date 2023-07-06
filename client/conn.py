from utils.crypto_config_util import *
from configs.secrets import conn_url, chain_id, conf
from chainmaker.chain_client import ChainClient
from chainmaker.node import Node
from chainmaker.user import User
from chainmaker.utils import file_utils


class SimpleConn:
    """
    SimpleConn is a simple configuration consisting of 1 organization, 1 node and 1 user
    """
    def __init__(self):
        """
        initiate a simple chainmaker connection instance
        """
        self._user_certs_path = None
        self._cas_path = None
        self._user_name = None
        self._org_name = None
        self._client = None
        self._node = None
        self._user = None
        self._chain_id = chain_id

    def init_client_from_conf(self):
        self._client = ChainClient.from_conf(conf)

    def init_client(self, org: str, user: str):
        self._org_name = org
        self._user_name = user
        self._cas_path = get_cas_path()
        self._user_certs_path = get_user_certs_path(org, user)
        self._user = User(self._org_name,
                          sign_key_bytes=file_utils.read_file_bytes(self._user_certs_path["sign.key"]),
                          sign_cert_bytes=file_utils.read_file_bytes(self._user_certs_path["sign.crt"]),
                          tls_key_bytes=file_utils.read_file_bytes(self._user_certs_path["sign.key"]),
                          tls_cert_bytes=file_utils.read_file_bytes(self._user_certs_path["sign.crt"]))

        self._node = Node(
            node_addr=conn_url,
            conn_cnt=1,
            enable_tls=False,
            trust_cas=[file_utils.read_file_bytes(crt_file) for crt_file in self._cas_path],
            tls_host_name=self._org_name
        )
        self._client = ChainClient(
            chain_id=self._chain_id,
            user=self._user,
            nodes=[self._node]
        )
        print(f"Chain client ({self._client.get_chainmaker_server_version()}) initiated.")

    def stop_client(self):
        self._client.stop()

    def test_simple_conn(self):
        print(self._cas_path)
        print(self._user_certs_path)


def test():
    test_org = get_orgs_name()[0]
    test_user = get_users_name(test_org)[1]
    conn = SimpleConn()
    conn.init_client(test_org, test_user)
    conn.stop_client()


if __name__ == '__main__':
    test()
