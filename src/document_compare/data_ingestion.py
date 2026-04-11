import sys
import pathlib import Path
import fitz
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException

class DocumentComparator:
    def __init__(self):
        pass
    def delete_existing_files(self):
        """Delete existing file in the specified path
        """
        pass
    def save_uploaded_files(self):
        """Save uploaded files to the specified path
        """
        pass
    def read_pdf(self, file_path: str) -> str:
        """Read the content of a PDF file and return it as a string
        """
        pass