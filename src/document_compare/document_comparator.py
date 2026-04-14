import sys
import os
from dotenv import load_dotenv
import pandas as pd
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from model.models import *
from prompt.prompt_library import PROMPT_REGISTRY
from utils.model_loader import ModelLoader
from langchain_core.output_parsers import JsonOutputParser
from langchain_classic.output_parsers import OutputFixingParser

class DocumentComparatorLLM:
    def __init__(self):
        load_dotenv() 
        self.log=CustomLogger().get_logger(__name__)
        self.loader = ModelLoader()
        self.llm = self.loader.load_llm()
        #summary response already defined in the models.py file 
        self.parser = JsonOutputParser(pydantic_object=SummaryResponse)
        self.fixing_parser = OutputFixingParser.from_llm(
            llm=self.llm,
            parser=self.parser
        )   
        self.prompt = PROMPT_REGISTRY["document_comparison"]
        self.chain = self.prompt | self.llm | self.parser 
        self.log.info("DocumentComparatorLLM initialized successfully")
    
    def compare_documents(self, combined_docs:str) -> pd.DataFrame:
        """Compare the content of two documents and identify the differences
           The output should be in a structured format with page wise comparison and summary of changes
        """
        try:
            inputs = {
                "combined_docs" : combined_docs,
                "format_instructions" : self.parser.get_format_instructions()
            }
            self.log.info("Starting document comparison using LLM")
            response = self.chain.invoke(inputs)
            self.log.info("Document comparison completed successfully", response=response)
            return self._format_response(response)
        
        except Exception as e:
            self.log.error(f"Error in comparing documents: {e}")
            raise DocumentPortalException("An error occurred while comparing documents:", sys)    
    
    def _format_response(self, response_parsed: list[dict]) -> pd.DataFrame:
        """Format the response from the LLM into a structured format for easier consumption
        """
        try:
            df = pd.DataFrame(response_parsed)
            self.log.info("Response formatted successfully into DataFrame", dataframe=df)
            return df
        except Exception as e:
            self.log.error(f"Error in formatting response: {e}")
            raise DocumentPortalException("An error occurred while formatting response:", sys)
    