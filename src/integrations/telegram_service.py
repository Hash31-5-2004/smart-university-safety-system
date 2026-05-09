"""
Telegram Integration Service for Campus Safety Alerts
Handles real-time alert distribution to security staff groups
Supports both text alerts and image uploads
"""

import os
import asyncio
from typing import Optional
from datetime import datetime
from dotenv import load_dotenv
from telegram import Bot, ChatPermissions
from telegram.error import TelegramError
from pathlib import Path

load_dotenv()


class TelegramService:
    """Service for sending alerts and notifications via Telegram."""
    
    def __init__(self):
        """Initialize Telegram bot with token and group ID from environment."""
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.group_id = os.getenv("TELEGRAM_GROUP_ID")
        
        if not self.bot_token or not self.group_id:
            raise ValueError(
                "Missing TELEGRAM_BOT_TOKEN or TELEGRAM_GROUP_ID in environment variables. "
                "Please set these in your .env file."
            )
        
        self.bot = Bot(token=self.bot_token)
        self.group_id = int(self.group_id)

    async def send_alert(
        self, 
        incident_type: str,
        location: str,
        confidence: float,
        priority: str,
        description: str = "",
        recommendations: str = ""
    ) -> bool:
        """
        Send a formatted alert to the security staff group.
        
        Args:
            incident_type: Type of incident detected
            location: Location where incident occurred
            confidence: Confidence score (0-1)
            priority: Priority level (CRITICAL, HIGH, MEDIUM, LOW)
            description: Detailed description of the incident
            recommendations: Safety recommendations
            
        Returns:
            True if message sent successfully, False otherwise
        """
        try:
            # Format message with emoji indicators for priority
            priority_emoji = {
                "CRITICAL": "🚨",
                "HIGH": "⚠️",
                "MEDIUM": "⏱️",
                "LOW": "ℹ️"
            }
            emoji = priority_emoji.get(priority, "📢")
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            message = (
                f"{emoji} <b>CAMPUS SAFETY ALERT</b>\n\n"
                f"<b>Priority:</b> {priority}\n"
                f"<b>Incident Type:</b> {incident_type}\n"
                f"<b>Location:</b> {location}\n"
                f"<b>Confidence:</b> {confidence:.1%}\n"
                f"<b>Timestamp:</b> {timestamp}\n"
            )
            
            if description:
                message += f"\n<b>Description:</b>\n{description}\n"
            
            if recommendations:
                message += f"\n<b>Recommended Actions:</b>\n{recommendations}\n"
            
            message += "\n<i>Security Team - Immediate Action Required</i>"
            
            # Send to group
            await self.bot.send_message(
                chat_id=self.group_id,
                text=message,
                parse_mode="HTML"
            )
            
            print(f"[TELEGRAM] Alert sent to group {self.group_id} at {timestamp}")
            return True
            
        except TelegramError as e:
            print(f"[TELEGRAM ERROR] Failed to send alert: {str(e)}")
            return False
        except Exception as e:
            print(f"[TELEGRAM ERROR] Unexpected error: {str(e)}")
            return False

    async def send_status_update(self, message: str) -> bool:
        """
        Send a general status update to the security staff group.
        
        Args:
            message: Status message to send
            
        Returns:
            True if message sent successfully, False otherwise
        """
        try:
            formatted_message = f"📊 <b>Status Update</b>\n\n{message}"
            
            await self.bot.send_message(
                chat_id=self.group_id,
                text=formatted_message,
                parse_mode="HTML"
            )
            return True
        except TelegramError as e:
            print(f"[TELEGRAM ERROR] Failed to send status: {str(e)}")
            return False

    def send_alert_sync(
        self,
        incident_type: str,
        location: str,
        confidence: float,
        priority: str,
        description: str = "",
        recommendations: str = ""
    ) -> bool:
        """
        Synchronous wrapper for send_alert. Use this when you can't use async.
        
        Args:
            incident_type: Type of incident detected
            location: Location where incident occurred
            confidence: Confidence score (0-1)
            priority: Priority level (CRITICAL, HIGH, MEDIUM, LOW)
            description: Detailed description of the incident
            recommendations: Safety recommendations
            
        Returns:
            True if message sent successfully, False otherwise
        """
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        return loop.run_until_complete(
            self.send_alert(
                incident_type=incident_type,
                location=location,
                confidence=confidence,
                priority=priority,
                description=description,
                recommendations=recommendations
            )
        )

    def send_status_update_sync(self, message: str) -> bool:
        """
        Synchronous wrapper for send_status_update. Use this when you can't use async.
        
        Args:
            message: Status message to send
            
        Returns:
            True if message sent successfully, False otherwise
        """
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        return loop.run_until_complete(self.send_status_update(message))

    async def send_alert_with_image(
        self,
        image_path: str,
        incident_type: str,
        location: str,
        confidence: float,
        priority: str,
        description: str = "",
        recommendations: str = ""
    ) -> bool:
        """
        Send an alert with image to the security staff group.
        
        Args:
            image_path: Path to the incident image file
            incident_type: Type of incident detected
            location: Location where incident occurred
            confidence: Confidence score (0-1)
            priority: Priority level (CRITICAL, HIGH, MEDIUM, LOW)
            description: Detailed description of the incident
            recommendations: Safety recommendations
            
        Returns:
            True if message sent successfully, False otherwise
        """
        try:
            # Validate image file exists
            if not os.path.exists(image_path):
                print(f"[TELEGRAM ERROR] Image file not found: {image_path}")
                return False
            
            # Format text message
            priority_emoji = {
                "CRITICAL": "🚨",
                "HIGH": "⚠️",
                "MEDIUM": "⏱️",
                "LOW": "ℹ️"
            }
            emoji = priority_emoji.get(priority, "📢")
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            message = (
                f"{emoji} <b>CAMPUS SAFETY ALERT</b>\n\n"
                f"<b>Priority:</b> {priority}\n"
                f"<b>Incident Type:</b> {incident_type}\n"
                f"<b>Location:</b> {location}\n"
                f"<b>Confidence:</b> {confidence:.1%}\n"
                f"<b>Timestamp:</b> {timestamp}\n"
            )
            
            if description:
                # Truncate description if needed
                desc_limit = 150
                if len(description) > desc_limit:
                    description = description[:desc_limit] + "..."
                message += f"\n<b>Description:</b>\n{description}\n"
            
            if recommendations:
                # Truncate recommendations due to Telegram's 1024 character caption limit
                # Reserve ~200 chars for the rest of the message
                rec_limit = 250
                if len(recommendations) > rec_limit:
                    recommendations = recommendations[:rec_limit] + "..."
                message += f"\n<b>Actions:</b>\n{recommendations}\n"
            
            message += "<i>Security Team - Immediate Action Required</i>"
            
            # Enforce Telegram's 1024 character caption limit
            TELEGRAM_CAPTION_LIMIT = 1024
            if len(message) > TELEGRAM_CAPTION_LIMIT:
                # If still too long, truncate at the end
                message = message[:TELEGRAM_CAPTION_LIMIT-3] + "..."
                print(f"[TELEGRAM WARNING] Caption truncated to {TELEGRAM_CAPTION_LIMIT} characters")
            
            # Send image with caption
            with open(image_path, "rb") as image_file:
                await self.bot.send_photo(
                    chat_id=self.group_id,
                    photo=image_file,
                    caption=message,
                    parse_mode="HTML"
                )
            
            print(f"[TELEGRAM] Alert with image sent to group {self.group_id} at {timestamp}")
            return True
            
        except TelegramError as e:
            print(f"[TELEGRAM ERROR] Failed to send alert with image: {str(e)}")
            return False
        except Exception as e:
            print(f"[TELEGRAM ERROR] Unexpected error: {str(e)}")
            return False

    def send_alert_with_image_sync(
        self,
        image_path: str,
        incident_type: str,
        location: str,
        confidence: float,
        priority: str,
        description: str = "",
        recommendations: str = ""
    ) -> bool:
        """
        Synchronous wrapper for send_alert_with_image. Use this when you can't use async.
        
        Args:
            image_path: Path to the incident image file
            incident_type: Type of incident detected
            location: Location where incident occurred
            confidence: Confidence score (0-1)
            priority: Priority level (CRITICAL, HIGH, MEDIUM, LOW)
            description: Detailed description of the incident
            recommendations: Safety recommendations
            
        Returns:
            True if message sent successfully, False otherwise
        """
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        return loop.run_until_complete(
            self.send_alert_with_image(
                image_path=image_path,
                incident_type=incident_type,
                location=location,
                confidence=confidence,
                priority=priority,
                description=description,
                recommendations=recommendations
            )
        )

    async def get_group_info(self) -> Optional[dict]:
        """Get information about the telegram group."""
        try:
            chat = await self.bot.get_chat(self.group_id)
            return {
                "id": chat.id,
                "title": chat.title,
                "type": chat.type,
                "members_count": chat.get_member_count() if hasattr(chat, 'get_member_count') else None
            }
        except TelegramError as e:
            print(f"[TELEGRAM ERROR] Could not get group info: {str(e)}")
            return None


# Convenience function for easy imports
def get_telegram_service() -> TelegramService:
    """Factory function to get a configured Telegram service instance."""
    return TelegramService()
