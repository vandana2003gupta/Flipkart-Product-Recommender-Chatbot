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
