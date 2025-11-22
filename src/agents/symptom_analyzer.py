"""
Symptom Analyzer Agent
Specialized agent for analyzing health symptoms and asking clarifying questions
"""

from typing import Dict, Any, List
from src.agents.base_agent import BaseAgent
from src.utils.helpers import load_json
from src.config import Config
from src.utils.logger import get_logger

logger = get_logger(__name__)

class SymptomAnalyzerAgent(BaseAgent):
    """
    Agent specialized in symptom analysis
    
    Responsibilities:
    - Ask clarifying questions about symptoms
    - Identify symptom patterns
    - Flag potential emergency situations
    - Track symptom history
    """
    
    SYSTEM_INSTRUCTION = """You are a Symptom Analyzer Agent, part of the MediMind AI healthcare system.

Your role:
1. Analyze user's symptoms with empathy and professionalism
2. Ask specific clarifying questions about:
   - Severity (1-10 scale)
   - Location and type of pain/discomfort
   - Duration and onset
   - Associated symptoms
   - Triggers or relieving factors

3. Identify potential red flags that require immediate medical attention
4. Track symptom patterns over time

IMPORTANT:
- Always be empathetic and non-judgmental
- Ask ONE question at a time for clarity
- Flag emergencies immediately
- Never diagnose - only gather and analyze information
- Always encourage professional medical consultation for concerning symptoms

Format your response clearly with:
- Acknowledgment of the symptom
- Specific questions (numbered)
- Any red flags or concerns
- Reminder about professional consultation when needed"""
    
    def __init__(self):
        """Initialize Symptom Analyzer Agent"""
        super().__init__(
            name="SymptomAnalyzer",
            system_instruction=self.SYSTEM_INSTRUCTION
        )
        
        # Load symptom database
        self.symptoms_db = load_json(Config.SYMPTOMS_DB)
        logger.info("Symptom Analyzer Agent initialized")
    
    def process(self, user_input: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process symptom-related queries
        
        Args:
            user_input: User's symptom description
            context: Conversation context
            
        Returns:
            Response with symptom analysis and questions
        """
        logger.info(f"Processing symptom query: {user_input[:50]}...")
        
        # Check for emergency keywords
        if self._detect_emergency(user_input):
            return {
                "response": self._generate_emergency_response(),
                "agent": self.name,
                "is_emergency": True
            }
        
        # Get relevant symptom questions
        questions = self._get_relevant_questions(user_input)
        
        # Build enhanced prompt
        enhanced_prompt = self._build_prompt(user_input, questions, context)
        
        # Generate response
        response = self.generate_response(
            enhanced_prompt,
            context.get("conversation_history", [])
        )
        
        return {
            "response": response,
            "agent": self.name,
            "symptom_questions": questions,
            "is_emergency": False
        }
    
    def _detect_emergency(self, text: str) -> bool:
        """Detect emergency keywords in text"""
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in Config.EMERGENCY_KEYWORDS)
    
    def _generate_emergency_response(self) -> str:
        """Generate emergency response"""
        return """🚨 EMERGENCY ALERT 🚨

Based on your symptoms, this may require IMMEDIATE medical attention.

PLEASE:
1. Call emergency services (911) immediately
2. Or go to the nearest emergency room
3. Do not wait or try to treat this at home

This is not something that can be safely managed through this app.

Your safety is the priority. Please seek emergency medical care now."""
    
    def _get_relevant_questions(self, user_input: str) -> List[str]:
        """Get relevant symptom questions from database"""
        questions = []
        
        common_symptoms = self.symptoms_db.get("common_symptoms", [])
        
        for symptom in common_symptoms:
            if symptom["name"].lower() in user_input.lower():
                questions.extend(symptom.get("questions", []))
                break
        
        return questions[:5]  # Limit to 5 questions
    
    def _build_prompt(
        self,
        user_input: str,
        questions: List[str],
        context: Dict[str, Any]
    ) -> str:
        """Build enhanced prompt with context"""
        
        prompt = f"User symptom report: {user_input}\n\n"
        
        if questions:
            prompt += "Relevant questions to consider asking:\n"
            for i, q in enumerate(questions, 1):
                prompt += f"{i}. {q}\n"
            prompt += "\n"
        
        prompt += "Please respond with empathy and ask 2-3 of the most relevant questions."
        
        return prompt