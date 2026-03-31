import os
import sys
from dotenv import load_dotenv
from utils.config_loader import load_config
from langchain_google_genai import GoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_groq import ChatGroq
#from langchain_openai import ChatOpenAI
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException

log = CustomLogger().get_logger("__file__")

class ModelLoader:
    """Loading embedding models and LLM (Utility class)
    """
    def __init__(self):
        load_dotenv()
        self._validate_env()
        self.config=load_config()
        log.info("Configuration loaded successfully", config_keys=list(self.config.keys()))
        
    def _validate_env(self):
        """Validate necessary environment variables are set and check API keys are present
        """
        required_vars=["GOOGLE_API_KEY", "GROQ_API_KEY"]
        self.api_keys={key: os.getenv(key) for key in required_vars}
        missing = [key for key, value in self.api_keys.items() if not value]
        
        if missing:
            log.error("Missing API keys:", missing_vars=missing)
            raise DocumentPortalException("Missing environment variables:", sys)
        log.info("All required environment variables are set", 
            available_keys=[k for k in self.api_keys if self.api_keys[k]])
        
    def load_embeddings(self):
        """Load and return embedding model 
        """
        try:
            log.info("Starting to load embedding model ...")
            model_name = self.config["embedding_model"]["model_name"]
            return GoogleGenerativeAIEmbeddings(model=model_name)
        except Exception as e:
            log.error("Error loading embedding model", error=str(e))
            raise DocumentPortalException("Failed to load embedding model", sys) 

    def load_llm(self):
        """Load and return LLM 
        """
        log.info("Starting to load LLM model ...")
        llm_block = self.config["llm"]
        #choosing default groq as llm provider
        provider_key = os.getenv("LLM_PROVIDER", "groq")
        
        if provider_key not in llm_block:
            log.error("Unsupported LLM provider", provider_key=provider_key)
            raise ValueError(f"Unsupported LLM provider: {provider_key} not found in the config")
        
        llm_config = llm_block[provider_key]
        provider = llm_config.get("provider")
        model_name = llm_config.get("model_name")
        temperature = llm_config.get("temperature", 0.3)
        max_tokens = llm_config.get("max_output_tokens", 2048)
        
        log.info("LLM configuration loaded", provider=provider, model_name=model_name, temperature=temperature, max_tokens=max_tokens)
        
        if provider == "google":
            llm=GoogleGenerativeAI(
                model=model_name, 
                temperature=temperature, 
                max_output_tokens=max_tokens
                )
            return llm
        elif provider == "groq":
            llm=ChatGroq(
                model=model_name, 
                api_key=self.api_keys["GROQ_API_KEY"],
                temperature=temperature, 
                )
            return llm  
        # elif provider == "openai":
        #     llm=ChatOpenAI(
        #         model=model_name, 
        #         api_key=self.api_keys["OPENAI_API_KEY"],
        #         temperature=temperature, 
        #         max_tokens=max_tokens
        #         )
        #     return llm
        else:
            log.error("Unsupported LLM provider", provider=provider)
            raise ValueError(f"Unsupported LLM provider: {provider}")
        
if __name__ == "__main__":
    
    loader = ModelLoader()
    
    #Test embedding model loading
    embedding_model = loader.load_embeddings()
    print(f"Embedding model loaded: {embedding_model}")
    
    # embed the model
    result = embedding_model.embed_content("How are you?")
    print(f"Embedding result: {result}")
    
    #Test LLM loading based on yaml config
    llm_model = loader.load_llm()
    print(f"LLM model loaded: {llm_model}")
    
    # Test the ModelLoader
    result = llm_model.invoke("How are you?")
    print(f"LLM response: {result.content}")