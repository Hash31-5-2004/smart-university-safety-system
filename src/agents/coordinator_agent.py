from crewai import Agent, Task, Crew
from crewai.tools import BaseTool
from .cv_agent import ComputerVisionAgent
from .rag_agent import RAGAgent
from .alert_agent import AlertAgent
import json
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

class ProcessIncidentTool(BaseTool):
    name: str = "Process Complete Incident"
    description: str = "Process a complete safety incident from image input to final alert."

    def _run(self, image_path: str, location: str) -> dict:
        try:
            # Create agents
            cv_agent = ComputerVisionAgent().create_agent()
            rag_agent = RAGAgent().create_agent()
            alert_agent = AlertAgent().create_agent()

            # Create crew
            crew = Crew(
                agents=[cv_agent, rag_agent, alert_agent],
                tasks=self._create_incident_tasks(image_path, location, cv_agent, rag_agent, alert_agent),
                verbose=True
            )

            # Execute the crew
            result = crew.kickoff()

            return {
                "status": "success",
                "result": str(result),
                "workflow": "CV Analysis → RAG Recommendations → Alert Formatting"
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

    def _create_incident_tasks(self, image_path: str, location: str, cv_agent, rag_agent, alert_agent):
        """Create the task sequence for incident processing."""
        # Task 1: CV Analysis
        cv_task = Task(
            description=f"Analyze the image at {image_path} captured at {location} for safety anomalies",
            agent=cv_agent,
            expected_output="Detailed analysis of any detected anomalies with confidence scores"
        )

        # Task 2: RAG Recommendations (depends on CV results)
        rag_task = Task(
            description="Based on the CV analysis, retrieve relevant safety protocols and generate recommendations",
            agent=rag_agent,
            context=[cv_task],
            expected_output="Evidence-based safety recommendations from knowledge base"
        )

        # Task 3: Alert Formatting (depends on both previous tasks)
        alert_task = Task(
            description="Format a comprehensive safety alert combining CV analysis and recommendations",
            agent=alert_agent,
            context=[cv_task, rag_task],
            expected_output="Prioritized, formatted safety alert ready for distribution"
        )

        return [cv_task, rag_task, alert_task]

class CoordinatorAgent:
    def __init__(self):
        self.cv_agent = ComputerVisionAgent().create_agent()
        self.rag_agent = RAGAgent().create_agent()
        self.alert_agent = AlertAgent().create_agent()

    def create_agent(self):
        return Agent(
            role="Safety Operations Coordinator",
            goal="Orchestrate multi-agent safety incident response and ensure proper workflow execution",
            backstory="""You are the central coordinator for campus safety operations. You manage the
            entire incident response workflow, delegating tasks to specialized agents and ensuring
            comprehensive, timely safety responses.""",
            tools=[ProcessIncidentTool()],
            llm="groq/llama-3.3-70b-versatile",
            verbose=True,
            allow_delegation=True
        )

    def create_crew(self, image_path: str, location: str):
        """Create and return a crew for processing a specific incident."""
        return Crew(
            agents=[self.cv_agent, self.rag_agent, self.alert_agent],
            tasks=ProcessIncidentTool()._create_incident_tasks(image_path, location, self.cv_agent, self.rag_agent, self.alert_agent),
            verbose=True
        )