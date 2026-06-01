import logging
import json
from pathlib import Path
from datetime import datetime

class JarvisLogger:
    """Custom logger for JARVIS assistant"""
    
    def __init__(self, name="JARVIS"):
        self.name = name
        self.logger = logging.getLogger(name)
        self.setup_logger()
    
    def setup_logger(self):
        """Setup logger configuration"""
        # Create logs directory if it doesn't exist
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # Set log level
        self.logger.setLevel(logging.DEBUG)
        
        # Create formatters
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # File handler
        file_handler = logging.FileHandler(log_dir / "jarvis.log")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
    
    def info(self, message):
        """Log info message"""
        self.logger.info(message)
    
    def debug(self, message):
        """Log debug message"""
        self.logger.debug(message)
    
    def warning(self, message):
        """Log warning message"""
        self.logger.warning(message)
    
    def error(self, message):
        """Log error message"""
        self.logger.error(message)
    
    def critical(self, message):
        """Log critical message"""
        self.logger.critical(message)
    
    def log_command(self, user_input, response, execution_time):
        """Log command execution"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "command": user_input,
            "response": response,
            "execution_time": execution_time
        }
        self.debug(f"Command: {json.dumps(log_entry)}")

# Create global logger instance
logger = JarvisLogger()
