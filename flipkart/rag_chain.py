# flipkart/rag_chain.py

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory

from flipkart.config import Config


# --------------------------------------------------------
# SAFE CLEAN ANSWER OUTPUT
# --------------------------------------------------------
def extract_answer(result):
    """
    Converts all LangChain outputs into a clean string.
    Prevents 'dict' object has no attribute 'replace'.
    """
    if hasattr(result, "content"):
        return str(result.content)

    if isinstance(result, dict):
        # LangChain wraps final output inside result["answer"]
        ans = result.get("answer")
        if hasattr(ans, "content"):
            return str(ans.content)
        return str(ans)

    return str(result)


# --------------------------------------------------------
# RAG Chain (Compatible with LangChain 1.3.1)
# --------------------------------------------------------
class RAGChainBuilder:
    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.model = ChatGroq(model=Config.RAG_MODEL, temperature=0.4)
        self.history_store = {}

    def _get_history(self, session_id: str) -> BaseChatMessageHistory:
        if session_id not in self.history_store:
            self.history_store[session_id] = ChatMessageHistory()
        return self.history_store[session_id]

    def build_chain(self):

        retriever = self.vector_store.as_retriever(search_kwargs={"k": 3})

        # Prompt Template
        qa_prompt = ChatPromptTemplate.from_messages([
            ("system",
             "You are a Flipkart product assistant. Be short and accurate.\n"
             "Use ONLY the provided context.\n\nCONTEXT:\n{context}"),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}")
        ])

        # Build LCEL pipeline
        rag_chain = (
            RunnableParallel({
                "context": retriever,        # doc retrieval
                "input": RunnablePassthrough()
            })
            | qa_prompt
            | self.model
        )

        return RunnableWithMessageHistory(
            rag_chain,
            self._get_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer"
        )
