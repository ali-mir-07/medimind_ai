"""
Orchestrator Agent
Main coordinator for the multi-agent system
Routes requests to specialized agents and manages workflow
"""

from typing import Dict, Any, Optional
from src.agents.base_agent import BaseAgent
from src.agents.symptom_analyzer import SymptomAnalyzerAgent
from src.agents.medication_manager import MedicationManagerAgent
from src.agents.doctor_prep import DoctorPrepAgent
from src.utils.logger import get_logger

logger = get_logger(__name__)

class OrchestratorAgent(BaseAgent):
    """
    Main orchestrator coordinating all specialized agents
    
    Responsibilities:
    - Route user queries to appropriate agents
    - Coordinate multi-agent workflows
    - Maintain conversation context
    - Ensure safety protocols
    - Aggregate responses
    """
    
    SYSTEM_INSTRUCTION = """You are the Orchestrator Agent for MediMind AI, a personal healthcare assistant.

Your role:
1. Understand user's healthcare needs
2. Determine which specialized agent(s) should handle the request
3. Provide helpful, empathetic responses
4. Maintain conversation flow
5. Ensure medical safety

You coordinate three specialized agents:
- Symptom Analyzer: For analyzing symptoms and health concerns
- Medication Manager: For medication-related queries and interactions
- Doctor Prep: For preparing doctor visit summaries

IMPORTANT SAFETY RULES:
- Always include medical disclaimer when appropriate
- Flag emergency situations immediately
- Never diagnose medical conditions
- Always encourage professional medical consultation for serious concerns
- Be empathetic and supportive

Respond naturally and conversationally while being professional and helpful."""
    
    def __init__(self):
        """Initialize Orchestrator and all specialized agents"""
        super().__init__(
            name="Orchestrator",
            system_instruction=self.SYSTEM_INSTRUCTION
        )
        
        # Initialize specialized agents
        self.symptom_agent = SymptomAnalyzerAgent()
        self.medication_agent = MedicationManagerAgent()
        self.doctor_prep_agent = DoctorPrepAgent()
        
        logger.info("Orchestrator Agent initialized with all sub-agents")
    
    def process(self, user_input: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process user input and route to appropriate agent(s)
        
        Args:
            user_input: User's message
            context: Conversation context
            
        Returns:
            Response from appropriate agent(s)
        """
        logger.info(f"Orchestrator processing: {user_input[:50]}...")
        
        # Determine intent and route to appropriate agent
        intent = self._classify_intent(user_input)
        
        logger.info(f"Classified intent: {intent}")
        
        # Route to appropriate agent
        if intent == "symptom":
            result = self.symptom_agent.process(user_input, context)
        elif intent == "medication":
            result = self.medication_agent.process(user_input, context)
        elif intent == "doctor_prep":
            result = self.doctor_prep_agent.process(user_input, context)
        else:
            # General health query - orchestrator handles it
            result = self._handle_general_query(user_input, context)
        
        # Update context with agent information
        result["intent"] = intent
        result["orchestrator"] = self.name
        
        return result
    
    def _classify_intent(self, user_input: str) -> str:
        """
        Classify user intent to route to correct agent
        
        Args:
            user_input: User's message
            
        Returns:
            Intent category: symptom, medication, doctor_prep, or general
        """
        text_lower = user_input.lower()
        
        # Symptom-related keywords
        symptom_keywords = [
            "pain", "hurt", "ache", "feel", "sick", "symptom",
            "headache", "fever", "tired", "fatigue", "dizzy", "nausea"
        ]
        
        # Medication-related keywords
        medication_keywords = [
            "medication", "medicine", "drug", "pill", "prescription",
            "aspirin", "ibuprofen", "acetaminophen", "take", "taking",
            "dose", "dosage"
        ]
        
        # Doctor prep keywords
        doctor_keywords = [
            "doctor", "appointment", "visit", "prepare", "summary",
            "questions to ask", "see my doctor"
        ]
        
        # Count keyword matches
        symptom_score = sum(1 for kw in symptom_keywords if kw in text_lower)
        medication_score = sum(1 for kw in medication_keywords if kw in text_lower)
        doctor_score = sum(1 for kw in doctor_keywords if kw in text_lower)
        
        # Determine intent based on highest score
        scores = {
            "symptom": symptom_score,
            "medication": medication_score,
            "doctor_prep": doctor_score
        }
        
        max_score = max(scores.values())
        
        if max_score == 0:
            return "general"
        
        return max(scores, key=scores.get)
    
    def _handle_general_query(self, user_input: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle general health queries not specific to any agent
        
        Args:
            user_input: User's message
            context: Conversation context
            
        Returns:
            General health guidance response
        """
        response = self.generate_response(
            user_input,
            context.get("conversation_history", [])
        )
        
        return {
            "response": response,
            "agent": self.name,
            "type": "general"
        }
    
    def get_all_agents_info(self) -> Dict[str, Any]:
        """Get information about all agents in the system"""
        return {
            "orchestrator": self.get_info(),
            "agents": [
                self.symptom_agent.get_info(),
                self.medication_agent.get_info(),
                self.doctor_prep_agent.get_info()
            ]
        }
    