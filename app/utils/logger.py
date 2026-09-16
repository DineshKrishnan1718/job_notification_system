import logging
import sys
import os

def setup_logger(name: str = "JobAutoSystem") -> logging.Logger:
    """Configures and returns a custom logger."""
    
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Prevent adding multiple handlers if logger is imported multiple times
    if not logger.handlers:
        # Create formatter
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(module)s:%(lineno)d | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Console Handler (Prints to terminal)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)

        # File Handler (Saves to file)
        file_handler = logging.FileHandler("logs/app.log")
        file_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger

# Global logger instance
logger = setup_logger()