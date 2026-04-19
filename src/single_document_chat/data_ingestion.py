import uuid
from Pathlib import Path
import sys
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from utils.model_loader import ModelLoader

Class SingleDocIngestor:
    def_init__(self):
        try:
            self.log = CustomLogger().get_logger(__name__)
        except Exception as e:
            self.log.error("Error in comparing documents", error=str(e))
            raise DocumentPortalException("An error occurred while comparing documents:", sys)
    
    def ingest_files(self, file_path: str):
        try:
            pass
        except Exception as e:
            self.log.error("Error in comparing documents", error=str(e))
            raise DocumentPortalException("An error occurred while comparing documents:", sys)
    
    def _create_retriever(self):
        try:
            pass
        except Exception as e:
            self.log.error("Error in comparing documents", error=str(e))
            raise DocumentPortalException("An error occurred while comparing documents:", sys)