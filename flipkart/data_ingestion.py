from langchain_astradb import AstraDBVectorStore
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from flipkart.data_converter import DataConverter
from flipkart.config import Config

class DataIngestor:
    def __init__(self):
        self.embedding = HuggingFaceEndpointEmbeddings(
            model=Config.EMBEDDING_MODEL
        )

        # WORKING FOR YOUR VERSION
        self.vstore = AstraDBVectorStore(
            embedding=self.embedding,
            collection_name="flipkart_database",
            api_endpoint=Config.ASTRA_DB_API_ENDPOINT,
            token=Config.ASTRA_DB_APPLICATION_TOKEN,
            namespace=Config.ASTRA_DB_KEYSPACE,
            pre_delete_collection=False   # <-- KEY FIX
        )

    def ingest(self, load_existing=True):
        if load_existing:
            return self.vstore

        docs = DataConverter("data/flipkart_product_review.csv").convert()
        self.vstore.add_documents(docs)

        return self.vstore
