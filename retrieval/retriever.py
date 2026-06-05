from embedding.embedder import Embedder
from storage.vector_db import VectorDB
from retrieval.ranker import Reranker
from retrieval.query_rewriter import QueryRewriter

import numpy as np
class Retriever:
    def __init__(self):
        self.embedder = Embedder()
        self.reranker = Reranker()
        self.vector_db = VectorDB()
        self.query_rewriter = QueryRewriter()

    def retrieve(self, query, top_k=5):
        query = self.query_rewriter.rewrite(query)
        query_vector = self.embedder.model.encode(query,normalize_embeddings=True)
        print("Query vector shape:", query_vector.shape)
        print("Vectors in index:", self.vector_db.index.ntotal)
        
        results = self.vector_db.search(query_vector, top_k)
        if not results:
            return []
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
        top_score=retrieved_docs[0]["rerank_score"]
        if top_score<0.4:
            return []
        
        seen = set()
        unique_docs = []
        for doc in retrieved_docs:
            key = doc["content"][:100]
            if key not in seen:
                seen.add(key)
                unique_docs.append(doc)
        retrieved_docs = unique_docs[:top_k]
        for i, doc in enumerate(retrieved_docs, start=1):
            print(f"\nDoc {i}")
            print("FAISS Score :", doc["score"])
            print("Rerank Score:", doc["rerank_score"])
            print(doc["content"][:300])


        return retrieved_docs
    
