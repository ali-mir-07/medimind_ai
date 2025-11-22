"""
Memory Bank
Long-term memory storage for patient history across sessions
"""

from typing import Dict, Any, List
from src.utils.helpers import load_json, save_json, get_timestamp
from src.config import Config
from src.utils.logger import get_logger

logger = get_logger(__name__)

class MemoryBank:
    """
    Long-term memory storage
    
    Stores:
    - Patient history across sessions
    - Chronic conditions
    - Medication history
    - Symptom patterns
    """
    
    def __init__(self, user_id: str = "default_user"):
        """
        Initialize memory bank
        
        Args:
            user_id: Unique user identifier
        """
        self.user_id = user_id
        self.memory_file = Config.MEMORY_BANK_PATH
        self.memory = self._load_memory()
        logger.info(f"Memory Bank initialized for user: {user_id}")
    
    def _load_memory(self) -> Dict[str, Any]:
        """Load memory from file"""
        memory = load_json(self.memory_file)
        
        if self.user_id not in memory:
            memory[self.user_id] = {
                "medications": [],
                "chronic_conditions": [],
                "symptom_history": [],
                "doctor_visits": [],
                "created_at": get_timestamp()
            }
        
        return memory
    
    def save_session(self, session_data: Dict[str, Any]) -> None:
        """
        Save session data to long-term memory
        
        Args:
            session_data: Session data to save
        """
        user_memory = self.memory[self.user_id]
        
        # Add timestamp
        session_data["timestamp"] = get_timestamp()
        
        # Update medications
        for med in session_data.get("user_medications", []):
            if med not in user_memory["medications"]:
                user_memory["medications"].append(med)
        
        # Add symptoms to history
        for symptom in session_data.get("symptoms_discussed", []):
            user_memory["symptom_history"].append({
                "symptom": symptom,
                "timestamp": get_timestamp()
            })
        
        # Save to file
        save_json(self.memory, self.memory_file)
        logger.info("Session saved to memory bank")
    
    def get_user_history(self) -> Dict[str, Any]:
        """Get user's complete history"""
        return self.memory.get(self.user_id, {})
    
    def get_medications(self) -> List[str]:
        """Get user's medication list"""
        return self.memory.get(self.user_id, {}).get("medications", [])
    
    def get_symptom_patterns(self) -> List[Dict[str, Any]]:
        """Get historical symptom patterns"""
        return self.memory.get(self.user_id, {}).get("symptom_history", [])