import os
import json
import platform
from pathlib import Path
from datetime import datetime
from utils.logger import logger

class ConfigManager:
    """Manage configuration files"""
    
    def __init__(self, config_path="config/config.json"):
        self.config_path = config_path
        self.config = self.load_config()
    
    def load_config(self):
        """Load configuration from JSON file"""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"Config file not found at {self.config_path}")
            return {}
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON in {self.config_path}")
            return {}
    
    def get(self, key, default=None):
        """Get configuration value by key (supports dot notation)"""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default
    
    def save(self):
        """Save configuration to file"""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
            logger.info("Configuration saved successfully")
        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")

class CommandParser:
    """Parse and extract intent from user commands"""
    
    def __init__(self, commands_path="config/commands.json"):
        self.commands_path = commands_path
        self.commands = self.load_commands()
    
    def load_commands(self):
        """Load commands from JSON file"""
        try:
            with open(self.commands_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"Commands file not found at {self.commands_path}")
            return {"commands": {}}
    
    def parse_intent(self, user_input):
        """Parse user input and identify intent"""
        user_input_lower = user_input.lower()
        
        for command_name, command_data in self.commands.get("commands", {}).items():
            patterns = command_data.get("patterns", [])
            for pattern in patterns:
                if pattern in user_input_lower:
                    return {
                        "intent": command_name,
                        "action": command_data.get("action"),
                        "confidence": 0.8
                    }
        
        return {"intent": None, "action": None, "confidence": 0.0}

class SystemInfo:
    """Get system information"""
    
    @staticmethod
    def get_os():
        """Get operating system"""
        return platform.system()
    
    @staticmethod
    def get_os_version():
        """Get OS version"""
        return platform.version()
    
    @staticmethod
    def get_python_version():
        """Get Python version"""
        return platform.python_version()
    
    @staticmethod
    def get_processor():
        """Get processor information"""
        return platform.processor()
    
    @staticmethod
    def get_hostname():
        """Get hostname"""
        return platform.node()
    
    @staticmethod
    def get_all_info():
        """Get all system information"""
        return {
            "os": SystemInfo.get_os(),
            "os_version": SystemInfo.get_os_version(),
            "python_version": SystemInfo.get_python_version(),
            "processor": SystemInfo.get_processor(),
            "hostname": SystemInfo.get_hostname()
        }

class FileManager:
    """Utility functions for file operations"""
    
    @staticmethod
    def create_file(filepath, content=""):
        """Create a new file"""
        try:
            Path(filepath).parent.mkdir(parents=True, exist_ok=True)
            with open(filepath, 'w') as f:
                f.write(content)
            logger.info(f"File created: {filepath}")
            return True
        except Exception as e:
            logger.error(f"Failed to create file: {e}")
            return False
    
    @staticmethod
    def delete_file(filepath):
        """Delete a file"""
        try:
            os.remove(filepath)
            logger.info(f"File deleted: {filepath}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete file: {e}")
            return False
    
    @staticmethod
    def read_file(filepath):
        """Read file content"""
        try:
            with open(filepath, 'r') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Failed to read file: {e}")
            return None
    
    @staticmethod
    def write_file(filepath, content):
        """Write content to file"""
        try:
            with open(filepath, 'w') as f:
                f.write(content)
            logger.info(f"File written: {filepath}")
            return True
        except Exception as e:
            logger.error(f"Failed to write to file: {e}")
            return False

def get_timestamp():
    """Get current timestamp"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def format_response(message, status="success"):
    """Format response message"""
    return {
        "status": status,
        "message": message,
        "timestamp": get_timestamp()
    }
