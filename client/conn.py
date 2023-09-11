from utils.crypto_config_util import *
from configs.secrets import conn_url, chain_id, conf
from configs.common import default_contract_name
from chainmaker.chain_client import ChainClient
from chainmaker.node import Node
from chainmaker.user import User
from chainmaker.utils import file_utils
from chainmaker.utils.evm_utils import calc_evm_contract_name, calc_evm_method_params


class SimpleConn:
    """
    SimpleConn is a simple configuration consisting of 1 organization, 1 node and 1 user
    """
    def __init__(self):
        """
        initiate a simple chainmaker connection util
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
        """
        initiate a client instance from given sdk_config.yml (path is hard encoded in secrets.py/conf)
        :return:
        """
        self._client = ChainClient.from_conf(conf)

    def init_client(self, org: str, user: str):
        """
        initiate a client instance from given organization name and user name
        :param org:
        :param user:
        :return:
        """
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
        # print(f"Chain client ({self._client.get_chainmaker_server_version()}) initiated.")

    def stop_client(self):
        """
        close the client instance
        :return:
        """
        self._client.stop()

    def invoke_contract(self, contract_name: str, method_name: str, params: list):
        evm_contract = calc_evm_contract_name(contract_name)
        evm_method, evm_params = calc_evm_method_params(method_name, params)
        resp = self._client.invoke_contract(evm_contract, evm_method, evm_params, with_sync_result=True)
        return resp

    def test_simple_conn(self):
        from eth_abi import decode_abi
        # self.invoke_contract(default_contract_name, "getIds", [])
        # self.invoke_contract(default_contract_name, "writeMemo", [{"uint256": "0"}, {"string": "About Omotcha"}, {"string": "Omotcha means toy in Japan."}, {"bool": True}])
        # self.invoke_contract(default_contract_name, "getIds", [])
        invoke_result = self.invoke_contract(default_contract_name, "getMemoItemById", [{"uint256": "0"}]).contract_result.result
        parse_result = decode_abi(("uint256", "string", "string"), bytes(invoke_result))
        print(parse_result)


def test():
    test_org = get_orgs_name()[0]
    test_user = get_users_name(test_org)[0]
    conn = SimpleConn()
    conn.init_client(test_org, test_user)
    conn.test_simple_conn()
    conn.stop_client()


if __name__ == '__main__':
    test()
