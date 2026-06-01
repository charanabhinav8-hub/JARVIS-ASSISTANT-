import os
import shutil
from pathlib import Path
from utils.logger import logger

class FileOperations:
    """File management operations"""
    
    @staticmethod
    def create_file(filepath, content=""):
        """Create a new file"""
        try:
            Path(filepath).parent.mkdir(parents=True, exist_ok=True)
            with open(filepath, 'w') as f:
                f.write(content)
            logger.info(f"File created: {filepath}")
            return True, f"File created: {filepath}"
        except Exception as e:
            logger.error(f"Failed to create file: {e}")
            return False, f"Failed to create file: {str(e)}"
    
    @staticmethod
    def delete_file(filepath):
        """Delete a file"""
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                logger.info(f"File deleted: {filepath}")
                return True, f"File deleted: {filepath}"
            else:
                return False, f"File not found: {filepath}"
        except Exception as e:
            logger.error(f"Failed to delete file: {e}")
            return False, f"Failed to delete file: {str(e)}"
    
    @staticmethod
    def read_file(filepath):
        """Read file content"""
        try:
            with open(filepath, 'r') as f:
                content = f.read()
            logger.info(f"File read: {filepath}")
            return True, content
        except Exception as e:
            logger.error(f"Failed to read file: {e}")
            return False, f"Failed to read file: {str(e)}"
    
    @staticmethod
    def write_file(filepath, content):
        """Write content to file"""
        try:
            with open(filepath, 'w') as f:
                f.write(content)
            logger.info(f"File written: {filepath}")
            return True, f"File written: {filepath}"
        except Exception as e:
            logger.error(f"Failed to write file: {e}")
            return False, f"Failed to write file: {str(e)}"
    
    @staticmethod
    def copy_file(source, destination):
        """Copy a file"""
        try:
            shutil.copy2(source, destination)
            logger.info(f"File copied from {source} to {destination}")
            return True, f"File copied to {destination}"
        except Exception as e:
            logger.error(f"Failed to copy file: {e}")
            return False, f"Failed to copy file: {str(e)}"
    
    @staticmethod
    def move_file(source, destination):
        """Move a file"""
        try:
            shutil.move(source, destination)
            logger.info(f"File moved from {source} to {destination}")
            return True, f"File moved to {destination}"
        except Exception as e:
            logger.error(f"Failed to move file: {e}")
            return False, f"Failed to move file: {str(e)}"
    
    @staticmethod
    def rename_file(filepath, new_name):
        """Rename a file"""
        try:
            new_path = os.path.join(os.path.dirname(filepath), new_name)
            os.rename(filepath, new_path)
            logger.info(f"File renamed from {filepath} to {new_path}")
            return True, f"File renamed to {new_name}"
        except Exception as e:
            logger.error(f"Failed to rename file: {e}")
            return False, f"Failed to rename file: {str(e)}"
    
    @staticmethod
    def list_files(directory):
        """List files in directory"""
        try:
            if os.path.isdir(directory):
                files = os.listdir(directory)
                logger.info(f"Listed files in {directory}")
                return True, files
            else:
                return False, f"Directory not found: {directory}"
        except Exception as e:
            logger.error(f"Failed to list files: {e}")
            return False, f"Failed to list files: {str(e)}"
    
    @staticmethod
    def create_directory(directory):
        """Create a directory"""
        try:
            Path(directory).mkdir(parents=True, exist_ok=True)
            logger.info(f"Directory created: {directory}")
            return True, f"Directory created: {directory}"
        except Exception as e:
            logger.error(f"Failed to create directory: {e}")
            return False, f"Failed to create directory: {str(e)}"
    
    @staticmethod
    def delete_directory(directory):
        """Delete a directory"""
        try:
            if os.path.exists(directory):
                shutil.rmtree(directory)
                logger.info(f"Directory deleted: {directory}")
                return True, f"Directory deleted: {directory}"
            else:
                return False, f"Directory not found: {directory}"
        except Exception as e:
            logger.error(f"Failed to delete directory: {e}")
            return False, f"Failed to delete directory: {str(e)}"
    
    @staticmethod
    def get_file_info(filepath):
        """Get file information"""
        try:
            stat_info = os.stat(filepath)
            info = {
                'size': stat_info.st_size,
                'created': stat_info.st_ctime,
                'modified': stat_info.st_mtime,
                'accessed': stat_info.st_atime
            }
            logger.info(f"File info retrieved: {filepath}")
            return True, info
        except Exception as e:
            logger.error(f"Failed to get file info: {e}")
            return False, f"Failed to get file info: {str(e)}"
