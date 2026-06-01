import os
import google.generativeai as genai
from dotenv import load_dotenv
from utils.logger import logger
from utils.helpers import ConfigManager

load_dotenv()

class GeminiAI:
    """Google Gemini AI integration"""
    
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.config = ConfigManager()
        
        if not self.api_key:
            logger.error("GEMINI_API_KEY not found in environment variables")
            raise ValueError("GEMINI_API_KEY is required")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(
            model_name=self.config.get("gemini.model", "gemini-pro"),
            generation_config=self._get_generation_config()
        )
        logger.info("Gemini AI initialized")
    
    def _get_generation_config(self):
        """Get generation configuration"""
        return {
            "temperature": self.config.get("gemini.temperature", 0.7),
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": self.config.get("gemini.max_output_tokens", 2048),
        }
    
    def generate_response(self, prompt, context=None):
        """Generate response from Gemini"""
        try:
            if context:
                full_prompt = f"{context}\n\nUser Query: {prompt}"
            else:
                full_prompt = prompt
            
            response = self.model.generate_content(full_prompt)
            
            if response and response.text:
                logger.info(f"Gemini response generated: {response.text[:100]}...")
                return response.text
            else:
                logger.warning("Empty response from Gemini")
                return "I'm unable to generate a response at the moment."
        
        except Exception as e:
            logger.error(f"Error generating Gemini response: {e}")
            return "An error occurred while processing your request."
    
    def chat(self, user_message, system_context=None):
        """Chat with Gemini"""
        system_prompt = system_context or "You are JARVIS, an intelligent personal computer assistant. You are helpful, professional, and efficient."
        
        full_prompt = f"{system_prompt}\n\nUser: {user_message}"
        return self.generate_response(full_prompt)
    
    def extract_intent(self, user_input):
        """Extract intent from user input"""
        prompt = f"""
        You are an intent extraction system. Analyze the following user input and extract:
        1. The main intent (action the user wants)
        2. The objects/parameters involved
        3. Confidence level (0-1)
        
        User Input: {user_input}
        
        Respond in JSON format with keys: intent, parameters, confidence
        """
        
        try:
            response = self.model.generate_content(prompt)
            if response and response.text:
                import json
                # Try to parse JSON from response
                text = response.text
                start = text.find('{')
                end = text.rfind('}') + 1
                if start >= 0 and end > start:
                    json_str = text[start:end]
                    return json.loads(json_str)
        except Exception as e:
            logger.error(f"Error extracting intent: {e}")
        
        return {"intent": None, "parameters": {}, "confidence": 0.0}
    
    def get_system_prompt(self):
        """Get system prompt for JARVIS"""
        return """You are JARVIS, an advanced personal computer assistant inspired by Iron Man's AI butler. 
You are:
- Highly intelligent and knowledgeable
- Professional yet personable
- Efficient and action-oriented
- Privacy-conscious and secure
- Able to perform various computer tasks

When users ask you to do something, provide clear instructions or confirmations. 
For dangerous operations, ask for confirmation."""

# Create global Gemini instance
try:
    gemini = GeminiAI()
except Exception as e:
    logger.error(f"Failed to initialize Gemini: {e}")
    gemini = None
