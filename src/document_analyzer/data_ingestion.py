import os
import fitz
import uuid
from datetime import datetime
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException

Class DocumentHandler:
    """Handles pdf savign and reading operations
       Automatically logs all actions and supports session based organization
    """
    def __init__(self):
        """
        Args:
            base_dir (str, optional): _description_. Defaults to 'documents'.
        """
        pass
    
    def save_pdf(self):
        """Saves the uploaded PDF file to the specified directory with a unique name.
           Logs the action and handles exceptions gracefully.
        """
        pass
    
    def read_pdf(self):
        """Reads the content of a PDF file and returns it as text.
           Logs the action and handles exceptions gracefully.
        """
        pass