import sys
import os
from dotenv import load_dotenv
#from langchain_core.chat_history import BaseChatPromptTemplate
from langchain_core.prompts import BaseChatPromptTemplate
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.vectorstores import FAISS
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_classic.chains import create_history_aware_retriever, create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from utils.model_loader import ModelLoader
from exception.custom_exception import DocumentPortalException
from logger.custom_logger import CustomLogger
from prompt.prompt_library import PROMPT_REGISTRY
from model.models import PromptType

class ConversationalRAG:
    
    def __init__(self, session_id: str, retriever) -> None:
        try:
            self.log = CustomLogger().get_logger(__name__)
            self.session_id = session_id
            self.retriever = retriever
            self.llm = self._load_llm()
            self.contextualize_prompt = PROMPT_REGISTRY[PromptType.CONTEXTUALIZE_QUESTION.value]
            self.qa_prompt = PROMPT_REGISTRY[PromptType.CONTEXT_QA.value]
            self.history_aware_retriever = create_history_aware_retriever(
                self.llm, self.retriever, self.contextualize_prompt #, self.qa_prompt
            )
            self.log.info("Conversational history_aware_retriever initialized", session_id=self.session_id)
            self.qa_chain = create_stuff_documents_chain( self.llm, self.qa_prompt)
            self.rag_chain = create_retriever_chain( self.history_aware_retriever, self.qa_chain)  
            self.log.info("Conversational RAG chain created", session_id=self.session_id)
                        
            self.chain = RunnableWithMessageHistory(
                self.rag_chain,
                self._get_session_history,
                input_messages_key="input",
                history_messages_key="history",
                output_messages_key="answer"
            )
            
            self.log.info("RunnableWithMessageHistory chain created", session_id=self.session_id)        
        
        except Exception as e:
            self.log.error("Failed to initialize conversational RAG", error=str(e), session = self.session_id)
            raise DocumentPortalException("Failed to initialize conversational RAG", sys)
    
    def _load_llm(self):
        try:
            llm = ModelLoader().load_llm()
            self.log.info("LLM loaded successfully", class_name=llm.__class__.__name__)
            return llm
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
            embeddings = ModelLoader().load_embeddings()
            if not os.path.isdir(index_path):
                raise FileNotFoundError(f"FAISS index directory not found at {index_path}")
            vectorestore = FAISS.load_local(index_path, embeddings)
            self.log.info("Loaded retriever from FAISS index", index_path=index_path)
            return vectorestore.as_retriever(search_type="similarity", search_kwargs={"k": 5})
        
        except Exception as e:
            self.log.error("Failed to load FAISS retriever", error=str(e), session = self.session_id)
            raise DocumentPortalException("Failed to load FAISS retriever", sys)
    
    def invoke(self, user_input: str)-> str:
        try:
            response = self.chain.invoke(
                {"input":user_input}, 
                config={"configurable": {"session_id": self.session_id} }
            )
            answer = response.get("answer", "No answer")
            if not answer:
                self.log.warning("No answer generated (Empty answer) by the RAG chain", session=self.session_id)
        
        except Exception as e:
            self.log.error("Failed to invoke the ConversationalRAG", error=str(e), session = self.session_id)
            raise DocumentPortalException("Failed to invoke the ConversationalRAG",sys)