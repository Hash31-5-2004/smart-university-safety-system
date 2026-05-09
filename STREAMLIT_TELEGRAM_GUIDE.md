# Streamlit Dashboard + Telegram with Image Alerts Guide

## Complete Integration Overview

Your Smart University Safety System now has a fully integrated dashboard with **real-time image alerts to Telegram**. Here's what happens:

```
Streamlit Dashboard
    ↓
Upload Image → Analyze → Generate Alert
    ↓
Sends to:
├─→ N8N Webhook (Automation)
├─→ Telegram (Real-time with IMAGE)
└─→ Dashboard Display
```

---

## What's New

### 🖼️ Image Upload Support
- Upload incident images directly from the dashboard
- Images are analyzed with CV + RAG
- **Images are sent to Telegram with the alert** ← NEW!

### 🚨 Smart Alert Routing
- All alerts go to Telegram group with the incident image
- All alerts go to n8n for automation
- Dashboard displays alert in real-time

### 📊 Dual-Channel Notifications
- **Telegram**: Real-time notification with visual evidence
- **N8N**: Automation (emails, tickets, logging, etc.)

---

## Using the Dashboard

### Step 1: Start the Dashboard

```bash
streamlit run dashboard.py
```

You should see:
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://your-ip:8501
```

Open your browser to: **http://localhost:8501**

### Step 2: Upload an Incident Image

1. In the "📤 Upload Image or Video for Analysis" section
2. Click the upload box
3. Select an image file (PNG, JPG, JPEG, TIF, BMP)
4. Image preview appears

### Step 3: Select Location

Choose where the incident occurred:
- Building A entrance
- Library side entrance
- Main Courtyard
- Building C parking
- Science Lab entrance

Or edit the list in dashboard.py to add your locations.

### Step 4: Analyze & Generate Alert

Click **"🔍 Analyze Media & Generate Alert"** button

The system will:
1. ✅ Analyze image for anomalies (Computer Vision)
2. ✅ Query knowledge base for recommendations (RAG)
3. ✅ Format structured alert
4. ✅ Send to Telegram with image
5. ✅ Send to n8n for automation
6. ✅ Display in dashboard

### Step 5: Monitor Results

Check for confirmation messages:

```
✅ Alert with image sent to Telegram security group
✅ Alert sent to n8n for email notifications
🚨 ACTIVE ALERT at Building A entrance
```

Check your **Telegram group** for the alert with image.

---

## What Happens in Telegram

### Alert with Image Format

When you generate an alert, your Telegram security group receives:

```
[IMAGE PREVIEW]

🚨 CAMPUS SAFETY ALERT

Priority: CRITICAL
Incident Type: Physical Altercation
Location: Building A entrance
Confidence: 92.0%
Timestamp: 2026-04-29 14:23:45

Description: Two individuals engaged in physical altercation

Recommended Actions:
Alert security immediately. Separate individuals. Call medical if injured.

Security Team - Immediate Action Required
```

### Why Include Images?

- ✅ **Visual Proof**: Security staff see the actual incident
- ✅ **Faster Response**: No need to pull footage separately
- ✅ **Better Decision-Making**: Context from the image
- ✅ **Evidence**: Recorded evidence of the incident

---

## Complete Workflow Example

### Scenario: Fight Detected

1. **Dashboard**: Security personnel sees monitor
2. **Upload**: Captures screenshot/image of fight
3. **Analyze**: Click "Analyze Media & Generate Alert"
4. **Results**:
   - 📊 Dashboard shows alert with details
   - 📱 Telegram group receives image + alert
   - 🔄 N8N workflow starts (could email, log, etc.)

### Timeline

```
14:23:45 - User uploads image to dashboard
14:23:50 - Image analyzed (CV + RAG)
14:23:52 - Alert generated
14:23:53 - Telegram: Image + alert sent
14:23:54 - N8N: Webhook received
14:23:55 - Dashboard: Alert displayed
```

---

## Dashboard Features

### System Status (Sidebar)

Shows:
- ✅ Image/Video Input Ready
- ✅ Groq RAG Ready
- 📚 Knowledge Base Documents count
- 🔍 Debug info (if enabled)

### RAG Test Query

Test the knowledge base:
- Ask safety questions
- Get instant recommendations
- Verify knowledge base is loaded

Example:
```
Question: "What are the NIST guidelines for incident response?"
Answer: [Detailed NIST response from knowledge base]
```

### Alert Display

After analysis, shows:
- 🚨 ACTIVE ALERT badge
- 📍 Location
- ⏰ Time
- 📊 Confidence score
- 📝 Image description
- 💡 Recommended actions (from RAG)

---

## Configuration Options

### Edit Locations

In dashboard.py, find this section:

```python
location = st.selectbox("Detected Location", [
    "Building A entrance",
    "Library side entrance", 
    "Main Courtyard",
    "Building C parking",
    "Science Lab entrance"
])
```

Add your campus locations:

```python
location = st.selectbox("Detected Location", [
    "Building A entrance",
    "Building A 2nd floor",
    "Building B - Main Hall",
    "Campus Security Office",
    "Student Center",
    "Parking Lot A",
    "Athletic Fields",
    "Library entrance"
])
```

### Configure N8N Webhook

```python
N8N_WEBHOOK_URL = "your-n8n-webhook-url-here"
```

### Optional: Add Authentication

```python
N8N_API_KEY = os.getenv("N8N_API_KEY", "")
```

---

## Troubleshooting

### Issue: Image Not Appearing in Telegram

**Symptoms**: Alert sent but no image in group

**Solutions**:
1. Check Telegram bot has "Post Messages" permission
2. Verify image file exists and is readable
3. Check file size (Telegram has limits)
4. Check for file format support (PNG, JPG, etc.)
5. Look at Streamlit console for errors

### Issue: Alert Not Going to Telegram

**Symptoms**: Streamlit shows success, but no message in group

**Solutions**:
1. Run `python test_telegram.py` to verify bot works
2. Check `.env` file has correct `TELEGRAM_BOT_TOKEN` and `TELEGRAM_GROUP_ID`
3. Verify bot is added to group with Admin permissions
4. Check network connectivity
5. Review console output for error messages

### Issue: N8N Not Receiving Alert

**Symptoms**: Alert sent to Streamlit, but n8n shows no execution

**Solutions**:
1. Verify webhook URL in dashboard.py
2. Test webhook with curl
3. Check n8n workflow is active/published
4. Look for timeout errors in Streamlit logs
5. Verify network connectivity to n8n

### Issue: Image Analysis Taking Too Long

**Symptoms**: "Processing image..." spinner hangs

**Solutions**:
1. Check CPU usage (CV analysis is intensive)
2. Try with a smaller image
3. Restart Streamlit
4. Check disk space (temp files)
5. Look at console for error messages

---

## Testing Checklist

Before going live:

- [ ] Dashboard starts without errors
- [ ] Can upload images (PNG, JPG, TIF)
- [ ] RAG test query works
- [ ] Alert generated successfully
- [ ] Image appears in Telegram with alert
- [ ] Telegram group receives proper emoji (🚨 ⚠️ ⏱️ ℹ️)
- [ ] N8N receives alert via webhook
- [ ] N8N execution shows alert data
- [ ] Confidence scores display correctly
- [ ] Timestamps are accurate
- [ ] All security staff can see Telegram alerts

---

## Performance Tips

### Optimize Image Upload

```python
# In dashboard.py
# Resize large images before analysis
from PIL import Image

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    
    # Resize if too large
    if img.size[0] > 1920:
        img.thumbnail((1920, 1440))
```

### Reduce Processing Time

```python
# Images larger than needed slow down CV analysis
# Recommended: 640x480 to 1280x720 pixels
```

### Parallel Processing

N8N processes alerts while Streamlit is responsive:

```
Streamlit (Fast): Show alert to user ✓ (1 second)
N8N (Background): Process automation (may take longer)
```

---

## Security Considerations

### Image Storage

⚠️ **Important**: Uploaded images are temporary
- Stored in `/tmp/` only
- Deleted after alert is sent
- Not persisted to disk
- For permanent storage, use n8n to save to database

### Image Privacy

- Only people in Telegram group see images
- Only n8n webhook has access via API
- Dashboard is local (http://localhost:8501)
- Never send images over unsecured networks

### Access Control

- Restrict Telegram group to authorized personnel only
- Use strong bot tokens (never share)
- Keep `.env` file secure (don't commit to git)
- Use VPN/SSH for remote dashboard access

---

## Advanced Features

### Custom Incident Types

Modify priority calculation in `send_alert_to_telegram()`:

```python
def send_alert_to_telegram(...):
    # Customize priority logic
    if "weapon" in event_type.lower():
        priority = "CRITICAL"
    elif "fire" in event_type.lower():
        priority = "CRITICAL"
    elif "medical" in event_type.lower():
        priority = "HIGH"
    ...
```

### Add More Alert Channels

```python
# After Telegram alert
send_alert_to_slack(...)  # Add Slack
send_alert_to_teams(...)  # Add Teams
send_alert_to_sms(...)    # Add SMS
```

### Log Incidents

```python
# In dashboard.py, add logging
import json
from datetime import datetime

with open("incident_log.jsonl", "a") as f:
    incident = {
        "timestamp": datetime.now().isoformat(),
        "location": location,
        "confidence": confidence,
        "event": event_dict.get("event")
    }
    f.write(json.dumps(incident) + "\n")
```

---

## Real-World Example

### Scenario: Campus Incident Response

**Time: 14:23**
- Security camera detects suspicious activity
- Guard takes screenshot

**Time: 14:24**
1. Guard uploads image to Streamlit dashboard
2. System analyzes: "Fight detected - 92% confidence"
3. Telegram group gets instant notification with image
4. All security staff see alert immediately

**Time: 14:25**
- First responders begin moving to location
- N8N automation:
  - Sends email to campus security director
  - Creates incident ticket in system
  - Notifies facilities about location
  - Logs incident for audit

**Time: 14:27**
- Incident resolved
- All evidence documented

---

## Deployment Scenarios

### Scenario 1: Single Monitor Station
```
┌─────────────────────┐
│  Campus Security    │
│   Control Room      │
│                     │
│ Laptop running      │
│ Streamlit Dashboard │
│                     │
│ (http://localhost)  │
└─────────────────────┘
```

### Scenario 2: Multiple Locations
```
Campus Monitoring      Central Dashboard      Telegram Group
  Cameras ──→ Streamlit (Main Server) ──→ All Security Staff
              (via Network/SSH)              Real-time
```

### Scenario 3: Automated Monitoring
```
Automated               Streamlit API       Telegram + N8N
Camera Feed ──→ Continuous Analysis ──→ Automated Responses
               (Scripts calling API)      (Emails, Tickets, etc.)
```

---

## Files Modified

| File | Changes |
|------|---------|
| `dashboard.py` | Added Telegram import, send_alert_to_telegram() function, image handling |
| `src/integrations/telegram_service.py` | Added send_alert_with_image() and sync wrapper |
| `src/integrations/telegram_tool.py` | Added SendTelegramAlertWithImageTool |
| `src/agents/alert_agent.py` | Added image tool to agent |

---

## Next Steps

1. ✅ Start Streamlit: `streamlit run dashboard.py`
2. ✅ Upload test image
3. ✅ Generate alert
4. ✅ Verify Telegram receives image
5. ✅ Check N8N executions
6. ✅ Customize locations and workflows
7. ✅ Deploy to production

---

## Support & Debugging

### Check Console Output

When running `streamlit run dashboard.py`, watch for:

```
✅ Image/Video Input Ready
✅ Groq RAG Ready
✅ Knowledge Base Documents: 17

Processing image → Detecting anomalies → Generating description → Running RAG...
✅ Alert with image sent to Telegram security group
✅ Alert sent to n8n for email notifications
```

### Enable Debug Mode

Add to dashboard.py:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Now you'll see detailed logs
```

### Test Each Component

```bash
# Test Telegram
python test_telegram.py

# Test N8N webhook
curl -X POST "https://your-webhook" -H "Content-Type: application/json" \
  -d '{"test": "data"}'

# Test CV detector
python -c "from src.cv_detection.anomaly_detector import CampusAnomalyDetector; cd = CampusAnomalyDetector()"

# Test RAG
python -c "from src.rag.rag_pipeline import UniversitySafetyRAG; rag = UniversitySafetyRAG()"
```

---

**Your campus is now monitored with real-time image alerts to your security team!** 🛡️📱🖼️
