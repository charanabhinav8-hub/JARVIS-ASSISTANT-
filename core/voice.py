import speech_recognition as sr
from gtts import gTTS
import pyttsx3
import os
from utils.logger import logger
from utils.helpers import ConfigManager

class VoiceInput:
    """Handle voice input from microphone"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.config = ConfigManager()
        self.microphone = sr.Microphone()
        
    def listen(self):
        """Listen to microphone input"""
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source)
                logger.info("Listening...")
                audio = self.recognizer.listen(
                    source,
                    timeout=self.config.get("voice.timeout", 10),
                    phrase_time_limit=self.config.get("voice.phrase_time_limit", 10)
                )
            
            # Try Google Speech Recognition
            text = self.recognizer.recognize_google(audio)
            logger.info(f"User said: {text}")
            return text
        
        except sr.UnknownValueValue:
            logger.warning("Could not understand audio")
            return None
        except sr.RequestError as e:
            logger.error(f"Speech recognition error: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error in voice input: {e}")
            return None
    
    def detect_wake_word(self, text, wake_word="hey jarvis"):
        """Detect wake word in text"""
        if text and wake_word.lower() in text.lower():
            return True
        return False

class VoiceOutput:
    """Handle voice output using text-to-speech"""
    
    def __init__(self):
        self.config = ConfigManager()
        self.engine = pyttsx3.init()
        self.setup_engine()
    
    def setup_engine(self):
        """Setup text-to-speech engine"""
        try:
            self.engine.setProperty('rate', 150)  # Speed
            self.engine.setProperty('volume', self.config.get("assistant.voice_volume", 1.0))
            logger.info("TTS engine initialized")
        except Exception as e:
            logger.error(f"Failed to setup TTS engine: {e}")
    
    def speak(self, text):
        """Speak text using pyttsx3"""
        try:
            logger.info(f"Speaking: {text}")
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            logger.error(f"Failed to speak: {e}")
    
    def speak_gTTS(self, text, lang='en', filename='temp_audio.mp3'):
        """Speak text using Google Text-to-Speech"""
        try:
            tts = gTTS(text=text, lang=lang, slow=False)
            tts.save(filename)
            logger.info(f"Saved audio: {filename}")
            
            # Play the audio (cross-platform)
            import platform
            if platform.system() == 'Darwin':  # macOS
                os.system(f'afplay {filename}')
            elif platform.system() == 'Windows':
                os.system(f'start {filename}')
            else:  # Linux
                os.system(f'mpg123 {filename}')
            
            # Clean up
            if os.path.exists(filename):
                os.remove(filename)
        
        except Exception as e:
            logger.error(f"Failed to speak with gTTS: {e}")

class VoiceAssistant:
    """Main voice assistant handler"""
    
    def __init__(self):
        self.voice_input = VoiceInput()
        self.voice_output = VoiceOutput()
        self.config = ConfigManager()
    
    def greet(self):
        """Greet the user"""
        greeting = "Hello! I'm JARVIS, your personal assistant. How can I help you today?"
        self.voice_output.speak(greeting)
    
    def listen_and_respond(self):
        """Listen for commands and return the text"""
        text = self.voice_input.listen()
        if text:
            return text
        return None
    
    def respond(self, message):
        """Respond with a message"""
        self.voice_output.speak(message)
