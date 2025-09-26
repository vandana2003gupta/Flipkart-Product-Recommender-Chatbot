<<<<<<< HEAD
from langchain_groq import ChatGroq
from langchain.chains import create_history_aware_retriever,create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from flipkart.config import Config

class RAGChainBuilder:
    def __init__(self,vector_store):
        self.vector_store=vector_store
        self.model = ChatGroq(model=Config.RAG_MODEL , temperature=0.5)
        self.history_store={}

    def _get_history(self,session_id:str) -> BaseChatMessageHistory:
        if session_id not in self.history_store:
            self.history_store[session_id] = ChatMessageHistory()
        return self.history_store[session_id]
    
    def build_chain(self):
        retriever = self.vector_store.as_retriever(search_kwargs={"k":3})

        context_prompt = ChatPromptTemplate.from_messages([
            ("system", "Given the chat history and user question, rewrite it as a standalone question."),
            MessagesPlaceholder(variable_name="chat_history"), 
            ("human", "{input}")  
        ])

        qa_prompt = ChatPromptTemplate.from_messages([
            ("system", """You're an e-commerce bot answering product-related queries using reviews and titles.
                          Stick to context. Be concise and helpful.\n\nCONTEXT:\n{context}\n\nQUESTION: {input}"""),
            MessagesPlaceholder(variable_name="chat_history"), 
            ("human", "{input}")  
        ])

        history_aware_retriever = create_history_aware_retriever(
            self.model , retriever , context_prompt
        )

        question_answer_chain = create_stuff_documents_chain(
            self.model , qa_prompt
        )

        rag_chain = create_retrieval_chain(
            history_aware_retriever,question_answer_chain
        )

        return RunnableWithMessageHistory(
=======
# flipkart/rag_chain.py

from langchain.chains import (
    create_history_aware_retriever,
    create_retrieval_chain,
)
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_groq import ChatGroq

from flipkart.config import Config


class RAGChainBuilder:
    def __init__(self, vector_store):
        """
        Initializes the RAG chain builder with a given vector store retriever.
        """
        self.vector_store = vector_store
        self.model = ChatGroq(model=Config.RAG_MODEL, temperature=0.5)
        self.history_store = {}

    def _get_history(self, session_id: str) -> BaseChatMessageHistory:
        """
        Retrieve or create a message history for a given session.
        """
        if session_id not in self.history_store:
            self.history_store[session_id] = ChatMessageHistory()
        return self.history_store[session_id]

    def build_chain(self):
        """
        Build the Retrieval-Augmented Generation (RAG) chain with history awareness.
        """
        retriever = self.vector_store.as_retriever(search_kwargs={"k": 3})

        # Prompt to rewrite context-aware questions
        context_prompt = ChatPromptTemplate.from_messages([
            ("system", "Given the chat history and user question, rewrite it as a standalone question."),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}")
        ])

        # Prompt for final Q&A response
        qa_prompt = ChatPromptTemplate.from_messages([
            ("system",
             """You're an e-commerce assistant. Answer questions using Flipkart product reviews, titles,
             and context. Be concise, relevant, and helpful.
             \n\nCONTEXT:\n{context}\n\nQUESTION: {input}"""),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}")
        ])

        # History-aware retriever
        history_aware_retriever = create_history_aware_retriever(
            self.model, retriever, context_prompt
        )

        # Question-answering chain
        question_answer_chain = create_stuff_documents_chain(
            self.model, qa_prompt
        )

        # Build the retrieval + QA chain
        rag_chain = create_retrieval_chain(
            history_aware_retriever,
            question_answer_chain
        )

        # Wrap with history so it remembers chat sessions
        rag_with_history = RunnableWithMessageHistory(
>>>>>>> fb74ba9e5ea1a37f37db3961a1b8c7e4d5e2f671
            rag_chain,
            self._get_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer"
        )

<<<<<<< HEAD


=======
        return rag_with_history
>>>>>>> fb74ba9e5ea1a37f37db3961a1b8c7e4d5e2f671
