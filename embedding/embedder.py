from sentence_transformers import SentenceTransformer
class Embedder:
    def __init__(self):
        EMBEDDING_MODEL="multi-qa-MiniLM-L6-cos-v1"
        self.model = SentenceTransformer(EMBEDDING_MODEL)
    def encode(self, texts):
        return self.model.encode(texts).tolist()