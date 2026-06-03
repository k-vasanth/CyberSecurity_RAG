from sentence_transformers import SentenceTransformer
class Embedder:
    def __init__(self):
        EMBEDDING_MODEL="all-MiniLM-L6-v2"
        self.model = SentenceTransformer(EMBEDDING_MODEL)
    def encode(self, texts):
        return self.model.encode(texts).tolist()