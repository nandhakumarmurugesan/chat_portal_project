from langchain_core.prompts import ChatPromptTemplate

document_analysis_prompt = ChatPromptTemplate.from_template("""
    You are a highly capable and qualified assistant trained to analyze and summarize and extract 
    information from documents.
    Return only valid JSON matching the exact schema below.
    {format_instructions}
    Analyze the following document  
    {document_text}                                   
    """
)

document_comparison_prompt= ChatPromptTemplate.from_template(
        """
        You are provided with two documents. Your task is to do the following
         1. compate the content in the two pdfs
         2. Identify the difference in PDF and note down the page numbers
         3. THe output you provide must be page wise comparison content
         4. If any page do not have any change, mention as "No Change"
         5. Summarize the difference and changes in the end of the output in the PDFs     
    """
    Input_documents: {combined_docs}
    Your response should follow the below format:
    {format_instructions}
    )

PROMPT_REGISTRY={"document_analysis": document_analysis_prompt,
                 "document_comparison": document_comparison_prompt
                 }                                     