from sentence_transformers import SentenceTransformer
from configs.common import models_dir
import os


class SentenceTransformerUtil:
    def __init__(self):
        self.model = SentenceTransformer(os.path.join(models_dir, "simcse"))

    def get_embeddings(self, sentence):
        return self.model.encode(sentence)


def test_get_sentence_transformer_embeddings():
    util = SentenceTransformerUtil()
    sentence = "test sentence"
    print(util.get_embeddings(sentence))


if __name__ == '__main__':
    test_get_sentence_transformer_embeddings()
