"""
Performance Metrics Tracking for MediMind AI
Tracks agent performance, response times, and usage statistics
"""

import time
from typing import Dict, Any, List
from datetime import datetime
from src.utils.logger import get_logger

logger = get_logger(__name__)

class MetricsTracker:
    """
    Track performance metrics for agents and system
    
    Monitors:
    - Request counts per agent
    - Response times
    - Emergency detections
    - Drug interaction checks
    - Error rates
    """
    
    def __init__(self):
        """Initialize metrics tracker with empty metrics"""
        self.metrics = {
            "total_requests": 0,
            "agent_calls": {
                "orchestrator": 0,
                "symptom_analyzer": 0,
                "medication_manager": 0,
                "doctor_prep": 0
            },
            "response_times": [],
            "errors": 0,
            "emergency_detections": 0,
            "interactions_checked": 0,
            "session_start": datetime.now()
        }
        logger.info("MetricsTracker initialized")
    
    def track_request(self, agent_name: str, response_time: float):
        """
        Track a request to an agent
        
        Args:
            agent_name: Name of the agent that handled request
            response_time: Response time in seconds
        """
        self.metrics["total_requests"] += 1
        
        # Normalize agent name
        agent_key = agent_name.lower().replace(" ", "_")
        
        if agent_key in self.metrics["agent_calls"]:
            self.metrics["agent_calls"][agent_key] += 1
        
        self.metrics["response_times"].append(response_time)
        
        logger.info(f"Request tracked: {agent_name} - {response_time:.2f}s")
    
    def track_error(self, error_type: str = "unknown"):
        """
        Track an error occurrence
        
        Args:
            error_type: Type of error that occurred
        """
        self.metrics["errors"] += 1
        logger.warning(f"Error tracked: {error_type}")
    
    def track_emergency(self):
        """Track emergency keyword detection"""
        self.metrics["emergency_detections"] += 1
        logger.warning("🚨 Emergency detection tracked")
    
    def track_interaction_check(self):
        """Track medication interaction check performed"""
        self.metrics["interactions_checked"] += 1
        logger.info("💊 Drug interaction check tracked")
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get comprehensive metrics summary
        
        Returns:
            Dictionary with all metrics and calculated statistics
        """
        # Calculate average response time
        avg_response_time = (
            sum(self.metrics["response_times"]) / len(self.metrics["response_times"])
            if self.metrics["response_times"] else 0
        )
        
        # Calculate session duration
        session_duration = datetime.now() - self.metrics["session_start"]
        
        return {
            "total_requests": self.metrics["total_requests"],
            "agent_calls": self.metrics["agent_calls"],
            "average_response_time": round(avg_response_time, 2),
            "min_response_time": round(min(self.metrics["response_times"]), 2) if self.metrics["response_times"] else 0,
            "max_response_time": round(max(self.metrics["response_times"]), 2) if self.metrics["response_times"] else 0,
            "errors": self.metrics["errors"],
            "emergency_detections": self.metrics["emergency_detections"],
            "interactions_checked": self.metrics["interactions_checked"],
            "session_duration": str(session_duration).split('.')[0],  # Remove microseconds
            "success_rate": round((1 - (self.metrics["errors"] / max(self.metrics["total_requests"], 1))) * 100, 1)
        }
    
    def print_summary(self):
        """Print beautiful metrics summary to console"""
        summary = self.get_summary()
        
        print("\n" + "="*60)
        print("📊 MEDIMIND AI - SESSION METRICS & PERFORMANCE")
        print("="*60)
        
        print(f"\n⏱️  Session Duration: {summary['session_duration']}")
        print(f"📈 Total Requests: {summary['total_requests']}")
        print(f"✅ Success Rate: {summary['success_rate']}%")
        
        print(f"\n⚡ Performance:")
        print(f"  • Average Response Time: {summary['average_response_time']}s")
        print(f"  • Fastest Response: {summary['min_response_time']}s")
        print(f"  • Slowest Response: {summary['max_response_time']}s")
        
        print(f"\n🤖 Agent Activity:")
        for agent, calls in summary['agent_calls'].items():
            agent_name = agent.replace('_', ' ').title()
            percentage = (calls / max(summary['total_requests'], 1)) * 100
            print(f"  • {agent_name}: {calls} calls ({percentage:.1f}%)")
        
        print(f"\n🛡️  Safety Metrics:")
        print(f"  • Emergency Detections: {summary['emergency_detections']}")
        print(f"  • Drug Interaction Checks: {summary['interactions_checked']}")
        print(f"  • Errors: {summary['errors']}")
        
        print("="*60 + "\n")
        
        logger.info("Metrics summary displayed")

# Global metrics tracker instance
metrics_tracker = MetricsTracker()