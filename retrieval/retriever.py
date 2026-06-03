

from embedding.embedder import Embedder
from storage.vector_db import VectorDB
from retrieval.ranker import Reranker

import numpy as np
class Retriever:
    def __init__(self):
        self.embedder = Embedder()
        self.reranker = Reranker()
        self.vector_db = VectorDB()
        

    def retrieve(self, query, top_k=5):
        query_vector = self.embedder.model.encode(query,normalize_embeddings=True)
        print("Query vector shape:", query_vector.shape)
        print("Vectors in index:", self.vector_db.index.ntotal)
        
        results = self.vector_db.search(query_vector, top_k)
        
        retrieved_docs = []
        for result in results:
            retrieved_docs.append({
                        "chunk_id": result["payload"]["chunk_id"],
                        "content": result["payload"]["content"],
                        "metadata": result["payload"],
                        "score": result["score"]
            })
            print(f"ID: {result['id']}")
            print(f"Score: {result['score']:.4f}")
        retrieved_docs = self.reranker.rank(query,retrieved_docs)
        if not results:
            return []
        
        top_score=results[0]["score"]
        if top_score<0.4:
            return []
        
        seen = set()
        unique_docs = []
        for doc in retrieved_docs:
            key = doc["content"][:100]
            if key not in seen:
                seen.add(key)
                unique_docs.append(doc)
        for i, doc in enumerate(retrieved_docs, start=1):
            print(f"\nDoc {i}")
            print("FAISS Score :", doc["score"])
            print("Rerank Score:", doc["rerank_score"])
            print(doc["content"][:300])

        if not retrieved_docs:
            return[]

        return retrieved_docs
