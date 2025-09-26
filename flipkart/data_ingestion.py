from langchain_astradb import AstraDBVectorStore
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from flipkart.data_converter import DataConverter
from flipkart.config import Config

class DataIngestor:
    def __init__(self):
        self.embedding = HuggingFaceEndpointEmbeddings(model=Config.EMBEDDING_MODEL)

        # Don't force recreate collection
        self.vstore = AstraDBVectorStore(
            embedding=self.embedding,
            collection_name="flipkart_database",
            api_endpoint=Config.ASTRA_DB_API_ENDPOINT,
            token=Config.ASTRA_DB_APPLICATION_TOKEN,
            namespace=Config.ASTRA_DB_KEYSPACE,
            pre_delete_collection=False   # ✅ ensures we don't try to drop/recreate
        )

    def ingest(self, load_existing=True):
        if load_existing:
            # ✅ Just return the existing vector store (no new collection created)
            return self.vstore

        # Otherwise, ingest data fresh
        docs = DataConverter("data/flipkart_product_review.csv").convert()

        # (Optional) reduce metadata to avoid exceeding Astra index limits
        for doc in docs:
            doc.metadata = {k: doc.metadata[k] for k in list(doc.metadata)[:3]}  # keep only first 3 keys

        self.vstore.add_documents(docs)
        return self.vstore
