import os
import pickle
import faiss
import numpy as np

class VectorDB:
    def __init__(self, dimension=384):
        self.dimension = dimension

        if os.path.exists("data/faiss_index.bin"):
            self.index = faiss.read_index("data/faiss_index.bin")
            with open("data/payloads.pkl", "rb") as f:
                self.payloads = pickle.load(f)
                print(type(next(iter(self.payloads.keys()))))
            self.next_id = len(self.payloads)
            print("Loaded FAISS index")
            print("Vectors in index:", self.index.ntotal)
        else:
            self.index = faiss.IndexFlatIP(dimension)
            self.payloads = {}
            self.next_id = 0
            print("Created empty FAISS index")

    def store(self, vectors, payloads):
        vectors_np = np.array(vectors).astype('float32')
        faiss.normalize_L2(vectors_np)
        self.index.add(vectors_np)
        for i, payload in enumerate(payloads):
            self.payloads[self.next_id + i] = payload
        self.next_id += len(payloads)
        
    
    def save(self):
            faiss.write_index(self.index,"data/faiss_index.bin")
            with open("data/payloads.pkl", "wb") as f:
                pickle.dump(self.payloads, f)

    def search(self, query_vector, top_k=5):
        query_np = np.array(query_vector).astype('float32')
        if len(query_np.shape) == 1:
            query_np = query_np.reshape(1, -1)
        faiss.normalize_L2(query_np)
        print("FAISS Query Shape:", query_np.shape)
        distances, indices = self.index.search(query_np, top_k)
        print("Distances:", distances)
        print("Indices:", indices)
        results = []
        for i, idx in enumerate(indices[0]):
            if idx == -1:
                continue
            score = distances[0][i]
            print(
                f"Rank {i+1}: "
                f"ID={idx} "
                f"Score={score:.4f}"
                )
            payload = self.payloads.get(int(idx))
            if payload:
                print(self.payloads[idx]["content"][:300])
                print("-" * 50)
                results.append({
                "id": int(idx),
                "payload": payload,
                "score": score
                })
        return results

        