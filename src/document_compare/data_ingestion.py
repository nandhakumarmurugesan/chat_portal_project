import sys
import uuid
from pathlib import Path
import fitz
from datetime import datetime, timezone
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException

class DocumentIngestion:
    def __init__(self, base_dir:str="data\\document_compare", session_id=None):
        self.log=CustomLogger().get_logger(__name__)
        self.base_dir = Path(base_dir)
        self.session_id = session_id or f"session_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}"
        self.session_path = self.base_dir / self.session_id 
        self.base_dir.mkdir(parents=True, exist_ok=True)
        
        self.log.info(f"DocumentIngestion initialized successfully with base directory: {self.base_dir}")
                
    # def delete_existing_files(self):
    #     """Delete existing file in the specified path
    #     """
    #     try:
    #         if self.base_dir.exists() and self.base_dir.is_dir():
    #             for file in self.base_dir.iterdir():
    #                 if file.is_file():
    #                     file.unlink() #delete the file 
    #                     self.log.info(f"Deleted existing file: {file}")
    #             self.log.info("All existing files deleted successfully and directory cleaned up", directory=str(self.base_dir))
    #     except Exception as e:
    #         self.log.error(f"Error deleting existing files: {e}")
    #         raise DocumentPortalException("An error occurred while deleting existing files:", sys)

    def save_uploaded_files(self, reference_file, actual_file):
        """Save uploaded files to the specified path
        """
        try:
            ref_path=self.base_dir / reference_file.name
            act_path=self.base_dir / actual_file.name
            
            if not reference_file.name.lower().endswith('.pdf') or not actual_file.name.lower().endswith('.pdf'):
                raise ValueError("Both files must be PDFs")
            
            with open(ref_path, 'wb') as f:
                f.write(reference_file.getbuffer())
            
            with open(act_path, 'wb') as f:
                f.write(actual_file.getbuffer())
            
            self.log.info(f"Files saved successfully: reference={ref_path}, actual={act_path}")
            return ref_path, act_path
                        
        except Exception as e:
            self.log.error(f"Error saving uploaded files: {e}")
            raise DocumentPortalException("An error occurred while saving uploaded files:", sys)

    def read_pdf(self, pdf_path: Path) -> str:
        """Read the content of a PDF file and return it as a string
        """
        try:
            with fitz.open(pdf_path) as doc:
                if doc.is_encrypted:
                    raise ValueError("PDF file is encrypted and cannot be read: {pdf_path.name}")
                
                all_text = []
                for page_num in range(doc.page_count):
                    page = doc.load_page(page_num)
                    text = page.get_text()
                    if text.strip():  # Check if the page has any text content
                        all_text.append(f"\n--- Page {page_num + 1} ---\n{text}")
                    
                    self.log.info(f"PDFs read succesfully", file=str(pdf_path), pages=len(all_text))
                    return "\n".join(all_text)                
                
        except Exception as e:
            self.log.error(f"Error reading PDF file: {pdf_path}, error: {e}")
            raise DocumentPortalException(f"An error occurred while reading PDF file: {pdf_path}", sys)
        
    def combine_documents(self) -> str:
        """Combine the content of reference and actual documents into a single string for comparison
        """
        try:
            doc_parts = []
            
            for file in sorted(self.base_dir.iterdir()):
                if file.is_file() and file.suffix.lower() == '.pdf':
                    content = self.read_pdf(file)
                    doc_parts.append(f"Document: {file.name}\n{content}")
            
            combined_text = "\n\n".join(doc_parts)
            self.log.info("Documents combined successfully", count=len(doc_parts))
            return combined_text
        
        except Exception as e:
            self.log.error(f"Error combining documents: {e}")
            raise DocumentPortalException("An error occurred while combining documents:", sys)
        
    def clean_old_sessions(self, keep_latest: int = 3):
        """Clean up old session directories, keeping only the latest few sessions
        """
        try:
            session_folders = sorted(
                [f for f in self.base_dir.iterdir() if f.is_dir()],
                reverse=True )       
            for folder in session_folders[keep_latest:]:
                for file in folder.iterdir():
                    file.unlink()
                folder.rmdir()
                self.log.info(f"Deleted old session directory path:, {folder}")
                
            self.log.info(f"Old sessions cleaned up successfully, kept latest {keep_latest} sessions")
        
        except Exception as e:
            self.log.error(f"Error cleaning old sessions: {e}")
            raise DocumentPortalException("An error occurred while cleaning old sessions:", sys)