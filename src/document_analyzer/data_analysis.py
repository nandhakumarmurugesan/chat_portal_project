import os
from utils.model_loader import ModelLoader
from logger.custom_logger import CustomLogger   
from exception.custom_exception import DocumentPortalException
from model.models import *
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.output_parsers import OutputFixingParser

Class DocumentAnalyzer:
    """Analyzes document using pre=trained models and extracts relevant information
       Automatically logs all actions and supports session based organization
    """
    def __init__(self):
        pass
    def analyze_metadata(self):
        pass
    
    