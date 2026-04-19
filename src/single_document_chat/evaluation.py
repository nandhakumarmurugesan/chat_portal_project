import sys
import os
from dotenv import load_dotenv
from langchain_core.chat_history import BaseChatPromptTemplate
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.vectorstores import FAISS
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.chains import create_history_aware_retriever, create_retriever_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from utils.model_loader import ModelLoader
from exception.custom_exception import DocumentPortalException
from logger.custom_logger import CustomLogger
from prompt.prompt_library import PROMPT_REGISTRY
from model.models import PromptType

Class ConversationalRAG:
    
    def __init__(self, session_id: str, retriever) -> None:
        try:
            self.log = CustomLogger().get_logger(__name__)
        except Exception as e:
            self.log.error("Failed to initialize conversational RAG", error=str(e), session = self.session_id)
            raise DocumentPortalException("Failed to initialize conversational RAG", sys)
    
    def _load_llm(self):
        try:
            pass
        except Exception as e:
            self.log.error("Failed to load LLM", error=str(e), session = self.session_id)
            raise DocumentPortalException("Failed to load LLM", sys)
    
    def _get_session_history(self, session_id: str):
        try:
            pass
        except Exception as e:
            self.log.error("Failed to get session history", error=str(e), session = self.session_id)
            raise DocumentPortalException("Failed to get session history", sys)
    
    def load_retriever_faiss(self):
        try:
            self.log = CustomLogger().get_logger(__name__)
        except Exception as e:
            self.log.error("Failed to load FAISS retriever", error=str(e), session = self.session_id)
            raise DocumentPortalException("Failed to load FAISS retriever", sys)
    
    def invoke(self):
        try:
            self.log = CustomLogger().get_logger(__name__)
        except Exception as e:
            self.log.error("Failed to invoke the ConversationalRAG", error=str(e), session = self.session_id)
            raise DocumentPortalException("Failed to invoke the ConversationalRAG",sys)