# flipkart/api_client.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST", "real-time-flipkart-data2.p.rapidapi.com")

HEADERS = {
    "x-rapidapi-key": RAPIDAPI_KEY,
    "x-rapidapi-host": RAPIDAPI_HOST
}

def search_products(query: str, pincode: str = "400001", limit: int = 5):
    """
    Search Flipkart products in real-time using RapidAPI.
    Returns list of dicts: {title, price, image, url}
    """
    url = f"https://{RAPIDAPI_HOST}/search"
    params = {"q": query, "pincode": pincode}

    resp = requests.get(url, headers=HEADERS, params=params, timeout=10)
    if resp.status_code != 200:
        raise RuntimeError(f"Flipkart API error: {resp.text}")

    data = resp.json()

    # Response shape may vary → adjust keys based on RapidAPI’s JSON
    items = data.get("products") or data.get("results") or []
    results = []
    for it in items[:limit]:
        title = it.get("title") or it.get("productTitle")
        price = it.get("price") or it.get("product_price")
        image = it.get("image") or it.get("image_url")
        url = it.get("url") or it.get("product_url")

        # Fix relative URLs
        if url and url.startswith("/"):
            url = "https://www.flipkart.com" + url

        results.append({
            "title": title,
            "price": price,
            "image": image,
            "url": url
        })

    return results
