import os
import fitz
import uuid
from datetime import datetime
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException

class DocumentHandler:
    """Handles pdf savign and reading operations
       Automatically logs all actions and supports session based organization
    """
    def __init__(self, data_dir=None, session_id=None):
        try:
            self.log=CustomLogger().get_logger(__name__)
            self.data_dir = data_dir or os.getenv(
                                    "DATA_STORAGE_PATH",
                                    os.path.join(os.getcwd(), 'data',"document_analysis")
                                )
            self.session_id = session_id or f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
            
            #Create base session directory if it doesn't exist
            self.session_path = os.path.join(self.data_dir, self.session_id)
            os.makedirs(self.session_path, exist_ok=True)
            
        except Exception as e:
            self.log.error(f"Error initializing DocumentHandler: {e}")
            raise DocumentPortalException("Failed to initialize DocumentHandler:", e) from e
        
        self.log.info(
                    f"PDFHandler initialized with session_id: {self.session_id}," 
                    f"session_path: {self.session_path}," 
                    )
            
    def save_pdf(self, uploaded_file):
        """Saves the uploaded PDF file to the specified directory with a unique name.
           Logs the action and handles exceptions gracefully.
        """
        try:
            filename = os.path.basename(uploaded_file.name)
            
            if not filename.lower().endswith(".pdf"):
                raise DocumentPortalException("Invalid file type. Only PDF files are allowed.")
            
            save_path = os.path.join(self.session_path, filename)
            with open(save_path, 'wb') as f:
                f.write(uploaded_file.getbuffer())
            self.log.info(f"PDF file saved successfully at: {save_path}", file=filename, save_path=save_path, session_id=self.session_id)
            
            return save_path
                        
        except Exception as e:
            self.log.error(f"Error initializing DocumentHandler: {e}")
            raise DocumentPortalException("Failed to initialize DocumentHandler:", e) from e
        
    def read_pdf(self, pdf_path: str)-> str:
        """Reads the content of a PDF file and returns it as text.
           Logs the action and handles exceptions gracefully.
        """
        try:
            text_chunks = []
            with fitz.open(pdf_path) as doc:
                for page_num, page in enumerate(doc, start=1):
                    text_chunks.append(f"\n---- {page_num} ---\n {page.get_text()}")
            return "\n".join(text_chunks)
        
            self.log.info("PDF file read successfully: {pdf_path}", file=pdf_path, session_id=self.session_id,pages=len(text_chunks)   ) 
            return text
        
        except Exception as e:
            self.log.error(f"Error initializing DocumentHandler: {e}")
            raise DocumentPortalException("Failed to initialize DocumentHandler:", e) from e
        
if __name__ == "__main__":
    from pathlib import Path
    from io import BytesIO
    handler = DocumentHandler()
    
    pdf_path = "C:\\Users\\91984\\chat_portal_project\\data\\document_analysis\\zero Maintanance.pdf"
    
    class DummyFile:
        def __init__(self, file_path):
            self.name = Path(file_path).name #os.path.basename(file_path)
            self._file_path = file_path
        def getbuffer(self):
            return open(self._file_path, 'rb').read()
    
    dummy_file = DummyFile(pdf_path)
    handler = DocumentHandler()
    
    try:
        saved_path = handler.save_pdf(dummy_file)
        print(f"PDF saved at: {saved_path}")
        
        content = handler.read_pdf(saved_path)        
        print(f"PDF content:")
        print(content[:500])  # Print first 500 characters of the PDF content
        
    except Exception as e:
        print(f"Error: {e}")