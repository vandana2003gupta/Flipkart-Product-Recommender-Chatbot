<<<<<<< HEAD
import pandas as pd
from langchain_core.documents import Document

class DataConverter:
    def __init__(self,file_path:str):
        self.file_path = file_path

    def convert(self):
        df = pd.read_csv(self.file_path)[["product_title","review"]]   

        docs = [
            Document(page_content=row['review'] , metadata = {"product_name" : row["product_title"]})
            for _, row in df.iterrows()
        ]

        return docs
=======
class DataConverter:
    """
    Simple utility class for cleaning and converting Flipkart API data.
    You can extend this based on your needs.
    """

    @staticmethod
    def convert(product: dict) -> dict:
        return {
            "title": product.get("title", "No title"),
            "price": product.get("price", "N/A"),
            "url": product.get("url", "#"),
            "image": product.get("image", ""),
            "description": product.get("description", ""),
        }
>>>>>>> fb74ba9e5ea1a37f37db3961a1b8c7e4d5e2f671
