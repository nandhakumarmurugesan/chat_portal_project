import os
import sys
from utils.model_loader import ModelLoader
from logger.custom_logger import CustomLogger   
from exception.custom_exception import DocumentPortalException
from model.models import *
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.output_parsers import OutputFixingParser
from prompt.prompt_library import *

Class DocumentAnalyzer:
    """Analyzes document using pre=trained models and extracts relevant information
       Automatically logs all actions and supports session based organization
    """
    def __init__(self):
        self.log=CustomLogger().get_logger(__name__)
        try:
            # Prepare parser
            self.parser = JsonOutputParser(pydantic_object=Metadata)
            self.fixing_parser = OutputFixingParser.from_llm(
                llm=self.llm,
                parser=self.parser
            )
            self.prompt = prompt
            self.log.info("DocumentAnalyzer initialized successfully")
            
        except Exception as e:
            self.log.error(f"Error initializing DocumentAnalyzer: {e}")
            raise DocumentPortalException("Failed to initialize DocumentAnalyzer:", sys)
        
    def analyze_metadata(self):
        pass