from flask import Flask, request, jsonify, render_template
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_astradb import AstraDBVectorStore
from flipkart.rag_chain import RAGChain
from flipkart.config import Config


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

    # FIXED ENDPOINT (frontend AJAX calls POST /get)
    @app.route("/get", methods=["POST"])
    def get_bot_response():
        user_query = request.form.get("msg", "")

        if not user_query:
            return jsonify({"text": "Please type something!"})

        try:
            answer = rag_chain.generate_answer(user_query)
            return jsonify({"text": str(answer)})
        except Exception as e:
            return jsonify({"text": f"Error: {str(e)}"})

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
