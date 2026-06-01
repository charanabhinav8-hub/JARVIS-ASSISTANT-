import os
import platform
import subprocess
from utils.logger import logger

class ApplicationControl:
    """Control various applications"""
    
    # Application paths for different OS
    APP_PATHS = {
        'Windows': {
            'chrome': 'chrome',
            'firefox': 'firefox',
            'notepad': 'notepad',
            'calculator': 'calc',
            'word': 'winword',
            'excel': 'excel',
            'powershell': 'powershell',
            'cmd': 'cmd'
        },
        'Darwin': {
            'chrome': '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
            'firefox': '/Applications/Firefox.app/Contents/MacOS/Firefox',
            'notepad': 'TextEdit',
            'calculator': '/Applications/Calculator.app/Contents/MacOS/Calculator',
            'word': '/Applications/Microsoft Word.app/Contents/MacOS/Microsoft Word',
            'excel': '/Applications/Microsoft Excel.app/Contents/MacOS/Microsoft Excel'
        },
        'Linux': {
            'chrome': 'google-chrome',
            'firefox': 'firefox',
            'notepad': 'gedit',
            'calculator': 'gnome-calculator',
            'text_editor': 'nano'
        }
    }
    
    @staticmethod
    def open_browser(url=None, browser='chrome'):
        """Open a web browser"""
        try:
            if platform.system() == "Windows":
                if url:
                    os.system(f"start {browser} {url}")
                else:
                    os.system(f"start {browser}")
            elif platform.system() == "Darwin":
                if url:
                    os.system(f"open -a {browser} {url}")
                else:
                    os.system(f"open -a {browser}")
            else:  # Linux
                if url:
                    os.system(f"{browser} {url} &")
                else:
                    os.system(f"{browser} &")
            
            logger.info(f"Opened {browser} with URL: {url}")
            return True, f"Opening {browser}"
        except Exception as e:
            logger.error(f"Failed to open browser: {e}")
            return False, str(e)
    
    @staticmethod
    def open_text_editor(filepath=None):
        """Open a text editor"""
        try:
            if platform.system() == "Windows":
                if filepath:
                    os.system(f"notepad {filepath}")
                else:
                    os.system("notepad")
            elif platform.system() == "Darwin":
                if filepath:
                    os.system(f"open -a TextEdit {filepath}")
                else:
                    os.system("open -a TextEdit")
            else:  # Linux
                if filepath:
                    os.system(f"gedit {filepath} &")
                else:
                    os.system("gedit &")
            
            logger.info(f"Opened text editor: {filepath}")
            return True, "Text editor opened"
        except Exception as e:
            logger.error(f"Failed to open text editor: {e}")
            return False, str(e)
    
    @staticmethod
    def open_file_explorer(path=None):
        """Open file explorer"""
        try:
            if not path:
                path = os.path.expanduser("~")
            
            if platform.system() == "Windows":
                os.system(f"explorer {path}")
            elif platform.system() == "Darwin":
                os.system(f"open {path}")
            else:  # Linux
                os.system(f"nautilus {path} &")
            
            logger.info(f"Opened file explorer: {path}")
            return True, "File explorer opened"
        except Exception as e:
            logger.error(f"Failed to open file explorer: {e}")
            return False, str(e)
    
    @staticmethod
    def open_settings():
        """Open system settings"""
        try:
            if platform.system() == "Windows":
                os.system("start ms-settings:")
            elif platform.system() == "Darwin":
                os.system("open /System/Library/PreferencePanes/")
            else:  # Linux
                os.system("gnome-control-center &")
            
            logger.info("Opened system settings")
            return True, "Settings opened"
        except Exception as e:
            logger.error(f"Failed to open settings: {e}")
            return False, str(e)
    
    @staticmethod
    def minimize_all_windows():
        """Minimize all windows"""
        try:
            if platform.system() == "Windows":
                os.system("explorer /minimize")
            elif platform.system() == "Darwin":
                os.system("osascript -e 'tell application \"System Events\" to set visible of every window to false'")
            logger.info("Minimized all windows")
            return True, "All windows minimized"
        except Exception as e:
            logger.error(f"Failed to minimize windows: {e}")
            return False, str(e)
    
    @staticmethod
    def maximize_window():
        """Maximize active window"""
        try:
            if platform.system() == "Windows":
                os.system("explorer /maximize")
            logger.info("Maximized window")
            return True, "Window maximized"
        except Exception as e:
            logger.error(f"Failed to maximize window: {e}")
            return False, str(e)
    
    @staticmethod
    def take_screenshot(filepath=None):
        """Take a screenshot"""
        try:
            if filepath is None:
                filepath = "screenshot.png"
            
            if platform.system() == "Windows":
                from PIL import ImageGrab
                img = ImageGrab.grab()
                img.save(filepath)
            elif platform.system() == "Darwin":
                os.system(f"screencapture {filepath}")
            else:  # Linux
                os.system(f"import -window root {filepath}")
            
            logger.info(f"Screenshot saved: {filepath}")
            return True, f"Screenshot saved: {filepath}"
        except Exception as e:
            logger.error(f"Failed to take screenshot: {e}")
            return False, str(e)
