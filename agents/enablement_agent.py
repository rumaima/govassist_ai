from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

class EnablementAgent:
    def __init__(self):
        model_name = "all-MiniLM-L6-v2"
        self.model = SentenceTransformer(model_name)

        self.chroma_client = chromadb.Client()
        self.collection = self.chroma_client.create_collection(
            name="jobs",
            embedding_function=SentenceTransformerEmbeddingFunction(model_name=model_name)
        )
        self._populate_jobs()

    def _populate_jobs(self):
        jobs = [
            {"id": "1", "title": "Retail Assistant", "desc": "customer service, cashier, sales"},
            {"id": "2", "title": "Warehouse Operator", "desc": "inventory handling, packing, lifting"},
            {"id": "3", "title": "Data Entry Clerk", "desc": "typing, Excel, data accuracy"},
            {"id": "4", "title": "Call Center Agent", "desc": "communication, empathy, phone calls"},
            {"id": "5", "title": "Junior Web Developer", "desc": "HTML, CSS, JavaScript"}
        ]

        for job in jobs:
            self.collection.add(
                documents=[job["desc"]],
                metadatas=[{"title": job["title"]}],
                ids=[job["id"]]
            )

    def recommend(self, resume_text, top_k=3):
        if not resume_text.strip():
            return []

        results = self.collection.query(
            query_texts=[resume_text],
            n_results=top_k
        )

        return [
            {
                "job_title": meta["title"],
                "relevance": round(dist, 2)
            }
            for meta, dist in zip(results["metadatas"][0], results["distances"][0])
    ]