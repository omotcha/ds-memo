import faiss
import numpy as np
from embeddings_util import SentenceTransformerUtil
from configs.common import vector_dim


class FaissUtil:
    def __init__(self, data: list, tag):
        """
        faiss store constructor
        :param data: list of encoded vectors
        :param tag: index name
        """
        # use flat L2
        # self._index = faiss.IndexFlatL2(vector_dim)
        # self._index.add(data)

        # use flat ip
        self._index = faiss.IndexIDMap(faiss.IndexFlatIP(vector_dim))
        self._index.add_with_ids(data, np.array(range(0, len(data))))
        print(f"{self._index.ntotal} vectors added.")

        # write index
        # faiss.write_index(self._index, tag)

        self._embeddings_util = SentenceTransformerUtil()

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


def test_faiss():
    raw_query = "The identification of complex audio, including music, has proven to be complicated."
    raw_data = ["this is raw text",
                "you are right, but genshin impact is an open-world...",
                "The proposed framework is very flexible, so it could use instrument models with various complexity—more advanced for those with weaker results and more straightforward for those with better results."]
    embeddings_util = SentenceTransformerUtil()
    embedded_data = embeddings_util.encode(raw_data)
    faiss_util = FaissUtil(embedded_data, "example")
    print(faiss_util.search(raw_query, 1)[0])


if __name__ == '__main__':
    test_faiss()

