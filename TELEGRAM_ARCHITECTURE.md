# Telegram Integration Architecture

## System Overview

Your Smart University Safety System now includes Telegram as a real-time alert channel alongside the existing n8n webhook integration.

```
┌─────────────────────────────────────────────────────────────────┐
│                     INCIDENT DETECTION                           │
│                    (Camera Feed Input)                            │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│              COMPUTER VISION AGENT                              │
│  • Analyzes image for anomalies                                │
│  • Detects: fights, falls, unauthorized access, etc.          │
│  • Confidence scoring (0-1)                                   │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                 RAG AGENT                                        │
│  • Retrieves relevant safety protocols                         │
│  • Queries knowledge base (NIST, campus policies, etc.)       │
│  • Generates recommendations                                  │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│              ALERT AGENT (UPDATED)                              │
│  • Formats structured alert                                    │
│  • Calculates priority level                                  │
│  • Dispatches to multiple channels                            │
└──────────┬──────────────────────────────────┬──────────────────┘
           │                                  │
           ▼                                  ▼
    ┌──────────────────┐            ┌──────────────────┐
    │   N8N WEBHOOK    │            │ TELEGRAM GROUP   │
    │  (Automation)    │            │  (Real-time)     │
    └──────────────────┘            └──────────────────┘
           │                                  │
           ▼                                  ▼
    Automated                        Security Staff
    responses                        notifications
```

## Component Details

### 1. TelegramService (src/integrations/telegram_service.py)

Core service managing Telegram bot communication.

**Methods:**
- `send_alert_sync()` - Synchronous alert sending
- `send_alert()` - Asynchronous alert sending  
- `send_status_update_sync()` - Synchronous status updates
- `send_status_update()` - Asynchronous status updates
- `get_group_info()` - Retrieve group information

**Features:**
- Async/await support for non-blocking operations
- Error handling with graceful fallbacks
- Formatted messages with emoji indicators
- Structured data with timestamps

### 2. Telegram Tools (src/integrations/telegram_tool.py)

CrewAI-compatible tools for use in agent workflows.

**Tools:**
- `SendTelegramAlertTool` - Agent can send alerts
- `SendTelegramStatusTool` - Agent can send status updates

**Schema Validation:**
- Pydantic BaseModel for type safety
- Automatic validation of alert parameters
- Clear error messages for invalid inputs

### 3. Updated AlertAgent (src/agents/alert_agent.py)

Alert agent now includes Telegram tools alongside existing n8n integration.

**Tools Available:**
1. `FormatAlertTool` - Structure alert data
2. `PrioritizeIncidentTool` - Calculate priority
3. `SendToN8NTool` - Webhook dispatch (existing)
4. `SendTelegramAlertTool` - Telegram dispatch (NEW)
5. `SendTelegramStatusTool` - Status updates (NEW)

## Data Flow

### Alert Processing Sequence

```
1. CV Agent Output (raw detection)
   └─ location: "Building A - Floor 3"
   └─ event: "Fight detected"
   └─ confidence: 0.92
   └─ caption: "Two individuals engaged in physical altercation"

2. RAG Agent Output (recommendations)
   └─ incident: "Violence"
   └─ recommendations: "Alert security, isolate area"
   └─ source: "campus_safety_3.txt"

3. FormatAlertTool (structured alert)
   └─ timestamp: "2026-04-29 14:23:45"
   └─ location: "Building A - Floor 3"
   └─ incident_type: "Fight detected"
   └─ confidence: 0.92
   └─ priority: "CRITICAL"
   └─ description: "Two individuals engaged..."
   └─ recommendations: "Alert security, isolate area"

4. Parallel Dispatch:
   ├─→ SendTelegramAlertTool
   │   └─ Formats with emoji
   │   └─ Sends to group
   │   └─ Returns: ✅ "Alert sent to security staff group"
   │
   └─→ SendToN8NTool
       └─ Posts to webhook
       └─ Triggers automation
       └─ Returns: ✅ "Alert dispatched to n8n"
```

## Environment Configuration

**Required:**
```
TELEGRAM_BOT_TOKEN=123456789:ABCDEfghIjklmnopQRSTuvwxyz1234567890
TELEGRAM_GROUP_ID=-1001234567890
```

**Optional:**
```
GROQ_API_KEY=your_groq_key  # For LLM agent
```

## Message Format

### Alert Message Structure

```html
🚨 CAMPUS SAFETY ALERT

Priority: CRITICAL
Incident Type: Fight detected
Location: Building A - Floor 3
Confidence: 92.0%
Timestamp: 2026-04-29 14:23:45

Description:
Two individuals engaged in physical altercation

Recommended Actions:
Alert security immediately. Isolate area. Review camera footage.

Security Team - Immediate Action Required
```

### Priority Emoji Mapping

| Priority | Emoji | Trigger | Use Case |
|----------|-------|---------|----------|
| CRITICAL | 🚨 | Confidence > 0.9 OR fight/assault/weapon | Immediate response needed |
| HIGH | ⚠️ | Confidence > 0.7 OR fall/medical/injury | Urgent response needed |
| MEDIUM | ⏱️ | Confidence > 0.5 | Standard response |
| LOW | ℹ️ | Confidence ≤ 0.5 | Informational |

## Integration Points

### With CrewAI Agent System

```python
class AlertAgent:
    def create_agent(self):
        return Agent(
            role="Emergency Alert Coordinator",
            tools=[
                FormatAlertTool(),
                PrioritizeIncidentTool(),
                SendToN8NTool(),           # Existing
                SendTelegramAlertTool(),   # NEW
                SendTelegramStatusTool()   # NEW
            ],
            ...
        )
```

The agent can now:
- Format alerts
- Determine priority
- Send via Telegram
- Send via n8n
- All in the same workflow

### With Environment Variables

```python
from dotenv import load_dotenv
import os

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_GROUP_ID = os.getenv("TELEGRAM_GROUP_ID")
```

### With Error Handling

```python
try:
    success = service.send_alert_sync(...)
    if success:
        return "✅ Alert sent successfully"
    else:
        return "⚠️ Failed - check configuration"
except TelegramError as e:
    return f"❌ Telegram error: {str(e)}"
except Exception as e:
    return f"❌ Unexpected error: {str(e)}"
```

## Security Architecture

### Token Management
- Bot token stored in `.env` (not in code)
- `.env` ignored by git
- Never logged or displayed

### Group Permissions
- Bot requires "Post Messages" permission only
- Can't delete messages or ban users
- Can't access group member information
- Read-only access to group updates

### Validation
- Pydantic models validate all inputs
- Type checking for confidence (0-1)
- Enum validation for priority levels
- String sanitization for safety

## Deployment Scenarios

### Scenario 1: Single Security Group
```
All incidents → Single Telegram Group
├─ CRITICAL alerts show 🚨
├─ HIGH alerts show ⚠️
├─ MEDIUM/LOW shown for reference
└─ All staff see all incidents
```

### Scenario 2: Multiple Security Teams (Future)
```
Can extend to support:
├─ Group A (Admin)
├─ Group B (Security)
├─ Group C (Facilities)
└─ Different priority thresholds per group
```

### Scenario 3: Escalation Path (Future)
```
Priority-based routing:
├─ CRITICAL → SMS + Telegram
├─ HIGH → Telegram + Email
├─ MEDIUM → Telegram only
└─ LOW → Logged only
```

## Performance Considerations

### Async Design
- Non-blocking alert sending
- Doesn't slow down CV/RAG processing
- Multiple alerts sent in parallel

### Error Resilience
- Telegram failure doesn't block n8n
- Graceful fallbacks to logging
- Retries handled by Telegram API

### Rate Limiting
- Telegram allows ~30 messages/second per group
- Campus incident rate rarely exceeds this
- Safe for normal operations

## Testing & Validation

### Unit Tests Available
- `test_telegram.py` - Comprehensive integration test
- Tests connection, alerts, status updates
- Tests priority level formatting
- Validates emoji indicators

### Integration Points Tested
1. ✅ Environment variable loading
2. ✅ Bot token validation
3. ✅ Group ID validation
4. ✅ Message formatting
5. ✅ Alert sending
6. ✅ Status updates
7. ✅ Error handling

## Future Enhancements

### Possible Extensions
1. **Incoming Commands**
   - Security staff ask bot for status
   - Query incident history
   - Acknowledge alerts

2. **Multimedia Alerts**
   - Send incident images
   - Include video clips
   - Share camera feeds

3. **Advanced Routing**
   - Multiple groups by severity
   - On-call escalation
   - Role-based distribution

4. **Metrics & Analytics**
   - Response time tracking
   - Alert statistics
   - Trend analysis

## Files Reference

| File | Purpose | Type |
|------|---------|------|
| `src/integrations/telegram_service.py` | Core Telegram API wrapper | Module |
| `src/integrations/telegram_tool.py` | CrewAI integration tools | Module |
| `src/integrations/__init__.py` | Package initialization | Module |
| `src/agents/alert_agent.py` | Agent with Telegram tools | Module (Updated) |
| `.env.example` | Configuration template | Config |
| `TELEGRAM_SETUP.md` | Detailed setup guide | Documentation |
| `TELEGRAM_QUICKSTART.md` | Quick start guide | Documentation |
| `TELEGRAM_INTEGRATION.md` | Integration overview | Documentation |
| `test_telegram.py` | Testing script | Utility |
| `find_group_id.py` | Group ID helper | Utility |

---

## Summary

Your safety system now has **dual-channel alert distribution**:

1. **n8n** - Handles automation and complex workflows
2. **Telegram** - Provides real-time human notification

Both work independently, so failure of one doesn't impact the other. Security staff get instant notifications while automated systems handle technical responses.

**Status: ✅ Ready for deployment**
