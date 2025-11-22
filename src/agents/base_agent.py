"""
Base Agent class for MediMind AI
Provides common functionality for all specialized agents
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from google import genai
from src.config import Config
from src.utils.logger import get_logger

logger = get_logger(__name__)

class BaseAgent(ABC):
    """
    Abstract base class for all agents
    
    Provides common functionality:
    - Gemini client management
    - System instruction handling
    - Response generation
    - Logging and tracing
    """
    
    def __init__(self, name: str, system_instruction: str):
        """
        Initialize base agent
        
        Args:
            name: Agent name
            system_instruction: System instruction for this agent
        """
        self.name = name
        self.system_instruction = system_instruction
        self.client = genai.Client(api_key=Config.GOOGLE_API_KEY)
        
        logger.info(f"Initialized agent: {name}")
    
    def generate_response(
        self,
        prompt: str,
        context: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """
        Generate response using Gemini
        
        Args:
            prompt: User prompt
            context: Optional conversation context
            
        Returns:
            Generated response text
        """
        try:
            logger.debug(f"{self.name} generating response for: {prompt[:50]}...")
            
            # Prepare messages
            messages = context or []
            messages.append({
                "role": "user",
                "parts": [{"text": prompt}]
            })
            
            # Generate response
            response = self.client.models.generate_content(
                model=Config.GEMINI_MODEL,
                contents=messages,
                config=genai.types.GenerateContentConfig(
                    system_instruction=self.system_instruction,
                    temperature=Config.TEMPERATURE,
                    top_p=Config.TOP_P,
                )
            )
            
            result = response.text
            logger.debug(f"{self.name} generated response: {result[:100]}...")
            
            return result
            
        except Exception as e:
            logger.error(f"{self.name} error generating response: {str(e)}")
            return f"I apologize, but I encountered an error. Please try again."
    
    @abstractmethod
    def process(self, user_input: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process user input and return agent-specific response
        
        Args:
            user_input: User's message
            context: Conversation context and state
            
        Returns:
            Dict containing response and updated context
        """
        pass
    
    def get_info(self) -> Dict[str, str]:
        """
        Get agent information
        
        Returns:
            Dict with agent name and description
        """
        return {
            "name": self.name,
            "instruction": self.system_instruction[:100] + "..."
        }