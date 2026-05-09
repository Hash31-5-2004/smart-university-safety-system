from crewai import Agent
from crewai.tools import BaseTool
from src.cv_detection.anomaly_detector import CampusAnomalyDetector
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

class AnalyzeImageTool(BaseTool):
    name: str = "Analyze Image for Anomalies"
    description: str = "Analyze an image for safety anomalies using computer vision models."

    def _run(self, image_path: str, location: str) -> dict:
        cv_detector = CampusAnomalyDetector(data_root="data/raw/ucsd")
        try:
            # Process the image
            result = cv_detector.process_image_and_generate_event(
                image_path=image_path,
                location=location
            )

            return {
                "status": "success",
                "location": location,
                "caption": result.get("caption", "No caption generated"),
                "event": result.get("event", "Unknown event"),
                "confidence": result.get("confidence", 0.0),
                "analysis": f"Detected: {result.get('event', 'Unknown')} at {location} with confidence {result.get('confidence', 0.0):.2f}"
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "location": location
            }

class ComputerVisionAgent:
    def __init__(self):
        self.cv_detector = CampusAnomalyDetector(data_root="data/raw/ucsd")

    def create_agent(self):
        return Agent(
            role="Computer Vision Specialist",
            goal="Analyze images and videos for safety anomalies and generate detailed descriptions",
            backstory="""You are an expert computer vision analyst specializing in campus safety.
            You use advanced AI models (BLIP and CLIP) to detect anomalies in surveillance footage
            and generate accurate, detailed descriptions of incidents.""",
            tools=[AnalyzeImageTool()],
            llm="groq/llama-3.3-70b-versatile",
            verbose=True,
            allow_delegation=False
        )