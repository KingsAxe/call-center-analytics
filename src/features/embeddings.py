# src/features/embeddings.py
from sentence_transformers import SentenceTransformer
import numpy as np

class VectorEngine:
    def __init__(self, model_name='all-mpnet-base-v2'):
        # MPNet is the gold standard for sentence embeddings in 2026
        self.model = SentenceTransformer(model_name)

    def generate_embeddings(self, texts: list):
        """Converts a list of transcripts into a matrix of embeddings."""
        print(f"Generating embeddings for {len(texts)} transcripts...")
        embeddings = self.model.encode(texts, show_progress_bar=True)
        return embeddings