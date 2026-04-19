import uuid
from pathlib import Path
import sys
from datetime import datetime, timezone
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from utils.model_loader import ModelLoader

class DocumentIngestor:
    SUPPORTED_EXTENSIONS = {'.pdf', '.txt', '.docx', '.md'}
    def __init__(self, temp_dir:str = "data/multi_document_chat", faiss_dir: str = "faiss_index", session_id:str | None = None):
        try:
            self.log = CustomLogger().get_logger(__name__)
            
            #base dirs
            self.temp_dir = Path(temp_dir)
            self.faiss_dir = Path(faiss_dir)
            self.temp_dir.mkdir(parents=True, exist_ok=True)    
            self.faiss_dir.mkdir(parents=True, exist_ok=True)
            
            #sessioned paths
            self.session_id = session_id or f"session_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}"
            self.session_temp_dir = self.temp_dir / self.session_id
            self.session_faiss_dir = self.faiss_dir / self.session_id
            self.session_temp_dir.mkdir(parents=True, exist_ok=True)
            self.session_faiss_dir.mkdir(parents=True, exist_ok=True)
            
            self.model_loader = ModelLoader()
            self.log.info(
                "DocumentIngestion initialized", 
                temp_base=str(self.temp_dir), 
                faiss_base=str(self.faiss_dir),
                session_id=self.session_id,
                temp_path=str(self.session_temp_dir),
                faiss_path=str(self.session_faiss_dir)                          
                )

        except Exception as e:
            self.log.error(f"Failed to initialize DocumentIngestion", error=str(e))
            raise DocumentPortalException("Failed to initialize DocumentIngestion", sys)

    def ingest_files(self, file_path: str):
        try:
            documents=[]
            
            for uploaded_file in uploaded_files:
                ext = Path(uploaded_file.filename).suffix.lower()
                if ext not in self.SUPPORTED_EXTENSIONS:
                    self.log.warning(f"Unsupported file type skipped:", filename=uploaded_file.filename)
                    continue
                unique_filename = f"{uuid.uuid4().hex[:8]}{ext}"
                temp_path=self.session_temp_dir / unique_filename
                
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.read())
                self.log.info("File saved for ingestion", filename=uploaded_file.filename, saved_as=str(temp_path), session_id=self.session_id)
                
                if ext == '.pdf':
                    loader = PyPDFLoader(str(temp_path))
                elif ext == '.txt' or ext == '.md':
                    loader = TextLoader(str(temp_path))
                elif ext == '.docx':
                    loader = Docx2txtLoader(str(temp_path))
                else:
                    self.log.warning(f"No loader available for file type, skipping file:", filename=uploaded_file.filename)
                    continue
                
                docs = loader.load()
                documents.extend(docs)
                
            if not documents:
                self.log.warning("No valid documents loaded", sys)
                
            self.log.info("File loaded into documents", total_docs=len(documents), session_id=self.session_id)
            return self._create_retriever(documents)
        
        except Exception as e:
            self.log.error(f"Failed to ingest files", error=str(e))
            raise DocumentPortalException("Failed to ingest files", sys)

    def _create_retriever(self, documents):
        try:
            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=300)
            chunks = splitter.split_documents(documents)
            self.log.info("Documents split into chunks", total_chunks=len(chunks), session_id=self.session_id)
            
            embeddings = self.model_loader.load_embeddings()
            vector_store = FAISS.from_documents(documents=chunks, embedding=embeddings)
            
            #Save FAISS index
            vector_store.save_local(str(self.session_faiss_dir))
            self.log.info("FAISS index created and saved", path=str(self.session_faiss_dir), session_id=self.session_id)
            
            retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 5})
            self.log.info("Retriever created from FAISS index", session_id=self.session_id)
            return retriever
            
        except Exception as e:
            self.log.error(f"Failed to create retriever", error=str(e))
            raise DocumentPortalException("Failed to create retriever", sys)

        