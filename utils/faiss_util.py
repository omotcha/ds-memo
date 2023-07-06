import faiss
import numpy as np
from embeddings_util import SentenceTransformerUtil
from configs.common import vector_dim


class FaissUtil:
    def __init__(self, tag):
        """
        faiss store constructor
        :param tag: index name
        """
        # uses flat ip
        self._index = faiss.IndexIDMap(faiss.IndexFlatIP(vector_dim))
        self._tag = tag if type(tag) is str else "default"
        self._embeddings_util = SentenceTransformerUtil()

    def load(self):
        """
        load an index (and replace current index)
        :return:
        """
        self._index = faiss.read_index(self._tag)

    def save(self):
        """
        save an index
        :return:
        """
        faiss.write_index(self._index, self._tag)

    def add(self, item: str or list, item_id: int or list):
        """
        add an item into index
        :param item_id: item id
        :param item: raw string
        :return:
        """
        if type(item) is str:
            item = [item]
        if type(item_id) is int:
            item_id = [item_id]
        self._index.add_with_ids(self._embeddings_util.encode(item), np.array(item_id))

    def get_index_size(self):
        return self._index.ntotal

    def search(self, query: str or list, top_k: int = 1):
        """
        semantic search
        :param query: raw text of query
        :param top_k:
        :return:
        """
        if type(query) is str:
            query = [query]
        query_vector = self._embeddings_util.encode(query)
        _, result = self._index.search(query_vector, top_k)
        return result


def test_save():
    raw_data = ["this is raw text",
                "you are right, but genshin impact is an open-world..."]
    util = FaissUtil("test")
    util.add(raw_data, [0, 1])
    util.save()


def test_load():
    raw_query = "The identification of complex audio, including music, has proven to be complicated."
    util = FaissUtil("test")
    util.load()
    print(util.search(raw_query, 1))


def test_add():
    raw_query = "The identification of complex audio, including music, has proven to be complicated."
    util = FaissUtil("test")
    util.load()
    size = util.get_index_size()
    new_item = "The proposed framework is very flexible, so it could use instrument models with various complexity—more advanced for those with weaker results and more straightforward for those with better results."
    util.add(new_item, size)
    print(util.search(raw_query, 1))
    print(util.get_index_size())


if __name__ == '__main__':
    # test_save()
    # test_load()
    test_add()

