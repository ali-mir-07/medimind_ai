"""
Session Manager
Handles conversation sessions and short-term memory
"""

from typing import Dict, Any, List, Optional
from src.utils.logger import get_logger
from src.config import Config

logger = get_logger(__name__)

class SessionManager:
    """
    Manages conversation sessions and context
    
    Handles:
    - Conversation history
    - User state tracking
    - Context management
    - Session persistence
    """
    
    def __init__(self):
        """Initialize session manager"""
        self.current_session = {
            "conversation_history": [],
            "user_medications": [],
            "symptoms_discussed": [],
            "health_concerns": [],
            "session_metadata": {}
        }
        logger.info("Session Manager initialized")
    
    def add_message(self, role: str, content: str) -> None:
        """
        Add message to conversation history
        
        Args:
            role: Message role (user or model)
            content: Message content
        """
        message = {
            "role": role,
            "parts": [{"text": content}]
        }
        
        self.current_session["conversation_history"].append(message)
        
        # Trim history if too long
        if len(self.current_session["conversation_history"]) > Config.MAX_CONVERSATION_HISTORY:
            self._compact_history()
        
        logger.debug(f"Added {role} message to history")
    
    def add_medication(self, medication: str) -> None:
        """Add medication to user's medication list"""
        if medication not in self.current_session["user_medications"]:
            self.current_session["user_medications"].append(medication)
            logger.info(f"Added medication: {medication}")
    
    def add_symptom(self, symptom: str) -> None:
        """Add symptom to discussed symptoms"""
        if symptom not in self.current_session["symptoms_discussed"]:
            self.current_session["symptoms_discussed"].append(symptom)
            logger.info(f"Added symptom: {symptom}")
    
    def get_context(self) -> Dict[str, Any]:
        """Get current session context"""
        return self.current_session.copy()
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get conversation history"""
        return self.current_session["conversation_history"]
    
    def _compact_history(self) -> None:
        """
        Compact conversation history using context compaction
        Keep only recent messages
        """
        history = self.current_session["conversation_history"]
        
        # Keep last N messages
        keep_count = Config.MAX_CONVERSATION_HISTORY - 5
        
        self.current_session["conversation_history"] = history[-keep_count:]
        
        logger.info(f"Compacted history to {keep_count} messages")
    
    def clear_session(self) -> None:
        """Clear current session"""
        self.current_session = {
            "conversation_history": [],
            "user_medications": [],
            "symptoms_discussed": [],
            "health_concerns": [],
            "session_metadata": {}
        }
        logger.info("Session cleared")