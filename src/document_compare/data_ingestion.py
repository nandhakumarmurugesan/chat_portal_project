import sys
from pathlib import Path
import fitz
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException

class DocumentIngestion:
    def __init__(self, base_dir:str="data\\document_compare"):
        self.log=CustomLogger().get_logger(__name__)
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.log.info(f"DocumentIngestion initialized successfully with base directory: {self.base_dir}")
                
    def delete_existing_files(self):
        """Delete existing file in the specified path
        """
        try:
            if self.base_dir.exists() and self.base_dir.is_dir():
                for file in self.base_dir.iterdir():
                    if file.is_file():
                        file.unlink() #delete the file 
                        self.log.info(f"Deleted existing file: {file}")
                self.log.info("All existing files deleted successfully and directory cleaned up", directory=str(self.base_dir))
        except Exception as e:
            self.log.error(f"Error deleting existing files: {e}")
            raise DocumentPortalException("An error occurred while deleting existing files:", sys)

    def save_uploaded_files(self, reference_file, actual_file):
        """Save uploaded files to the specified path
        """
        try:
            self.delete_existing_files()
            self.log.info("Existing files deleted successfully")
            
            ref_path=self.base_dir / reference_file.name
            act_path=self.base_dir / actual_file.name
            
            if not reference_file.name.endswith('.pdf'):
                raise ValueError("Reference file must be a PDF")
            
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
            content_dict ={}
            doc_parts =[]
            
            for filename in sorted(self.base_dir.iterdir()):
                if filename.is_file() and filename.suffix == '.pdf':
                    content_dict[filename.name] = self.read_pdf(filename)
            
            for filename, content in content_dict.items():
                doc_parts.append(f"Document: {filename}\nContent:\n{content}")
            
            combined_text = "\n\n".join(doc_parts)
            #f"Reference Document Content:\n{ref_content}\n\nActual Document Content:\n{act_content}"
            self.log.info("Documents combined successfully", count=len(doc_parts))
            return combined_text
        
        except Exception as e:
            self.log.error(f"Error combining documents: {e}")
            raise DocumentPortalException("An error occurred while combining documents:", sys)