# app.py

from flask import Flask, render_template, request, Response
from prometheus_client import Counter, generate_latest
from flipkart.data_ingestion import DataIngestor
from flipkart.rag_chain import RAGChainBuilder
from flipkart.api_client import search_products
from flipkart.config import Config
from dotenv import load_dotenv
import logging

# Load .env
load_dotenv()

# Prometheus counter
REQUEST_COUNT = Counter("http_requests_total", "Total HTTP Requests")

# Logging config
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


def create_app():
    app = Flask(__name__)

    # Initialize vector store & RAG chain
    vector_store = DataIngestor().ingest(load_existing=True)
    rag_chain = RAGChainBuilder(vector_store).build_chain()

    @app.route("/")
    def index():
        REQUEST_COUNT.inc()
        return render_template("index.html")

    @app.route("/get", methods=["POST"])
    def get_response():
        try:
            user_input = request.form["msg"]
            logging.info(f"User input: {user_input}")

            # Get RAG answer
            rag_result = rag_chain.invoke(
                {"input": user_input},
                config={"configurable": {"session_id": "user-session"}}
            )
            response = rag_result.get("answer", "⚠️ Sorry, I couldn’t generate an answer.")

            logging.info(f"RAG response: {response}")

            # Get Flipkart products
            try:
                products = search_products(user_input, limit=3)
            except Exception as e:
                logging.error(f"Flipkart API failed: {e}")
                products = []

            # Build HTML product cards
            product_html = ""
            if products:
                product_html += "<br><b>🛒 Flipkart Products:</b><br>"
                for p in products:
                    product_html += f"""
                    <div class='product-card'>
                        <a href='{p.get("url")}' target='_blank'>
                            <img src='{p.get("image")}' alt='{p.get("title")}' width='120'>
                            <p><b>{p.get("title")}</b></p>
                            <p style='color:green;'>{p.get("price")}</p>
                        </a>
                    </div>
                    """

            return response + product_html

        except Exception as e:
            logging.error(f"Error in /get: {e}")
            return "⚠️ Sorry, something went wrong. Please try again."

    @app.route("/metrics")
    def metrics():
        return Response(generate_latest(), mimetype="text/plain")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
