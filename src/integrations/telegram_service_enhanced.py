"""
Enhanced Telegram Integration Service with Retry Logic
Handles real-time alert distribution with exponential backoff
"""

import os
import asyncio
import time
from typing import Optional, Dict, Any
from datetime import datetime
from dotenv import load_dotenv
from telegram import Bot, ChatPermissions
from telegram.error import TelegramError, RetryAfter, NetworkError
from pathlib import Path
import logging

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EnhancedTelegramService:
    """Enhanced Telegram service with retry logic and error recovery."""
    
    def __init__(self, max_retries: int = 3, base_delay: float = 1.0):
        """
        Initialize Telegram bot with retry configuration.
        
        Args:
            max_retries: Maximum number of retry attempts
            base_delay: Base delay for exponential backoff (seconds)
        """
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.group_id = os.getenv("TELEGRAM_GROUP_ID")
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.delivery_stats = {
            "sent": 0,
            "failed": 0,
            "retried": 0,
            "total_attempts": 0
        }
        
        if not self.bot_token or not self.group_id:
            raise ValueError(
                "Missing TELEGRAM_BOT_TOKEN or TELEGRAM_GROUP_ID in environment variables. "
                "Please set these in your .env file."
            )
        
        self.bot = Bot(token=self.bot_token)
        self.group_id = int(self.group_id)

    def _calculate_backoff(self, attempt: int) -> float:
        """
        Calculate exponential backoff delay.
        
        Args:
            attempt: Current retry attempt (0-indexed)
            
        Returns:
            Delay in seconds with jitter
        """
        import random
        delay = self.base_delay * (2 ** attempt)
        jitter = random.uniform(0, delay * 0.1)  # 10% jitter
        return delay + jitter

    async def send_alert_with_retry(
        self, 
        incident_type: str,
        location: str,
        confidence: float,
        priority: str,
        description: str = "",
        recommendations: str = ""
    ) -> Dict[str, Any]:
        """
        Send alert with automatic retry on failure.
        
        Args:
            incident_type: Type of incident detected
            location: Location where incident occurred
            confidence: Confidence score (0-1)
            priority: Priority level (CRITICAL, HIGH, MEDIUM, LOW)
            description: Detailed description
            recommendations: Safety recommendations
            
        Returns:
            Dict with success status, attempts, and error details
        """
        result = {
            "success": False,
            "attempts": 0,
            "message_id": None,
            "error": None,
            "recovery": False
        }
        
        for attempt in range(self.max_retries):
            result["attempts"] = attempt + 1
            self.delivery_stats["total_attempts"] += 1
            
            try:
                # Format message
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
                
                # Send message
                response = await self.bot.send_message(
                    chat_id=self.group_id,
                    text=message,
                    parse_mode="HTML",
                    read_timeout=10,
                    write_timeout=10,
                    connect_timeout=10,
                    pool_timeout=10
                )
                
                result["success"] = True
                result["message_id"] = response.message_id
                self.delivery_stats["sent"] += 1
                
                if attempt > 0:
                    result["recovery"] = True
                    self.delivery_stats["retried"] += 1
                    logger.info(f"Message sent successfully on attempt {attempt + 1}")
                
                return result
                
            except RetryAfter as e:
                # Telegram rate limiting
                wait_time = e.retry_after
                logger.warning(f"Rate limit hit. Waiting {wait_time}s before retry...")
                await asyncio.sleep(wait_time)
                continue
                
            except NetworkError as e:
                # Network connectivity issues - retry with backoff
                if attempt < self.max_retries - 1:
                    backoff = self._calculate_backoff(attempt)
                    logger.warning(f"Network error (attempt {attempt + 1}): {str(e)}. Retrying in {backoff:.2f}s...")
                    await asyncio.sleep(backoff)
                    continue
                else:
                    result["error"] = f"Network error: {str(e)}"
                    
            except TelegramError as e:
                # Telegram-specific errors
                error_str = str(e)
                if "429" in error_str or "rate" in error_str.lower():
                    # Rate limiting - extract wait time if available
                    if attempt < self.max_retries - 1:
                        backoff = self._calculate_backoff(attempt)
                        logger.warning(f"Rate limit (attempt {attempt + 1}). Waiting {backoff:.2f}s...")
                        await asyncio.sleep(backoff)
                        continue
                
                if attempt < self.max_retries - 1:
                    backoff = self._calculate_backoff(attempt)
                    logger.warning(f"Telegram error (attempt {attempt + 1}): {error_str}. Retrying in {backoff:.2f}s...")
                    await asyncio.sleep(backoff)
                    continue
                else:
                    result["error"] = f"Telegram error: {error_str}"
                    
            except Exception as e:
                # Unexpected errors
                if attempt < self.max_retries - 1:
                    backoff = self._calculate_backoff(attempt)
                    logger.warning(f"Unexpected error (attempt {attempt + 1}): {str(e)}. Retrying in {backoff:.2f}s...")
                    await asyncio.sleep(backoff)
                    continue
                else:
                    result["error"] = f"Unexpected error: {str(e)}"
        
        self.delivery_stats["failed"] += 1
        return result

    def send_alert_sync(
        self,
        incident_type: str,
        location: str,
        confidence: float,
        priority: str,
        description: str = "",
        recommendations: str = ""
    ) -> Dict[str, Any]:
        """
        Synchronous wrapper for send_alert_with_retry.
        
        Returns:
            Dict with delivery results
        """
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        return loop.run_until_complete(
            self.send_alert_with_retry(
                incident_type=incident_type,
                location=location,
                confidence=confidence,
                priority=priority,
                description=description,
                recommendations=recommendations
            )
        )

    def get_delivery_stats(self) -> Dict[str, Any]:
        """Get delivery statistics."""
        total = self.delivery_stats["total_attempts"]
        successful = self.delivery_stats["sent"]
        delivery_rate = (successful / total * 100) if total > 0 else 0
        
        return {
            **self.delivery_stats,
            "delivery_rate_percent": round(delivery_rate, 2),
            "average_attempts": round(total / max(successful, 1), 2) if successful > 0 else 0
        }

    def reset_stats(self):
        """Reset delivery statistics."""
        self.delivery_stats = {
            "sent": 0,
            "failed": 0,
            "retried": 0,
            "total_attempts": 0
        }
