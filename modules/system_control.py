import os
import platform
import subprocess
import psutil
from utils.logger import logger

class SystemControl:
    """System control operations"""
    
    @staticmethod
    def get_system_info():
        """Get system information"""
        try:
            info = {
                'os': platform.system(),
                'os_version': platform.version(),
                'hostname': platform.node(),
                'processor': platform.processor(),
                'python_version': platform.python_version(),
                'cpu_count': psutil.cpu_count(),
                'total_memory': psutil.virtual_memory().total,
                'available_memory': psutil.virtual_memory().available,
                'cpu_percent': psutil.cpu_percent(interval=1)
            }
            logger.info("System info retrieved")
            return True, info
        except Exception as e:
            logger.error(f"Failed to get system info: {e}")
            return False, str(e)
    
    @staticmethod
    def get_cpu_usage():
        """Get CPU usage"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            logger.info(f"CPU usage: {cpu_percent}%")
            return True, cpu_percent
        except Exception as e:
            logger.error(f"Failed to get CPU usage: {e}")
            return False, str(e)
    
    @staticmethod
    def get_memory_usage():
        """Get memory usage"""
        try:
            memory = psutil.virtual_memory()
            memory_info = {
                'total': memory.total,
                'used': memory.used,
                'available': memory.available,
                'percent': memory.percent
            }
            logger.info(f"Memory usage: {memory.percent}%")
            return True, memory_info
        except Exception as e:
            logger.error(f"Failed to get memory usage: {e}")
            return False, str(e)
    
    @staticmethod
    def get_disk_usage(path="/"):
        """Get disk usage"""
        try:
            disk = psutil.disk_usage(path)
            disk_info = {
                'total': disk.total,
                'used': disk.used,
                'free': disk.free,
                'percent': disk.percent
            }
            logger.info(f"Disk usage for {path}: {disk.percent}%")
            return True, disk_info
        except Exception as e:
            logger.error(f"Failed to get disk usage: {e}")
            return False, str(e)
    
    @staticmethod
    def open_application(app_name):
        """Open an application"""
        try:
            if platform.system() == "Windows":
                os.system(f"start {app_name}")
            elif platform.system() == "Darwin":  # macOS
                os.system(f"open -a {app_name}")
            else:  # Linux
                os.system(f"{app_name} &")
            
            logger.info(f"Opened application: {app_name}")
            return True, f"Opening {app_name}"
        except Exception as e:
            logger.error(f"Failed to open application: {e}")
            return False, str(e)
    
    @staticmethod
    def close_application(app_name):
        """Close an application"""
        try:
            if platform.system() == "Windows":
                os.system(f"taskkill /IM {app_name}.exe")
            elif platform.system() == "Darwin":  # macOS
                os.system(f"pkill {app_name}")
            else:  # Linux
                os.system(f"pkill {app_name}")
            
            logger.info(f"Closed application: {app_name}")
            return True, f"Closed {app_name}"
        except Exception as e:
            logger.error(f"Failed to close application: {e}")
            return False, str(e)
    
    @staticmethod
    def list_running_processes():
        """List running processes"""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'status']):
                try:
                    processes.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'status': proc.info['status']
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            logger.info(f"Listed {len(processes)} processes")
            return True, processes
        except Exception as e:
            logger.error(f"Failed to list processes: {e}")
            return False, str(e)
    
    @staticmethod
    def execute_command(command):
        """Execute a system command"""
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
            logger.info(f"Command executed: {command}")
            return True, result.stdout if result.stdout else "Command executed successfully"
        except subprocess.TimeoutExpired:
            logger.error(f"Command timeout: {command}")
            return False, "Command execution timed out"
        except Exception as e:
            logger.error(f"Failed to execute command: {e}")
            return False, str(e)
    
    @staticmethod
    def shutdown_computer():
        """Shutdown the computer"""
        try:
            logger.warning("Initiating system shutdown")
            if platform.system() == "Windows":
                os.system("shutdown /s /t 30")
            elif platform.system() == "Darwin":  # macOS
                os.system("sudo shutdown -h now")
            else:  # Linux
                os.system("sudo shutdown -h now")
            return True, "System shutdown initiated"
        except Exception as e:
            logger.error(f"Failed to shutdown: {e}")
            return False, str(e)
    
    @staticmethod
    def restart_computer():
        """Restart the computer"""
        try:
            logger.warning("Initiating system restart")
            if platform.system() == "Windows":
                os.system("shutdown /r /t 30")
            elif platform.system() == "Darwin":  # macOS
                os.system("sudo shutdown -r now")
            else:  # Linux
                os.system("sudo shutdown -r now")
            return True, "System restart initiated"
        except Exception as e:
            logger.error(f"Failed to restart: {e}")
            return False, str(e)
