import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import argparse
from eth_abi import decode_abi
from utils.crypto_config_util import *
from utils.faiss_util import FaissUtil
from client.conn import SimpleConn
from configs.common import client_dir, override_memo, default_contract_name, query_top_k
from configs.logging import LOGGING_CONFIG

import logging.config

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
        self._tag = tag

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

    def search_memo(self, query: str, top_k: int) -> list:
        """
        memo search
        :param top_k:
        :param query:
        :return:
        """
        query_result = self._faiss.search(query, top_k)[0]
        result = []
        for memo_id in query_result:
            if memo_id < 0:
                break
            invoke_result = self._conn.invoke_contract(
                default_contract_name,
                "getMemoItemById",
                [{"uint256": f"{memo_id}"}]).contract_result.result
            parse_result = decode_abi(("uint256", "string", "string"), bytes(invoke_result))
            result.append(parse_result[2])
        return result

    def sync(self):
        """
        sync titles from chain and reconstruct faiss store
        :return:
        """
        # remove faiss store if exists
        if self._tag in os.listdir(client_dir):
            os.remove(os.path.join(client_dir, self._tag))
        # reset index
        self._faiss.reset()

        # fetch titles and ids from chain
        invoke_result = self._conn.invoke_contract(
            default_contract_name,
            "getAllTitlesWithIds",
            []
        ).contract_result.result

        # dev checkpoint: parse result should be like ((a,b,c),(1,2,3))
        parse_titles, parse_ids = decode_abi(("string[]", "uint256[]"), bytes(invoke_result))
        self._faiss.add(list(parse_titles), list(parse_ids))
        self._faiss.save()

    def test_memo(self):
        # self.add_memo("About omotcha", "Omotcha means toy in Japanese")
        # self.add_memo("About Genshin Impact", "You are right, but Genshin Impact is an open-world action RPG...")
        # search_result = self.search_memo("omotcha")
        # search_result = self.search_memo("genshin, game start")
        # print(search_result)
        self.sync()


if __name__ == '__main__':
    logging.config.dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger(__name__)

    test_org = get_orgs_name()[0]
    test_user = get_users_name(test_org)[0]
    app = Memo(test_org, test_user, "test")

    parser = argparse.ArgumentParser(description="ds-memo")
    parser.add_argument("task", choices=['add', 'query', 'sync'])
    parser.add_argument("-t", "--title", type=str, default=None)
    parser.add_argument("-c", "--content", type=str, default=None)
    parser.add_argument("-k", "--top", type=int, default=1)
    args = parser.parse_args()

    if args.task == "add":
        if args.title is None:
            print("Error: Title missing.")
        elif args.content is None:
            print("Error: Content missing.")
        else:
            app.add_memo(args.title, args.content)
    elif args.task == "query":
        if args.title is None:
            print("Error: Title missing.")
        else:
            print(app.search_memo(args.title, args.top))
    elif args.task == "sync":
        app.sync()
    else:
        print("Error: Wrong task.")
    print(args)

