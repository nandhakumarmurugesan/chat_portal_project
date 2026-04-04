from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union

class Metadata(BaseModel):
    """Pydantic model to represent the metadata extracted from documents.
       This model can be extended with additional fields as needed.
    """
    Summary: List[str] = Field(default_factory=list, description="List of summary points extracted from the document")
    Title: str
    Author: str
    DateCreated: str
    LastModified: str
    Publisher: str
    Language: str
    PageCount: Union[int, str]  # Some PDFs might have non-integer page counts, hence Union
    SentimentTone: str

class 2:
    pass

class 3:
    pass
    
    