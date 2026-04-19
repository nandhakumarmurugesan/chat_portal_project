import uuid
from pathlib import Path
import sys
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from utils.model_loader import ModelLoader

class SingleDocIngestor:
    def __init__(self, data_dir: str = "data/single_document_chat",faiss_dir: str = "faiss_index"):
        try:
            self.log = CustomLogger().get_logger(__name__)
            
            self.data_dir = Path(data_dir)
            self.data_dir.mkdir(parents=True, exist_ok=True)    
            self.faiss_dir = Path(faiss_dir)
            self.faiss_dir.mkdir(parents=True, exist_ok=True)
            self.model_loader = ModelLoader()

            self.log.info("SingleDocIngestor initialized", temp_data_dir=str(self.data_dir), temp_faiss_dir=str(self.faiss_dir))
            
        except Exception as e:
            self.log.error("Error in comparing documents", error=str(e))
            raise DocumentPortalException("An error occurred while comparing documents:", sys)
    
    def ingest_files(self, file_path: str):
        try:
            documents=[]
            for uploaded_file in uploaded_files:
                unique_filename = f"session_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}.pdf"
                temp_path=self.data_dir / unique_filename
                with open(temp_path, "wb") as f_out:
                    f_out.write(uploaded_file.read())
                loader = PyPDFLoader(str(temp_path))
                docs = loader.load()
                documents.extend(docs) 
            self.log.info("PDF files loaded", count=len(documents))
            return _create_retriever(documents)
            
        except Exception as e:
            self.log.error("Error in comparing documents", error=str(e))
            raise DocumentPortalException("An error occurred while comparing documents:", sys)
    
    def _create_retriever(self):
        try:
            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            chunks = splitter.split_documents(documents)
            self.log.info("Documents split into chunks", count=len(chunks))
            
            embeddings = self.model_loader.load_embeddings()
            vector_store = FAISS.from_documents(documents=chunks, embedding=embeddings)
            
            #save FAISS index
            vectorstore.save_local(str(self.faiss_dir))
            self.log.info("FAISS index created and saved", faiss_path=str(self.faiss_dir))
            
            retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 5})
            self.log.info("Retriever created from FAISS index", retriever_type=str(type(retriever)))
            return retriever
            
        except Exception as e:
            self.log.error("Error in comparing documents", error=str(e))
            raise DocumentPortalException("An error occurred while comparing documents:", sys)