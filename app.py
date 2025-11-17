from flask import Flask, request, jsonify, render_template, Response
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_astradb import AstraDBVectorStore
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from time import time

from flipkart.rag_chain import RAGChain
from flipkart.config import Config


REQUEST_COUNT = Counter(
    "flipkart_app_request_count",
    "Total number of requests received"
)

REQUEST_LATENCY = Histogram(
    "flipkart_app_request_latency_seconds",
    "Latency of requests in seconds"
)


def create_app():
    app = Flask(__name__)

    print("Loading embeddings…")
    embeddings = HuggingFaceEmbeddings(model_name=Config.EMBEDDING_MODEL)

    print("Connecting to AstraDB Vector Store…")
    vector_store = AstraDBVectorStore(
        collection_name="flipkart_products",
        embedding=embeddings,
        api_endpoint=Config.ASTRA_DB_API_ENDPOINT,
        token=Config.ASTRA_DB_APPLICATION_TOKEN,
        namespace=Config.ASTRA_DB_KEYSPACE,
    )

    rag_chain = RAGChain(vector_store)

    @app.route("/")
    def home():
        return render_template("index.html")


    @app.route("/get", methods=["POST"])
    def get_bot_response():
        start_time = time()  # start timer
        REQUEST_COUNT.inc()  # increment counter

        user_query = request.form.get("msg", "")

        if not user_query:
            return jsonify({"text": "Please type something!"})

        try:
            answer = rag_chain.generate_answer(user_query)
            return jsonify({"text": str(answer)})
        except Exception as e:
            return jsonify({"text": f"Error: {str(e)}"})
        finally:
            REQUEST_LATENCY.observe(time() - start_time)  # record latency

    @app.route("/metrics")
    def metrics():
        return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
