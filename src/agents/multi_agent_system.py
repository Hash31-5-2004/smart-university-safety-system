from crewai import Crew, Task
from .coordinator_agent import CoordinatorAgent
import os
from datetime import datetime

class MultiAgentSafetySystem:
    """
    Multi-agent system for campus safety incident response using CrewAI.
    Implements the instructor requirement for multi-agent architecture.
    """

    def __init__(self):
        self.coordinator = CoordinatorAgent()
        self.coordinator_agent = self.coordinator.create_agent()

    def process_incident(self, image_path: str, location: str) -> dict:
        """
        Process a safety incident using the multi-agent system.

        Args:
            image_path: Path to the incident image
            location: Location where incident occurred

        Returns:
            Complete processing results
        """
        try:
            print(f"🚀 Starting multi-agent incident processing at {location}")

            # Create crew for this specific incident
            crew = self.coordinator.create_crew(image_path, location)

            # Execute the crew
            result = crew.kickoff()

            print("✅ Multi-agent processing completed")

            return {
                "status": "success",
                "timestamp": datetime.now().isoformat(),
                "location": location,
                "result": str(result),
                "agents_used": ["CV Agent", "RAG Agent", "Alert Agent"]
            }

        except Exception as e:
            print(f"❌ Multi-agent processing failed: {e}")
            return {
                "status": "error",
                "error": str(e),
                "location": location
            }

    def get_system_status(self) -> dict:
        """Get the current status of the multi-agent system."""
        return {
            "system": "Multi-Agent Campus Safety System",
            "framework": "CrewAI",
            "agents": [
                "Computer Vision Agent (Anomaly Detection)",
                "RAG Agent (Knowledge Retrieval)",
                "Alert Agent (Response Coordination)",
                "Coordinator Agent (Workflow Management)"
            ],
            "knowledge_base": "NIST Standards + Campus Protocols",
            "status": "operational"
        }

# Test function
if __name__ == "__main__":
    print("🧪 Testing Multi-Agent Safety System")

    system = MultiAgentSafetySystem()
    print("System Status:", system.get_system_status())

    # Test with a sample image if available
    test_image = "test_image.png"
    if os.path.exists(test_image):
        result = system.process_incident(test_image, "Building A entrance")
        print("Test Result:", result)
    else:
        print("No test image found. Create test_image.png to run full test.")