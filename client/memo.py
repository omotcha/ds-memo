from eth_abi import decode_abi
from utils.crypto_config_util import *
from utils.faiss_util import FaissUtil
from client.conn import SimpleConn
from configs.common import client_dir, override_memo, default_contract_name, query_top_k


class Memo:
    """
    the memo app logic
    """

    def __init__(self, org: str, user: str, tag: str):
        """
        init memo app
        :param org:
        :param user:
        """
        self._conn = SimpleConn()
        self._conn.init_client(org, user)
        self._faiss = FaissUtil(tag)

        # faiss::load index
        if tag not in os.listdir(client_dir):
            self._faiss.save()
        self._faiss.load()

    def add_memo(self, title: str, content: str):
        """
        add a memo
        Currently memo in faiss do not support content substitution,
        it means that writing memos with same title would contaminate the faiss store.
        A solution to this is to reconstruct faiss store using sync()
        :param title:
        :param content:
        :return:
        """
        memo_id = self._faiss.get_index_size()
        # add title to faiss store
        self._faiss.load()
        self._faiss.add(title, memo_id)
        self._faiss.save()
        # add record to chain
        self._conn.invoke_contract(
            default_contract_name,
            "writeMemo",
            [{"uint256": f"{memo_id}"}, {"string": f"{title}"}, {"string": f"{content}"}, {"bool": override_memo}]
        )

    def search_memo(self, query: str):
        query_result = self._faiss.search(query, query_top_k)[0]
        for memo_id in query_result:
            if memo_id < 0:
                break
            invoke_result = self._conn.invoke_contract(
                default_contract_name,
                "getMemoItemById",
                [{"uint256": f"{memo_id}"}]).contract_result.result
            parse_result = decode_abi(("uint256", "string", "string"), bytes(invoke_result))
            print(parse_result[2])

    def sync(self):
        """
        sync titles from chain and reconstruct faiss store
        WIP
        :return:
        """
        pass

    def test_memo(self):
        # self.add_memo("About omotcha", "Omotcha means toy in Japanese")
        self.search_memo("omotcha")


if __name__ == '__main__':
    test_org = get_orgs_name()[0]
    test_user = get_users_name(test_org)[0]
    app = Memo(test_org, test_user, "test")
    app.test_memo()
