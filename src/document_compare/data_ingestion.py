import sys
import pathlib import Path
import fitz
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException

class DocumentIngestion:
    def __init__(self):
        self.log=CustomLogger().get_logger(__name__)
        self.base_dir = Path(self.base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.log.info(f"DocumentIngestion initialized successfully with base directory: {self.base_dir}")
                
    def delete_existing_files(self):
        """Delete existing file in the specified path
        """
        try:
            pass
        except Exception as e:
            self.log.error(f"Error deleting existing files: {e}")
            raise DocumentPortalException("An error occurred while deleting existing files:", sys)

    def save_uploaded_files(self):
        """Save uploaded files to the specified path
        """
        try:
            pass
        except Exception as e:
            self.log.error(f"Error saving uploaded files: {e}")
            raise DocumentPortalException("An error occurred while saving uploaded files:", sys)

    def read_pdf(self, file_path: str) -> str:
        """Read the content of a PDF file and return it as a string
        """
        try:
            with fitz.open(self,pdf_path:str) as doc:
                if doc.is_encrypted:
                    raise ValueError("PDF file is encrypted and cannot be read.")
        except Exception as e:
            self.log.error(f"Error reading PDF file: {file_path}, error: {e}")
            raise DocumentPortalException(f"An error occurred while reading PDF file: {file_path}", sys)