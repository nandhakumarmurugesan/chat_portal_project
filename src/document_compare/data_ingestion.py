import sys
import pathlib import Path
import fitz
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException

class DocumentIngestion:
    def __init__(self, base_dir):
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