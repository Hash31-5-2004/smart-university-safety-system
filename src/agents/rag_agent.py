from crewai import Agent
from crewai.tools import BaseTool
from src.rag.rag_pipeline import UniversitySafetyRAG
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

class GetSafetyRecommendationsTool(BaseTool):
    name: str = "Get Safety Recommendations"
    description: str = "Retrieve safety recommendations from the knowledge base based on incident description."

    def _run(self, incident_description: str) -> dict:
        rag_system = UniversitySafetyRAG()
        try:
            # Get recommendations from RAG system
            result = rag_system.get_safety_recommendation(incident_description)

            return {
                "status": "success",
                "incident": incident_description,
                "recommendations": result.get("result", ""),
                "source": "RAG Knowledge Base (NIST + Campus Protocols)"
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "incident": incident_description
            }

class RAGAgent:
    def __init__(self):
        self.rag_system = UniversitySafetyRAG()

    def create_agent(self):
        return Agent(
            role="Safety Knowledge Specialist",
            goal="Retrieve relevant safety protocols and generate evidence-based recommendations",
            backstory="""You are a safety protocol expert with access to comprehensive knowledge bases
            including NIST security standards, campus safety procedures, and emergency response guidelines.
            You provide authoritative, actionable recommendations based on incident analysis.""",
            tools=[GetSafetyRecommendationsTool()],
            llm="groq/llama-3.3-70b-versatile",
            verbose=True,
            allow_delegation=False
        )