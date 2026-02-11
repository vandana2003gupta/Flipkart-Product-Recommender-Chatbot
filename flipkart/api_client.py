import os
import requests
from dotenv import load_dotenv

load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST", "flipkart-apis.p.rapidapi.com")

HEADERS = {
    "x-rapidapi-key": RAPIDAPI_KEY,
    "x-rapidapi-host": RAPIDAPI_HOST
}


def search_products(query: str, page: int = 1, limit: int = 5):
    """
    Real-time Flipkart PRODUCT SEARCH from RapidAPI
    → Returns a clean list of: {title, price, image, url}
    """

    url = f"https://{RAPIDAPI_HOST}/backend/rapidapi/search"

    params = {
        "query": query,
        "page": page
    }

    resp = requests.get(url, headers=HEADERS, params=params, timeout=15)

    if resp.status_code != 200:
        raise RuntimeError(f"Flipkart API error: {resp.text}")

    data = resp.json()

    # Adjust based on Flipkart RapidAPI format
    items = data.get("products") or data.get("data") or []

    results = []

    for item in items[:limit]:

        title = item.get("title") or item.get("productTitle") or "Unknown Product"
        price = (
            item.get("price")
            or item.get("product_price")
            or item.get("finalPrice")
            or "N/A"
        )

        image = (
            item.get("image")
            or item.get("product_image")
            or item.get("image_url")
        )

        url = item.get("url") or item.get("product_url")
        if url and url.startswith("/"):
            url = "https://www.flipkart.com" + url

        results.append({
            "title": title,
            "price": price,
            "image": image,
            "url": url
        })

    return results
