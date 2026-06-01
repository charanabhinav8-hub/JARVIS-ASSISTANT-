import spacy
from utils.logger import logger
from utils.helpers import CommandParser

class NLPProcessor:
    """Natural Language Processing using spaCy"""
    
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
            logger.info("spaCy model loaded successfully")
        except OSError:
            logger.warning("spaCy model not found. Run: python -m spacy download en_core_web_sm")
            self.nlp = None
        
        self.command_parser = CommandParser()
    
    def extract_entities(self, text):
        """Extract named entities from text"""
        if not self.nlp:
            return []
        
        try:
            doc = self.nlp(text)
            entities = []
            for ent in doc.ents:
                entities.append({
                    "text": ent.text,
                    "label": ent.label_,
                    "start": ent.start_char,
                    "end": ent.end_char
                })
            return entities
        except Exception as e:
            logger.error(f"Error extracting entities: {e}")
            return []
    
    def tokenize(self, text):
        """Tokenize text"""
        if not self.nlp:
            return text.split()
        
        try:
            doc = self.nlp(text)
            tokens = [token.text for token in doc]
            return tokens
        except Exception as e:
            logger.error(f"Error tokenizing text: {e}")
            return text.split()
    
    def get_pos_tags(self, text):
        """Get Part-of-Speech tags"""
        if not self.nlp:
            return []
        
        try:
            doc = self.nlp(text)
            pos_tags = [(token.text, token.pos_) for token in doc]
            return pos_tags
        except Exception as e:
            logger.error(f"Error getting POS tags: {e}")
            return []
    
    def extract_actions(self, text):
        """Extract action verbs from text"""
        if not self.nlp:
            return []
        
        try:
            doc = self.nlp(text)
            actions = [token.text for token in doc if token.pos_ == "VERB"]
            return actions
        except Exception as e:
            logger.error(f"Error extracting actions: {e}")
            return []
    
    def extract_objects(self, text):
        """Extract objects/nouns from text"""
        if not self.nlp:
            return []
        
        try:
            doc = self.nlp(text)
            objects = [token.text for token in doc if token.pos_ in ["NOUN", "PROPN"]]
            return objects
        except Exception as e:
            logger.error(f"Error extracting objects: {e}")
            return []
    
    def parse_command(self, text):
        """Parse command using both spaCy and command patterns"""
        entities = self.extract_entities(text)
        actions = self.extract_actions(text)
        objects = self.extract_objects(text)
        intent_data = self.command_parser.parse_intent(text)
        
        return {
            "original_text": text,
            "entities": entities,
            "actions": actions,
            "objects": objects,
            "intent": intent_data.get("intent"),
            "action": intent_data.get("action"),
            "confidence": intent_data.get("confidence")
        }

class SemanticAnalyzer:
    """Analyze semantic similarity between texts"""
    
    def __init__(self):
        self.nlp = None
        try:
            self.nlp = spacy.load("en_core_web_md")
            logger.info("spaCy medium model loaded for semantic analysis")
        except OSError:
            logger.warning("spaCy medium model not found. Run: python -m spacy download en_core_web_md")
    
    def similarity(self, text1, text2):
        """Calculate similarity between two texts"""
        if not self.nlp:
            return 0.0
        
        try:
            doc1 = self.nlp(text1)
            doc2 = self.nlp(text2)
            return doc1.similarity(doc2)
        except Exception as e:
            logger.error(f"Error calculating similarity: {e}")
            return 0.0
    
    def find_most_similar(self, text, candidates):
        """Find the most similar text from candidates"""
        if not self.nlp or not candidates:
            return None
        
        similarities = [(candidate, self.similarity(text, candidate)) for candidate in candidates]
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        return similarities[0] if similarities else None
