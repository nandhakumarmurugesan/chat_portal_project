import logging
import os
from datetime import datetime
import structlog


class CustomLogger:
    def __init__(self,log_dir="logs"):
        #check for log directory exists or not if not create one        
        self.log_dir=os.path.join(os.getcwd(), "logs")
        os.makedirs(log_dir, exist_ok=True)
        
        #create log file name with timestamp
        LOG_File=f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
        self.LOG_File_Path=os.path.join(log_dir, LOG_File)
        
        #configure logging
        # logging.basicConfig(
        #     filename=LOG_File_Path,
        #     format='%(asctime)s - %(levelname)s - %(message)s',
        #     level=logging.INFO
        #     )

    def get_logger(self,name=__file__):
        logger_name=os.path.basename(name)
    
        #configure logging for console and file in json format
        
        file_handler=logging.FileHandler(self.LOG_File_Path)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter("%(message)s"))
        
        console_handler=logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter("%(message)s"))
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(message)s',
            handlers=[file_handler, console_handler]
            
        )

        #configure structlog for JSON structure logging
        structlog.configure(
            processors=[
                structlog.processors.TimeStamper(fmt="iso",utc=True,key="timestamp"),
                structlog.processors.add_log_level,
                structlog.processors.EventRenamer(to="event"),
                structlog.processors.JSONRenderer()
            ],
            logger_factory=structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use=True,
        )
        
        return structlog.get_logger(logger_name)

if __name__=="__main__":
    logger=CustomLogger()
    logger=logger.get_logger(__file__)
    logger.info("user uploaded a pdf", user_id=123, file_name="document.pdf")
    logger.error("Failed to process the document", user_id=123, error="File format not supported")
    