import sys
from dotenv import load_dotenv
import pandas as pd
from langchain_core.output_parsers import JsonOutputParser
from langchain_classic.output_parsers import OutputFixingParser
from utils.model_loader import ModelLoader
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from prompt.prompt_library import PROMPT_REGISTRY
from model.models import * #SummaryResponse, PromptType

class DocumentComparatorLLM:
    def __init__(self):
        load_dotenv() 
        self.log=CustomLogger().get_logger(__name__)
        self.loader = ModelLoader()
        self.llm = self.loader.load_llm()
        #summary response already defined in the models.py file 
        self.parser = JsonOutputParser(pydantic_object=SummaryResponse)
        self.prompt = PROMPT_REGISTRY[PromptType.DOCUMENT_COMPARISON.value]
        #self.fixing_parser = OutputFixingParser.from_llm( parser=self.parser, llm=self.llm )
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
            self.log.info("Invoking document comparison LLM Chain")
            response = self.chain.invoke(inputs)
            self.log.info("Chain comparison completed successfully", response_preview=str(response)[:200])
            return self._format_response(response)
        
        except Exception as e:
            self.log.error("Error in comparing documents", error=str(e))
            raise DocumentPortalException("An error occurred while comparing documents:", sys)
    
    def _format_response(self, response_parsed: list[dict]) -> pd.DataFrame:
        """Format the response from the LLM into a structured format for easier consumption
        """
        try:
            df = pd.DataFrame(response_parsed)
            #self.log.info("Response formatted successfully into DataFrame")
            return df
        except Exception as e:
            self.log.error("Error in formatting response", error=str(e))
            raise DocumentPortalException("An error occurred while formatting response:", sys)
    