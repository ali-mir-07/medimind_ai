"""
Medication Manager Agent
Specialized agent for medication management and interaction checking
"""

from typing import Dict, Any, List
from src.agents.base_agent import BaseAgent
from src.utils.helpers import load_json
from src.config import Config
from src.utils.logger import get_logger

logger = get_logger(__name__)

class MedicationManagerAgent(BaseAgent):
    """
    Agent specialized in medication management
    
    Responsibilities:
    - Track current medications
    - Check for drug interactions
    - Provide dosage information
    - Schedule reminders
    - Flag safety concerns
    """
    
    SYSTEM_INSTRUCTION = """You are a Medication Manager Agent, part of the MediMind AI healthcare system.

Your role:
1. Help users track their medications
2. Check for potential drug interactions
3. Provide general information about medications (not medical advice)
4. Remind users about medication schedules
5. Flag potential safety concerns

When discussing medications:
- Ask about current medications being taken
- Inquire about dosage and frequency
- Check for potential interactions
- Provide general safety information
- Always emphasize consulting healthcare providers

IMPORTANT:
- Never recommend specific medications
- Never suggest changing prescribed dosages
- Always encourage consulting with doctors/pharmacists
- Flag serious interactions immediately
- Be clear this is informational, not medical advice

Format responses with:
- Clear acknowledgment of medications mentioned
- Potential interactions or concerns
- Safety information
- Recommendation to consult healthcare provider"""
    
    def __init__(self):
        """Initialize Medication Manager Agent"""
        super().__init__(
            name="MedicationManager",
            system_instruction=self.SYSTEM_INSTRUCTION
        )
        
        # Load medication databases
        self.medications_db = load_json(Config.MEDICATIONS_DB)
        self.interactions_db = load_json(Config.INTERACTIONS_DB)
        logger.info("Medication Manager Agent initialized")
    
    def process(self, user_input: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process medication-related queries
        
        Args:
            user_input: User's medication query
            context: Conversation context
            
        Returns:
            Response with medication information and warnings
        """
        logger.info(f"Processing medication query: {user_input[:50]}...")
        
        # Extract mentioned medications
        mentioned_meds = self._extract_medications(user_input)
        
        # Check for interactions
        interactions = self._check_interactions(mentioned_meds, context)
        
        # Build enhanced prompt
        enhanced_prompt = self._build_prompt(user_input, mentioned_meds, interactions)
        
        # Generate response
        response = self.generate_response(
            enhanced_prompt,
            context.get("conversation_history", [])
        )
        
        return {
            "response": response,
            "agent": self.name,
            "medications_mentioned": mentioned_meds,
            "interactions_found": interactions
        }
    
    def _extract_medications(self, text: str) -> List[str]:
        """Extract medication names from text"""
        medications = []
        text_lower = text.lower()
        
        # Check against known medications
        for med in self.medications_db.get("common_medications", []):
            if med["name"].lower() in text_lower:
                medications.append(med["name"])
        
        return medications
    
    def _check_interactions(
        self,
        medications: List[str],
        context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Check for drug interactions"""
        interactions = []
        
        # Get medications from context (previously mentioned)
        context_meds = context.get("user_medications", [])
        all_meds = list(set(medications + context_meds))
        
        # Check each pair
        for i, med1 in enumerate(all_meds):
            for med2 in all_meds[i+1:]:
                interaction = self._find_interaction(med1, med2)
                if interaction:
                    interactions.append(interaction)
        
        return interactions
    
    def _find_interaction(self, drug1: str, drug2: str) -> Dict[str, Any]:
        """Find interaction between two drugs"""
        for interaction in self.interactions_db.get("drug_interactions", []):
            if (interaction["drug1"].lower() == drug1.lower() and 
                interaction["drug2"].lower() == drug2.lower()) or \
               (interaction["drug2"].lower() == drug1.lower() and 
                interaction["drug1"].lower() == drug2.lower()):
                return interaction
        return None
    
    def _build_prompt(
        self,
        user_input: str,
        medications: List[str],
        interactions: List[Dict[str, Any]]
    ) -> str:
        """Build enhanced prompt with medication context"""
        
        prompt = f"User medication query: {user_input}\n\n"
        
        if medications:
            prompt += f"Medications mentioned: {', '.join(medications)}\n\n"
        
        if interactions:
            prompt += "⚠️ POTENTIAL INTERACTIONS FOUND:\n"
            for interaction in interactions:
                prompt += f"- {interaction['drug1']} + {interaction['drug2']}: "
                prompt += f"{interaction['severity'].upper()} - {interaction['description']}\n"
                prompt += f"  Recommendation: {interaction['recommendation']}\n\n"
        
        prompt += "Please respond with this interaction information and emphasize consulting healthcare providers."
        
        return prompt