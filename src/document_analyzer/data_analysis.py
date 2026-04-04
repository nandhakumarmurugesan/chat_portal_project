import os
import sys
from utils.model_loader import ModelLoader
from logger.custom_logger import CustomLogger   
from exception.custom_exception import DocumentPortalException
from model.models import *
from langchain_core.output_parsers import JsonOutputParser
#from langchain-core.output_parsers import OutputFixingParser
from langchain_classic.output_parsers import OutputFixingParser
from prompt.prompt_library import *

class DocumentAnalyzer:
    """Analyzes document using pre=trained models and extracts relevant information
       Automatically logs all actions and supports session based organization
    """
    def __init__(self):
        self.log=CustomLogger().get_logger(__name__)
        try:
            self.loader = ModelLoader()
            self.llm = self.loader.load_llm()
            
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
        
    def analyze_document(self, document_text: str) -> dict:
        "Analyze the document text and extract metadat information and summary"
        try:
            chain = self.prompt | self.llm | self.fixing_parser
            self.log.info("Metadata extraction chain created successfully")
            
            response = chain.invoke({
                "format_instructions": self.parser.get_format_instructions(),
                "document_text": document_text
            })
            
            self.log.info("Metadata extraction completed successfully", keys=list(response.keys()))
            return response
        
        except Exception as e:
            self.log.error(f"Error analyzing document: {e}")
            raise DocumentPortalException("Failed to analyze document:", e) from e