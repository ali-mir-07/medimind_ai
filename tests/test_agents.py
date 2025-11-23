"""
Automated Test Suite for MediMind AI
Tests all agents, safety features, and core functionality
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agents.orchestrator import OrchestratorAgent
from src.memory.session_manager import SessionManager
from src.agents.symptom_analyzer import SymptomAnalyzerAgent
from src.agents.medication_manager import MedicationManagerAgent
from src.agents.doctor_prep import DoctorPrepAgent

# Test counter
tests_passed = 0
tests_failed = 0

def print_test_header(test_name):
    """Print test header"""
    print(f"\n{'='*60}")
    print(f"🧪 Testing: {test_name}")
    print('='*60)

def print_result(test_name, passed, details=""):
    """Print test result"""
    global tests_passed, tests_failed
    
    if passed:
        tests_passed += 1
        print(f"✅ PASSED: {test_name}")
        if details:
            print(f"   ℹ️  {details}")
    else:
        tests_failed += 1
        print(f"❌ FAILED: {test_name}")
        if details:
            print(f"   ⚠️  {details}")

def test_orchestrator_initialization():
    """Test orchestrator agent initialization"""
    print_test_header("Orchestrator Initialization")
    
    try:
        orchestrator = OrchestratorAgent()
        
        # Check all agents initialized
        has_symptom = hasattr(orchestrator, 'symptom_agent')
        has_medication = hasattr(orchestrator, 'medication_agent')
        has_doctor_prep = hasattr(orchestrator, 'doctor_prep_agent')
        
        success = has_symptom and has_medication and has_doctor_prep
        
        print_result(
            "Orchestrator Initialization",
            success,
            f"All agents initialized: Symptom={has_symptom}, Med={has_medication}, Prep={has_doctor_prep}"
        )
        
        return orchestrator
        
    except Exception as e:
        print_result("Orchestrator Initialization", False, f"Error: {str(e)}")
        return None

def test_symptom_analysis(orchestrator):
    """Test symptom analyzer agent"""
    print_test_header("Symptom Analysis")
    
    try:
        context = {"conversation_history": []}
        result = orchestrator.process("I have a severe headache", context)
        
        # Check result structure
        has_response = "response" in result and result["response"]
        has_agent = result.get("agent") == "SymptomAnalyzer"
        not_emergency = not result.get("is_emergency", False)
        
        success = has_response and has_agent and not_emergency
        
        print_result(
            "Symptom Analysis",
            success,
            f"Response: {len(result.get('response', ''))} chars, Agent: {result.get('agent')}"
        )
        
        return success
        
    except Exception as e:
        print_result("Symptom Analysis", False, f"Error: {str(e)}")
        return False

def test_medication_interaction(orchestrator):
    """Test medication manager and interaction detection"""
    print_test_header("Medication Interaction Detection")
    
    try:
        context = {"conversation_history": []}
        result = orchestrator.process(
            "I take aspirin daily. Can I also take ibuprofen for pain?",
            context
        )
        
        # Check result
        has_response = "response" in result and result["response"]
        has_agent = result.get("agent") == "MedicationManager"
        has_meds = len(result.get("medications_mentioned", [])) >= 2
        has_interactions = len(result.get("interactions_found", [])) > 0
        
        success = has_response and has_agent and has_meds and has_interactions
        
        print_result(
            "Medication Interaction Detection",
            success,
            f"Meds found: {result.get('medications_mentioned', [])}, Interactions: {len(result.get('interactions_found', []))}"
        )
        
        return success
        
    except Exception as e:
        print_result("Medication Interaction Detection", False, f"Error: {str(e)}")
        return False

def test_doctor_prep(orchestrator):
    """Test doctor prep agent"""
    print_test_header("Doctor Visit Preparation")
    
    try:
        context = {
            "conversation_history": [],
            "symptoms_discussed": ["headache", "nausea"],
            "user_medications": ["aspirin", "ibuprofen"]
        }
        
        result = orchestrator.process(
            "Help me prepare for my doctor appointment tomorrow",
            context
        )
        
        # Check result
        has_response = "response" in result and result["response"]
        has_agent = result.get("agent") == "DoctorPrep"
        long_response = len(result.get("response", "")) > 100  # Should be detailed
        
        success = has_response and has_agent and long_response
        
        print_result(
            "Doctor Visit Preparation",
            success,
            f"Agent: {result.get('agent')}, Response length: {len(result.get('response', ''))} chars"
        )
        
        return success
        
    except Exception as e:
        print_result("Doctor Visit Preparation", False, f"Error: {str(e)}")
        return False

def test_emergency_detection(orchestrator):
    """Test emergency keyword detection"""
    print_test_header("Emergency Detection")
    
    try:
        context = {"conversation_history": []}
        
        # Test emergency phrases
        emergency_phrases = [
            "I have severe chest pain",
            "I can't breathe properly",
            "I'm having a stroke"
        ]
        
        detections = []
        for phrase in emergency_phrases:
            result = orchestrator.process(phrase, context)
            is_emergency = result.get("is_emergency", False)
            detections.append(is_emergency)
        
        success = any(detections)  # At least one should trigger
        
        print_result(
            "Emergency Detection",
            success,
            f"Detected emergencies: {sum(detections)}/{len(emergency_phrases)}"
        )
        
        return success
        
    except Exception as e:
        print_result("Emergency Detection", False, f"Error: {str(e)}")
        return False

def test_intent_classification(orchestrator):
    """Test intent classification accuracy"""
    print_test_header("Intent Classification")
    
    try:
        test_cases = [
            ("I have a headache", "symptom"),
            ("I take aspirin daily", "medication"),
            ("Help me prepare for doctor visit", "doctor_prep"),
            ("What is a healthy diet", "general")
        ]
        
        correct = 0
        for query, expected_intent in test_cases:
            context = {"conversation_history": []}
            result = orchestrator.process(query, context)
            
            # Check if routed to correct agent
            agent = result.get("agent", "").lower()
            
            if expected_intent == "symptom" and "symptom" in agent:
                correct += 1
            elif expected_intent == "medication" and "medication" in agent:
                correct += 1
            elif expected_intent == "doctor_prep" and "doctor" in agent:
                correct += 1
            elif expected_intent == "general" and "orchestrator" in agent:
                correct += 1
        
        success = correct >= 3  # At least 75% accuracy
        
        print_result(
            "Intent Classification",
            success,
            f"Correctly classified: {correct}/{len(test_cases)} queries"
        )
        
        return success
        
    except Exception as e:
        print_result("Intent Classification", False, f"Error: {str(e)}")
        return False

def test_session_management():
    """Test session manager"""
    print_test_header("Session Management")
    
    try:
        session = SessionManager()
        
        # Test adding messages
        session.add_message("user", "Hello")
        session.add_message("model", "Hi there!")
        
        # Test adding medications
        session.add_medication("aspirin")
        session.add_medication("ibuprofen")
        
        # Test adding symptoms
        session.add_symptom("headache")
        
        # Get context
        context = session.get_context()
        
        has_messages = len(context["conversation_history"]) == 2
        has_meds = len(context["user_medications"]) == 2
        has_symptoms = len(context["symptoms_discussed"]) == 1
        
        success = has_messages and has_meds and has_symptoms
        
        print_result(
            "Session Management",
            success,
            f"Messages: {len(context['conversation_history'])}, Meds: {len(context['user_medications'])}, Symptoms: {len(context['symptoms_discussed'])}"
        )
        
        return success
        
    except Exception as e:
        print_result("Session Management", False, f"Error: {str(e)}")
        return False

def run_all_tests():
    """Run complete test suite"""
    global tests_passed, tests_failed
    
    print("\n" + "🚀"*30)
    print("MEDIMIND AI - AUTOMATED TEST SUITE")
    print("🚀"*30)
    
    # Initialize orchestrator
    orchestrator = test_orchestrator_initialization()
    
    if orchestrator:
        # Run agent tests
        test_symptom_analysis(orchestrator)
        test_medication_interaction(orchestrator)
        test_doctor_prep(orchestrator)
        test_emergency_detection(orchestrator)
        test_intent_classification(orchestrator)
    
    # Run session tests
    test_session_management()
    
    # Print summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    print(f"✅ Tests Passed: {tests_passed}")
    print(f"❌ Tests Failed: {tests_failed}")
    print(f"📈 Success Rate: {(tests_passed / (tests_passed + tests_failed) * 100):.1f}%")
    print("="*60 + "\n")
    
    if tests_failed == 0:
        print("🎉 ALL TESTS PASSED! System is working perfectly!\n")
    else:
        print(f"⚠️  {tests_failed} tests need attention.\n")

if __name__ == "__main__":
    run_all_tests()