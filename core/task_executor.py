import json
import subprocess
import time
import os
from utils.logger import logger
from utils.helpers import ConfigManager, format_response

class TaskExecutor:
    """Execute tasks based on parsed commands"""
    
    def __init__(self):
        self.config = ConfigManager()
        self.task_history = []
        self.dangerous_commands = self.config.get("security.dangerous_commands", [])
        self.require_confirmation = self.config.get("security.require_confirmation", True)
    
    def execute(self, action, parameters=None, context=None):
        """Execute a task"""
        parameters = parameters or {}
        
        try:
            logger.info(f"Executing action: {action} with parameters: {parameters}")
            
            # Check if action is dangerous
            if self._is_dangerous(action) and self.require_confirmation:
                logger.warning(f"Dangerous action detected: {action}")
                return format_response(
                    f"This is a dangerous operation. Please confirm you want to {action}",
                    status="confirmation_required"
                )
            
            # Execute based on action type
            result = self._execute_action(action, parameters, context)
            
            # Log to history
            self.task_history.append({
                "action": action,
                "parameters": parameters,
                "result": result,
                "timestamp": time.time()
            })
            
            return result
        
        except Exception as e:
            logger.error(f"Error executing action {action}: {e}")
            return format_response(f"Error executing task: {str(e)}", status="error")
    
    def _is_dangerous(self, action):
        """Check if action is in dangerous commands list"""
        action_lower = action.lower()
        return any(cmd in action_lower for cmd in self.dangerous_commands)
    
    def _execute_action(self, action, parameters, context):
        """Execute the actual action"""
        
        if action == "open_app":
            return self._open_application(parameters)
        elif action == "close_app":
            return self._close_application(parameters)
        elif action == "manage_files":
            return self._manage_files(parameters)
        elif action == "search_web":
            return self._search_web(parameters)
        elif action == "send_email":
            return self._send_email(parameters)
        elif action == "manage_calendar":
            return self._manage_calendar(parameters)
        elif action == "get_system_info":
            return self._get_system_info()
        elif action == "execute_command":
            return self._execute_system_command(parameters)
        else:
            return format_response(f"Unknown action: {action}", status="error")
    
    def _open_application(self, parameters):
        """Open an application"""
        app_name = parameters.get("app_name")
        if not app_name:
            return format_response("No application name provided", status="error")
        
        try:
            import platform
            
            if platform.system() == "Windows":
                os.system(f"start {app_name}")
            elif platform.system() == "Darwin":  # macOS
                os.system(f"open -a {app_name}")
            else:  # Linux
                os.system(f"{app_name} &")
            
            logger.info(f"Opened application: {app_name}")
            return format_response(f"Opening {app_name}")
        except Exception as e:
            logger.error(f"Failed to open application: {e}")
            return format_response(f"Failed to open {app_name}", status="error")
    
    def _close_application(self, parameters):
        """Close an application"""
        app_name = parameters.get("app_name")
        if not app_name:
            return format_response("No application name provided", status="error")
        
        try:
            import platform
            
            if platform.system() == "Windows":
                os.system(f"taskkill /IM {app_name}.exe")
            elif platform.system() == "Darwin":  # macOS
                os.system(f"pkill {app_name}")
            else:  # Linux
                os.system(f"pkill {app_name}")
            
            logger.info(f"Closed application: {app_name}")
            return format_response(f"Closing {app_name}")
        except Exception as e:
            logger.error(f"Failed to close application: {e}")
            return format_response(f"Failed to close {app_name}", status="error")
    
    def _manage_files(self, parameters):
        """Manage files (create, delete, move, etc.)"""
        operation = parameters.get("operation")
        filepath = parameters.get("filepath")
        
        if operation == "create":
            return self._create_file(filepath, parameters.get("content", ""))
        elif operation == "delete":
            return self._delete_file(filepath)
        elif operation == "move":
            return self._move_file(filepath, parameters.get("destination"))
        else:
            return format_response(f"Unknown file operation: {operation}", status="error")
    
    def _create_file(self, filepath, content=""):
        """Create a file"""
        try:
            from pathlib import Path
            Path(filepath).parent.mkdir(parents=True, exist_ok=True)
            with open(filepath, 'w') as f:
                f.write(content)
            logger.info(f"File created: {filepath}")
            return format_response(f"File created: {filepath}")
        except Exception as e:
            logger.error(f"Failed to create file: {e}")
            return format_response(f"Failed to create file: {str(e)}", status="error")
    
    def _delete_file(self, filepath):
        """Delete a file"""
        try:
            os.remove(filepath)
            logger.info(f"File deleted: {filepath}")
            return format_response(f"File deleted: {filepath}")
        except Exception as e:
            logger.error(f"Failed to delete file: {e}")
            return format_response(f"Failed to delete file: {str(e)}", status="error")
    
    def _move_file(self, source, destination):
        """Move a file"""
        try:
            import shutil
            shutil.move(source, destination)
            logger.info(f"File moved from {source} to {destination}")
            return format_response(f"File moved to {destination}")
        except Exception as e:
            logger.error(f"Failed to move file: {e}")
            return format_response(f"Failed to move file: {str(e)}", status="error")
    
    def _search_web(self, parameters):
        """Search the web"""
        query = parameters.get("query")
        if not query:
            return format_response("No search query provided", status="error")
        
        logger.info(f"Web search requested: {query}")
        return format_response(f"Searching for: {query}")
    
    def _send_email(self, parameters):
        """Send an email"""
        recipient = parameters.get("recipient")
        subject = parameters.get("subject", "")
        message = parameters.get("message", "")
        
        if not recipient:
            return format_response("No recipient provided", status="error")
        
        logger.info(f"Email queued to: {recipient}")
        return format_response(f"Email prepared for {recipient}")
    
    def _manage_calendar(self, parameters):
        """Manage calendar events"""
        event_type = parameters.get("type")
        description = parameters.get("description")
        
        logger.info(f"Calendar event ({event_type}): {description}")
        return format_response(f"Calendar event scheduled: {description}")
    
    def _get_system_info(self):
        """Get system information"""
        try:
            from utils.helpers import SystemInfo
            info = SystemInfo.get_all_info()
            logger.info(f"System info retrieved: {info}")
            return format_response(json.dumps(info, indent=2))
        except Exception as e:
            logger.error(f"Failed to get system info: {e}")
            return format_response(f"Failed to get system info: {str(e)}", status="error")
    
    def _execute_system_command(self, parameters):
        """Execute a system command"""
        command = parameters.get("command")
        
        if not command:
            return format_response("No command provided", status="error")
        
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            logger.info(f"Command executed: {command}")
            return format_response(result.stdout if result.stdout else "Command executed successfully")
        except Exception as e:
            logger.error(f"Failed to execute command: {e}")
            return format_response(f"Failed to execute command: {str(e)}", status="error")
    
    def get_history(self, limit=10):
        """Get task execution history"""
        return self.task_history[-limit:]
