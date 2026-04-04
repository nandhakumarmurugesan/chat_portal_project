from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template("""
    You are a highly capable and qualified assistant trained to analyze and summarize and extract 
    information from documents.
    Return only valid JSON matching the exact schema below.
    
    {format_instructions}
    
    Analyze the following document
    
    {document_text}
    
                                           
    """
)                                      