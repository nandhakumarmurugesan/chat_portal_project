import logging
import os
from datetime import datetime

class CustomLogger:
    def __init__(self,log_dir="logs"):
        #check for log directory exists or not if not create one        
        log_dir=os.path.join(os.getcwd(), "logs")
        os.makedirs(log_dir, exist_ok=True)
        #create log file name with timestamp
        LOG_File=f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
        LOG_File_Path=os.path.join(log_dir, LOG_File)
        #configure logging
        logging.basicConfig(
            filename=LOG_File_Path,
            format='%(asctime)s - %(levelname)s - %(message)s',
            level=logging.INFO
            )
        
    def get_logger(self,name=__file__):
        return logging.getLogger(os.path.basename(name))
    
if __name__=="__main__":
    logger=CustomLogger()
    logger=logger.get_logger(__file__)
    logger.info("Custom Logger Initialized. This is an info message.")