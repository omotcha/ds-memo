from sentence_transformers import SentenceTransformer
from configs.common import models_dir, embedding_model_name
import os


class SentenceTransformerUtil:
    def __init__(self):
        self.model = SentenceTransformer(os.path.join(models_dir, embedding_model_name))

    def get_embeddings(self, sentence: str or list):
        return self.model.encode(sentence)


def test_get_sentence_transformer_embeddings():
    util = SentenceTransformerUtil()
    sentence = ["test sentence 1", "test sentence 2"]
    print(len(util.get_embeddings(sentence)[0]))


if __name__ == '__main__':
    test_get_sentence_transformer_embeddings()
