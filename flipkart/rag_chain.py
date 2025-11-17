from langchain_groq import ChatGroq
from flipkart.config import Config


class RAGChain:
    def __init__(self, vector_store):
        self.vector_store = vector_store

        # LLM (Groq - llama-3.1-8b-instant)
        self.llm = ChatGroq(
            api_key=Config.GROQ_API_KEY,
            model=Config.RAG_MODEL,
            temperature=0.2,
        )

        # Strong bullet-point enforced prompt
        self.prompt_template = """
You are a Flipkart Product Recommendation Assistant.

STRICT RULES:
- ALWAYS answer in bullet points (• or -).
- ALWAYS provide 3–6 product recommendations.
- ALWAYS include:
    • Product Name  
    • 1-line description  
    • Flipkart search link in this format:
      https://www.flipkart.com/search?q=<product name>
- If context exists → use it.
- If context is missing → answer using your own knowledge.
- No long paragraphs. No introductions. No conclusions.

Context:
{context}

User Query:
{question}

Now give the final answer ONLY in bullet points.
"""

    def generate_answer(self, question):
        docs = self.vector_store.similarity_search(question, k=4)
        context = "\n\n".join([d.page_content for d in docs]) if docs else ""

        prompt = self.prompt_template.format(context=context, question=question)

        response = self.llm.invoke(prompt)

        return response.content if hasattr(response, "content") else str(response)
