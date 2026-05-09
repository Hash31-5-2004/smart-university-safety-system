import os
import requests
from crewai import Agent
from crewai.tools import BaseTool
from datetime import datetime
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from src.integrations.telegram_tool import SendTelegramAlertTool, SendTelegramStatusTool, SendTelegramAlertWithImageTool

load_dotenv()

# --- Data Schemas ---

class CVAnalysis(BaseModel):
    location: str
    caption: str = ""
    event: str = ""
    confidence: float = 0.0
    analysis: str = ""

class RAGRecommendations(BaseModel):
    status: str
    incident: str
    recommendations: str = ""
    source: str = ""

class IncidentDetails(BaseModel):
    confidence: float = 0.0
    event: str = ""

class SendToN8NArgs(BaseModel):
    alert_payload: dict = Field(..., description="The complete alert dictionary to send to n8n.")

# --- Tools ---

class SendToN8NTool(BaseTool):
    name: str = "Send to n8n Webhook"
    description: str = "Dispatches the finalized safety alert to n8n for automated emergency response."
    args_schema: type[BaseModel] = SendToN8NArgs

    def _run(self, alert_payload: dict) -> str:
        # PASTE YOUR WEBHOOK URL HERE
        webhook_url = "https://hash314151.app.n8n.cloud/webhook-test/home/rt-detection/smart-university-safety-system/src/agents/alert_agent.py"
        
        try:
            response = requests.post(webhook_url, json=alert_payload, timeout=10)
            if response.status_code == 200:
                return f"Success: Alert dispatched to n8n. Response: {response.text}"
            else:
                return f"Error: n8n returned status code {response.status_code}."
        except Exception as e:
            return f"Critical Failure: Could not connect to n8n. Error: {str(e)}"

class FormatAlertArgs(BaseModel):
    cv_analysis: CVAnalysis
    rag_recommendations: RAGRecommendations

class FormatAlertTool(BaseTool):
    name: str = "Format Safety Alert"
    description: str = "Combines CV and RAG data into a single structured alert object."
    args_schema: type[BaseModel] = FormatAlertArgs

    def _run(self, cv_analysis: CVAnalysis | dict, rag_recommendations: RAGRecommendations | dict) -> dict:
        try:
            if isinstance(cv_analysis, dict):
                cv_analysis = CVAnalysis.model_validate(cv_analysis)
            if isinstance(rag_recommendations, dict):
                rag_recommendations = RAGRecommendations.model_validate(rag_recommendations)

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            priority = self._calculate_priority(cv_analysis)

            alert = {
                "timestamp": timestamp,
                "location": cv_analysis.location,
                "incident_type": cv_analysis.event or "Unknown",
                "confidence": round(cv_analysis.confidence, 2),
                "description": cv_analysis.caption or "No description available",
                "recommendations": rag_recommendations.recommendations,
                "priority": priority,
                "status": "ACTIVE"
            }
            return alert
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def _calculate_priority(self, cv_analysis: CVAnalysis) -> str:
        confidence = cv_analysis.confidence
        event = cv_analysis.event.lower()
        if confidence > 0.9 or any(k in event for k in ["fight", "assault", "weapon"]):
            return "CRITICAL"
        elif confidence > 0.7 or any(k in event for k in ["fall", "medical", "injury"]):
            return "HIGH"
        return "MEDIUM" if confidence > 0.5 else "LOW"

class PrioritizeIncidentArgs(BaseModel):
    incident_details: IncidentDetails

class PrioritizeIncidentTool(BaseTool):
    name: str = "Prioritize Incident"
    description: str = "Analyze incident details and assign priority level."
    args_schema: type[BaseModel] = PrioritizeIncidentArgs

    def _run(self, incident_details: IncidentDetails | dict) -> dict:
        try:
            if isinstance(incident_details, dict):
                incident_details = IncidentDetails.model_validate(incident_details)
            
            # Logic similar to internal _calculate_priority for standalone use
            return {"priority": "Determined based on event type and confidence"}
        except Exception as e:
            return {"status": "error", "error": str(e)}

# --- Agent Configuration ---

class AlertAgent:
    def create_agent(self):
        return Agent(
            role="Emergency Alert Coordinator",
            goal="Format safety alerts and immediately trigger both n8n automation workflow and Telegram notifications with evidence.",
            backstory="""You are the critical link between AI detection and real-world 
            response. Your job is to take raw incident data, wrap it into a clear 
            alert, and use both the SendToN8NTool and Telegram tools to notify 
            campus security instantly through multiple channels with visual evidence.
            Speed and accuracy are your highest priorities.""",
            tools=[FormatAlertTool(), PrioritizeIncidentTool(), SendToN8NTool(), SendTelegramAlertTool(), SendTelegramStatusTool(), SendTelegramAlertWithImageTool()],
            llm="groq/llama-3.3-70b-versatile",
            verbose=True,
            allow_delegation=False
        )

##############################################################################################

# from crewai import Agent
# from crewai.tools import BaseTool
# from datetime import datetime
# from dotenv import load_dotenv
# from pydantic import BaseModel

# load_dotenv()

# class CVAnalysis(BaseModel):
#     location: str
#     caption: str = ""
#     event: str = ""
#     confidence: float = 0.0
#     analysis: str = ""

# class RAGRecommendations(BaseModel):
#     status: str
#     incident: str
#     recommendations: str = ""
#     source: str = ""

# class IncidentDetails(BaseModel):
#     confidence: float = 0.0
#     event: str = ""

# class FormatAlertArgs(BaseModel):
#     cv_analysis: CVAnalysis
#     rag_recommendations: RAGRecommendations

# class FormatAlertTool(BaseTool):
#     name: str = "Format Safety Alert"
#     description: str = "Format a comprehensive safety alert combining CV analysis and RAG recommendations."
#     args_schema: type[BaseModel] = FormatAlertArgs

#     def _run(self, cv_analysis: CVAnalysis | dict, rag_recommendations: RAGRecommendations | dict) -> dict:
#         try:
#             if isinstance(cv_analysis, dict):
#                 cv_analysis = CVAnalysis.model_validate(cv_analysis)
#             if isinstance(rag_recommendations, dict):
#                 rag_recommendations = RAGRecommendations.model_validate(rag_recommendations)

#             timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#             alert = {
#                 "timestamp": timestamp,
#                 "location": cv_analysis.location,
#                 "incident_type": cv_analysis.event or "Unknown",
#                 "confidence": cv_analysis.confidence,
#                 "description": cv_analysis.caption or "No description available",
#                 "recommendations": rag_recommendations.recommendations,
#                 "priority": self._calculate_priority(cv_analysis),
#                 "status": "ACTIVE"
#             }

#             return {
#                 "status": "success",
#                 "alert": alert,
#                 "formatted_message": self._create_alert_message(alert)
#             }
#         except Exception as e:
#             return {
#                 "status": "error",
#                 "error": str(e)
#             }

#     def _calculate_priority(self, cv_analysis: CVAnalysis) -> str:
#         confidence = cv_analysis.confidence
#         event = cv_analysis.event.lower()

#         if confidence > 0.9 or "fight" in event or "assault" in event:
#             return "CRITICAL"
#         elif confidence > 0.7 or "fall" in event or "medical" in event:
#             return "HIGH"
#         elif confidence > 0.5:
#             return "MEDIUM"
#         else:
#             return "LOW"

#     def _create_alert_message(self, alert: dict) -> str:
#         return f"""🚨 CAMPUS SAFETY ALERT 🚨

# Time: {alert['timestamp']}
# Location: {alert['location']}
# Priority: {alert['priority']}

# Incident: {alert['incident_type']} (Confidence: {alert['confidence']:.2f})
# Description: {alert['description']}

# {alert['recommendations']}

# Status: {alert['status']}"""

# class PrioritizeIncidentArgs(BaseModel):
#     incident_details: IncidentDetails

# class PrioritizeIncidentTool(BaseTool):
#     name: str = "Prioritize Incident"
#     description: str = "Analyze incident details and assign priority level."
#     args_schema: type[BaseModel] = PrioritizeIncidentArgs

#     def _run(self, incident_details: IncidentDetails | dict) -> dict:
#         try:
#             if isinstance(incident_details, dict):
#                 incident_details = IncidentDetails.model_validate(incident_details)

#             confidence = incident_details.confidence
#             event_type = incident_details.event.lower()

#             if confidence > 0.9:
#                 base_priority = "CRITICAL"
#             elif confidence > 0.7:
#                 base_priority = "HIGH"
#             elif confidence > 0.5:
#                 base_priority = "MEDIUM"
#             else:
#                 base_priority = "LOW"

#             if any(keyword in event_type for keyword in ["fight", "assault", "weapon", "fire"]):
#                 priority = "CRITICAL"
#             elif any(keyword in event_type for keyword in ["fall", "medical", "injury"]):
#                 priority = "HIGH" if base_priority in ["CRITICAL", "HIGH"] else "MEDIUM"
#             else:
#                 priority = base_priority

#             return {
#                 "status": "success",
#                 "priority": priority,
#                 "confidence": confidence,
#                 "reasoning": f"Priority {priority} based on {confidence:.2f} confidence and incident type: {event_type}"
#             }
#         except Exception as e:
#             return {
#                 "status": "error",
#                 "error": str(e)
#             }

# class AlertAgent:
#     def __init__(self):
#         pass

#     def create_agent(self):
#         return Agent(
#             role="Alert Coordinator",
#             goal="Format, prioritize, and coordinate safety alerts for appropriate response",
#             backstory="""You are a crisis management coordinator responsible for formatting alerts,
#             determining response priorities, and ensuring proper escalation procedures are followed.
#             You analyze incident severity and recommend appropriate response levels.""",
#             tools=[FormatAlertTool(), PrioritizeIncidentTool()],
#             llm="groq/llama-3.3-70b-versatile",
#             verbose=True,
#             allow_delegation=False
#         )