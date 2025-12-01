import logging
import json
import os
from datetime import datetime

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "func": record.funcName,
        }
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record)

def setup_logging(log_file: str = "imartty.log", level=logging.INFO):
    """Configure structured logging."""
    logger = logging.getLogger("imartty")
    logger.setLevel(level)
    
    # File handler with JSON formatting
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(JsonFormatter())
    logger.addHandler(file_handler)
    
    # Console handler (optional, maybe just for errors or debug)
    # console_handler = logging.StreamHandler()
    # console_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
    # logger.addHandler(console_handler)
    
    return logger

def get_logger(name: str):
    return logging.getLogger(f"imartty.{name}")
