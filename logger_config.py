import logging
import logging.handlers
import os
from datetime import datetime

def setup_logger():
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Create formatters
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
    )

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)

    # Create file handler
    log_file = f'logs/app_{datetime.now().strftime("%Y%m%d")}.log'
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)

    # Create error file handler
    error_log_file = f'logs/error_{datetime.now().strftime("%Y%m%d")}.log'
    error_file_handler = logging.handlers.RotatingFileHandler(
        error_log_file,
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(file_formatter)

    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    # Remove any existing handlers
    root_logger.handlers = []

    # Add handlers
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(error_file_handler)

    return root_logger

def get_logger(name):
    """Get a logger instance with the specified name"""
    return logging.getLogger(name)

# Custom log filter for sensitive data
class SensitiveDataFilter(logging.Filter):
    def __init__(self, patterns=None):
        super().__init__()
        self.patterns = patterns or {
            'phone': r'\+?\d{10,}',
            'email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            'ssn': r'\d{3}-\d{2}-\d{4}',
            'credit_card': r'\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}'
        }

    def filter(self, record):
        if isinstance(record.msg, str):
            for pattern_name, pattern in self.patterns.items():
                record.msg = record.msg.replace(pattern, f'[REDACTED_{pattern_name.upper()}]')
        return True

# Initialize logger when module is imported
logger = setup_logger()
