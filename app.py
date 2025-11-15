from flask import Flask, render_template, request, Response
from prometheus_client import Counter, generate_latest
from dotenv import load_dotenv
import re

from flipkart.data_ingestion import DataIngestor
from flipkart.rag_chain import RAGChainBuilder, extract_answer

load_dotenv()

REQUEST_COUNT = Counter("http_requests_total", "Total HTTP Requests")


def create_app():

    app = Flask(__name__)

    print("📌 Loading vector store...")
    vector_store = DataIngestor().ingest(load_existing=True)

    rag_chain = RAGChainBuilder(vector_store).build_chain()

    @app.route("/")
    def index():
        REQUEST_COUNT.inc()
        return render_template("index.html")

    @app.route("/get", methods=["POST"])
    def get_response():

        user_input = request.form.get("msg", "")

        try:
            result = rag_chain.invoke(
                {"input": user_input},
                config={"configurable": {"session_id": "user-session"}}
            )

            answer = extract_answer(result)

            # Convert newlines safely for HTML
            answer = re.sub(r"\n+", "<br>", answer)

            return answer

        except Exception as e:
            print("❌ Error:", e)
            return f"Error: {str(e)}"

    @app.route("/metrics")
    def metrics():
        return Response(generate_latest(), mimetype="text/plain")

    return app


if __name__ == "__main__":
    app = create_app()
    print("🚀 Running on http://127.0.0.1:5000/")
    app.run(host="0.0.0.0", port=5000, debug=True)
