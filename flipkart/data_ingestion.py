# flipkart/data_ingestion.py

import os
import pandas as pd
from langchain_core.documents import Document
from langchain_astradb import AstraDBVectorStore
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from flipkart.config import Config


class DataConverter:
    """Converts raw Flipkart product review CSV data into LangChain Document objects."""
    def __init__(self, csv_path: str):
        self.csv_path = csv_path

    def convert(self):
        if not os.path.exists(self.csv_path):
            raise FileNotFoundError(f"CSV file not found at {self.csv_path}")

        df = pd.read_csv(self.csv_path)
        documents = []

        for _, row in df.iterrows():
            product = row.get("product_name", "")
            review = row.get("review_text", "")
            rating = row.get("rating", "")

            content = f"Product: {product}\nReview: {review}\nRating: {rating}"
            metadata = {"product": product, "rating": rating}
            documents.append(Document(page_content=content, metadata=metadata))

        return documents


class DataIngestor:
    """Handles embedding and ingestion of documents into AstraDB Vector Store."""
    def __init__(self):
        # ✅ Use HuggingFace API token from config.py
        hf_token = Config.HF_TOKEN or Config.HUGGINGFACEHUB_API_TOKEN
        if not hf_token:
            raise ValueError("❌ Missing HF_TOKEN / HUGGINGFACEHUB_API_TOKEN in environment or config.")

        # Hugging Face embeddings
        self.embedding = HuggingFaceEndpointEmbeddings(
            model=Config.EMBEDDING_MODEL,
            huggingfacehub_api_token=hf_token
        )

        # AstraDB Vector Store
        self.vstore = AstraDBVectorStore(
            embedding=self.embedding,
            collection_name="flipkart_database",
            api_endpoint=Config.ASTRA_DB_API_ENDPOINT,
            token=Config.ASTRA_DB_APPLICATION_TOKEN,
            namespace=Config.ASTRA_DB_KEYSPACE,
        )

    def ingest(self, load_existing=True):
        if load_existing:
            print("✅ Loading existing vector store...")
            return self.vstore

        print("📥 Ingesting new documents...")
        docs = DataConverter("data/flipkart_product_review.csv").convert()
        self.vstore.add_documents(docs)
        print(f"✅ Ingested {len(docs)} documents into AstraDB.")

        return self.vstore


if __name__ == "__main__":
    ingestor = DataIngestor()
    ingestor.ingest(load_existing=False)  # Re-ingest documents
