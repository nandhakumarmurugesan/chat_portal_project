from pydantic import BaseModel, RootModel #,Field
from typing import List, Union #,Optional, Dict, Any
from enum import Enum

class Metadata(BaseModel):
    """Pydantic model to represent the metadata extracted from documents.
       This model can be extended with additional fields as needed.
    """
    Summary: List[str] # = Field(default_factory=list, description="List of summary points extracted from the document")
    Title: str
    Author: List[str]
    DateCreated: str
    LastModified: str
    Publisher: str
    Language: str
    PageCount: Union[int, str]  # Some PDFs might have non-integer page counts, hence Union
    SentimentTone: str

class ChangeFormat(BaseModel):
    """Pydantic model to represent the change format for documents.
       This model can be extended with additional fields as needed.
    """
    Page: str
    changes: str

class SummaryResponse(RootModel[list[ChangeFormat]]):
    pass
    
class PromptType(str, Enum):
    DOCUMENT_ANALYSIS = "document_analysis"
    DOCUMENT_COMPARISON = "document_comparison"
    CONTEXTUAL_QUESTION = "contextual_question"
    CONTEXT_QA = "context_qa"
    