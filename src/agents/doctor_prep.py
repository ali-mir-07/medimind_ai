"""
Doctor Prep Agent
Specialized agent for preparing doctor visit summaries and questions
"""

from typing import Dict, Any, List
from src.agents.base_agent import BaseAgent
from src.utils.helpers import get_timestamp
from src.utils.logger import get_logger

logger = get_logger(__name__)

class DoctorPrepAgent(BaseAgent):
    """
    Agent specialized in doctor visit preparation
    
    Responsibilities:
    - Summarize conversation history
    - Generate relevant questions for doctor
    - Create symptom timeline
    - Compile medication list
    - Organize health information
    """
    
    SYSTEM_INSTRUCTION = """You are a Doctor Prep Agent, part of the MediMind AI healthcare system.

Your role:
1. Help users prepare for doctor appointments
2. Summarize symptoms and health concerns discussed
3. Generate relevant questions to ask the doctor
4. Create organized timelines of symptoms
5. Compile medication lists

When preparing for doctor visits:
- Review conversation history for key symptoms
- Identify patterns or progressions
- Suggest specific questions based on symptoms
- Organize information in clear, concise format
- Encourage users to bring notes to appointment

Format your summaries with:
**Symptoms Summary:**
- List of symptoms with duration and severity

**Medications:**
- Current medications and dosages

**Questions to Ask Doctor:**
- Numbered list of relevant questions

**Timeline:**
- Chronological progression of symptoms

Be thorough but concise. Focus on medically relevant information."""
    
    def __init__(self):
        """Initialize Doctor Prep Agent"""
        super().__init__(
            name="DoctorPrep",
            system_instruction=self.SYSTEM_INSTRUCTION
        )
        logger.info("Doctor Prep Agent initialized")
    
    def process(self, user_input: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process doctor preparation request
        
        Args:
            user_input: User's request for doctor prep
            context: Conversation context with history
            
        Returns:
            Formatted doctor visit preparation
        """
        logger.info("Processing doctor prep request")
        
        # Extract key information from context
        summary = self._extract_summary(context)
        
        # Build enhanced prompt
        enhanced_prompt = self._build_prompt(user_input, summary)
        
        # Generate response
        response = self.generate_response(
            enhanced_prompt,
            context.get("conversation_history", [])
        )
        
        return {
            "response": response,
            "agent": self.name,
            "summary": summary
        }
    
    def _extract_summary(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Extract key information from conversation context"""
        
        summary = {
            "symptoms": context.get("symptoms_discussed", []),
            "medications": context.get("user_medications", []),
            "concerns": context.get("health_concerns", []),
            "duration": context.get("conversation_duration", "recent conversation")
        }
        
        return summary
    
    def _build_prompt(self, user_input: str, summary: Dict[str, Any]) -> str:
        """Build enhanced prompt for doctor prep"""
        
        prompt = f"User request: {user_input}\n\n"
        prompt += "Based on our conversation:\n\n"
        
        if summary["symptoms"]:
            prompt += f"Symptoms discussed: {', '.join(summary['symptoms'])}\n"
        
        if summary["medications"]:
            prompt += f"Medications mentioned: {', '.join(summary['medications'])}\n"
        
        if summary["concerns"]:
            prompt += f"Health concerns: {', '.join(summary['concerns'])}\n"
        
        prompt += "\nPlease create a comprehensive doctor visit preparation summary."
        
        return prompt