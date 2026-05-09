"""
Telegram Tool for CrewAI Integration
Allows the alert agent to send alerts to Telegram
Supports text alerts and image uploads
"""

from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Optional
from src.integrations.telegram_service import get_telegram_service


class SendTelegramAlertArgs(BaseModel):
    """Arguments for sending a Telegram alert."""
    incident_type: str = Field(..., description="Type of incident (e.g., 'Fight', 'Medical Emergency')")
    location: str = Field(..., description="Location where incident occurred")
    confidence: float = Field(..., description="Confidence score of detection (0-1)")
    priority: str = Field(..., description="Priority level: CRITICAL, HIGH, MEDIUM, or LOW")
    description: Optional[str] = Field(None, description="Detailed description of the incident")
    recommendations: Optional[str] = Field(None, description="Safety recommendations")


class SendTelegramAlertTool(BaseTool):
    """Tool for sending safety alerts to Telegram group."""
    
    name: str = "Send Telegram Alert"
    description: str = (
        "Sends a formatted safety alert to the security staff Telegram group "
        "with incident details, priority level, and recommendations."
    )
    args_schema: type[BaseModel] = SendTelegramAlertArgs

    def _run(
        self,
        incident_type: str,
        location: str,
        confidence: float,
        priority: str,
        description: Optional[str] = None,
        recommendations: Optional[str] = None
    ) -> str:
        """
        Send alert to Telegram group.
        
        Returns:
            Success or error message
        """
        try:
            telegram_service = get_telegram_service()
            
            success = telegram_service.send_alert_sync(
                incident_type=incident_type,
                location=location,
                confidence=confidence,
                priority=priority,
                description=description or "",
                recommendations=recommendations or ""
            )
            
            if success:
                return f"✅ Telegram alert sent successfully to security staff group for {incident_type} at {location}"
            else:
                return f"⚠️ Failed to send Telegram alert. System may be offline or misconfigured."
                
        except Exception as e:
            return f"❌ Error sending Telegram alert: {str(e)}"


class SendTelegramStatusArgs(BaseModel):
    """Arguments for sending a status update."""
    message: str = Field(..., description="Status message to send")


class SendTelegramStatusTool(BaseTool):
    """Tool for sending status updates to Telegram group."""
    
    name: str = "Send Telegram Status"
    description: str = "Sends a status update message to the security staff Telegram group"
    args_schema: type[BaseModel] = SendTelegramStatusArgs

    def _run(self, message: str) -> str:
        """
        Send status update to Telegram group.
        
        Returns:
            Success or error message
        """
        try:
            telegram_service = get_telegram_service()
            
            success = telegram_service.send_status_update_sync(message)
            
            if success:
                return f"✅ Status update sent to Telegram group"
            else:
                return f"⚠️ Failed to send status update"
                
        except Exception as e:
            return f"❌ Error sending status: {str(e)}"


class SendTelegramAlertWithImageArgs(BaseModel):
    """Arguments for sending a Telegram alert with image."""
    image_path: str = Field(..., description="Path to the incident image file")
    incident_type: str = Field(..., description="Type of incident (e.g., 'Fight', 'Medical Emergency')")
    location: str = Field(..., description="Location where incident occurred")
    confidence: float = Field(..., description="Confidence score of detection (0-1)")
    priority: str = Field(..., description="Priority level: CRITICAL, HIGH, MEDIUM, or LOW")
    description: Optional[str] = Field(None, description="Detailed description of the incident")
    recommendations: Optional[str] = Field(None, description="Safety recommendations")


class SendTelegramAlertWithImageTool(BaseTool):
    """Tool for sending safety alerts with images to Telegram group."""
    
    name: str = "Send Telegram Alert with Image"
    description: str = (
        "Sends a formatted safety alert with incident image to the security staff Telegram group "
        "with incident details, priority level, recommendations, and visual evidence."
    )
    args_schema: type[BaseModel] = SendTelegramAlertWithImageArgs

    def _run(
        self,
        image_path: str,
        incident_type: str,
        location: str,
        confidence: float,
        priority: str,
        description: Optional[str] = None,
        recommendations: Optional[str] = None
    ) -> str:
        """
        Send alert with image to Telegram group.
        
        Returns:
            Success or error message
        """
        try:
            telegram_service = get_telegram_service()
            
            success = telegram_service.send_alert_with_image_sync(
                image_path=image_path,
                incident_type=incident_type,
                location=location,
                confidence=confidence,
                priority=priority,
                description=description or "",
                recommendations=recommendations or ""
            )
            
            if success:
                return f"✅ Telegram alert with image sent successfully to security staff group for {incident_type} at {location}"
            else:
                return f"⚠️ Failed to send Telegram alert with image. Check file path and permissions."
                
        except Exception as e:
            return f"❌ Error sending Telegram alert with image: {str(e)}"
