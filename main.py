#!/usr/bin/env python3
"""
JARVIS - Personal Computer Assistant
A sophisticated AI-powered assistant for complete computer control
"""

import os
import sys
import time
import json
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from core.voice import VoiceAssistant
from core.gemini import gemini
from core.nlp import NLPProcessor
from core.task_executor import TaskExecutor
from utils.logger import logger
from utils.helpers import ConfigManager, CommandParser, SystemInfo

class JARVIS:
    """Main JARVIS Assistant Class"""
    
    def __init__(self):
        logger.info("=" * 50)
        logger.info("Initializing JARVIS Assistant")
        logger.info("=" * 50)
        
        self.config = ConfigManager()
        self.voice_assistant = VoiceAssistant()
        self.nlp_processor = NLPProcessor()
        self.task_executor = TaskExecutor()
        self.command_parser = CommandParser()
        
        self.wake_word = self.config.get("assistant.wake_word", "hey jarvis")
        self.running = False
        
        logger.info("JARVIS initialized successfully")
    
    def start(self):
        """Start JARVIS"""
        self.running = True
        logger.info("JARVIS started")
        
        print("\n" + "=" * 60)
        print("JARVIS - Personal Computer Assistant".center(60))
        print("=" * 60)
        print(f"\nWake word: '{self.wake_word}'")
        print("Press Ctrl+C to exit\n")
        
        # Greet user
        greeting = "Good day! I'm JARVIS, your personal assistant. I'm ready to help you with any task. What would you like me to do?"
        print(f"\nJARVIS: {greeting}")
        self.voice_assistant.respond(greeting)
        
        # Main loop
        try:
            while self.running:
                self.listen_and_process()
        except KeyboardInterrupt:
            self.shutdown()
    
    def listen_and_process(self):
        """Listen for commands and process them"""
        try:
            # Listen for user input
            user_input = self.voice_assistant.listen_and_respond()
            
            if not user_input:
                return
            
            print(f"\nYou: {user_input}")
            
            # Check for wake word
            if not self.voice_assistant.voice_input.detect_wake_word(user_input, self.wake_word):
                logger.debug("Wake word not detected")
                return
            
            # Remove wake word from input
            command = user_input.lower().replace(self.wake_word.lower(), "").strip()
            
            if not command:
                response = "I'm listening. What can I help you with?"
                print(f"\nJARVIS: {response}")
                self.voice_assistant.respond(response)
                return
            
            logger.info(f"Processing command: {command}")
            
            # Parse command with NLP
            parsed_command = self.nlp_processor.parse_command(command)
            logger.debug(f"Parsed command: {parsed_command}")
            
            # Get response from Gemini
            system_prompt = gemini.get_system_prompt() if gemini else "You are JARVIS"
            response = self.process_command(command, parsed_command, system_prompt)
            
            print(f"\nJARVIS: {response}")
            self.voice_assistant.respond(response)
        
        except Exception as e:
            logger.error(f"Error in listen_and_process: {e}")
            error_response = "I encountered an error processing your request. Please try again."
            print(f"\nJARVIS: {error_response}")
            self.voice_assistant.respond(error_response)
    
    def process_command(self, command, parsed_command, system_prompt):
        """Process user command and return response"""
        try:
            action = parsed_command.get("action")
            intent = parsed_command.get("intent")
            
            # Special handling for specific intents
            if intent == "greeting":
                return "Hello! How can I assist you today?"
            elif intent == "help":
                return self.get_help_text()
            elif intent == "time":
                from datetime import datetime
                return f"The current time is {datetime.now().strftime('%I:%M %p')}"
            elif intent == "date":
                from datetime import datetime
                return f"Today is {datetime.now().strftime('%A, %B %d, %Y')}"
            elif intent == "system_info":
                info = SystemInfo.get_all_info()
                return f"System: {info['os']}, Processor: {info['processor']}, Python: {info['python_version']}"
            
            # Use Gemini for general responses
            if gemini:
                response = gemini.chat(command, system_prompt)
                return response
            else:
                return "I'm having trouble connecting to my AI engine. Please try again later."
        
        except Exception as e:
            logger.error(f"Error processing command: {e}")
            return "I encountered an error processing your request."
    
    def get_help_text(self):
        """Get help text"""
        return """
I can help you with:
- Opening and closing applications
- Managing files
- Searching the web
- Sending emails
- Managing your calendar
- Getting system information
- Controlling your computer
- And much more!

What would you like me to do?
"""
    
    def shutdown(self):
        """Shutdown JARVIS"""
        logger.info("Shutting down JARVIS")
        self.running = False
        
        goodbye_message = "Thank you for using JARVIS. Goodbye!"
        print(f"\nJARVIS: {goodbye_message}")
        self.voice_assistant.respond(goodbye_message)
        
        print("\n" + "=" * 60)
        print("JARVIS - Shutdown".center(60))
        print("=" * 60)

def main():
    """Main entry point"""
    try:
        jarvis = JARVIS()
        jarvis.start()
    except Exception as e:
        logger.critical(f"Fatal error: {e}")
        print(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
