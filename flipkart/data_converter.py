import pandas as pd
from langchain_core.documents import Document


class DataConverter:
    def __init__(self, csv_path):
        self.csv_path = csv_path

    def convert(self):
        df = pd.read_csv(self.csv_path)

        docs = []
        for _, row in df.iterrows():
            txt = f"""
Product: {row.get('product_name', '')}
Category: {row.get('category', '')}
Review: {row.get('review', '')}
Rating: {row.get('rating', '')}
            """

            docs.append(Document(page_content=txt))

        return docs
