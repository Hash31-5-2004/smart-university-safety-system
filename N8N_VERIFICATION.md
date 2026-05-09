# N8N Integration Verification Guide

## Overview

N8N is your **workflow automation engine** that handles automated responses to security alerts. Once an incident is detected, n8n can:

- Send email notifications to security staff
- Create tickets in your incident management system
- Trigger alarm systems
- Log incidents to databases
- Escalate to authorities
- And more...

This guide helps you verify that n8n is properly connected to your safety system.

---

## Current N8N Integration

Your system sends alerts to n8n via a **webhook**. Here's how it works:

```
Dashboard (Streamlit)
    ↓
Image Analysis (CV + RAG)
    ↓
Alert Generated
    ↓
Sends to:
├─→ N8N Webhook (for automation)
├─→ Telegram (for real-time notification)
└─→ Streamlit Display (for dashboard)
```

---

## Step 1: Verify N8N Webhook URL

### What is Your Current Webhook?

Check your dashboard.py file to see your n8n webhook URL:

```python
# In dashboard.py (around line 20)
N8N_WEBHOOK_URL = "https://hash3040531.app.n8n.cloud/webhook-test/home/rt-detection/smart-university-safety-system/src/agents/alert_agent.py"
```

Your URL should look like:
```
https://[your-account].app.n8n.cloud/webhook-[unique-path]
```

### ✅ Verify Webhook Exists

Open your webhook URL in a browser. You should see:
- ✅ Success message
- ✅ JSON response
- ❌ 404 or "not found" = Webhook doesn't exist (needs to be created in n8n)

---

## Step 2: Create/Update Webhook in N8N

### If You Don't Have a Webhook Yet:

1. **Log in to n8n**: https://app.n8n.cloud
2. **Create a new workflow**:
   - Click "Create new workflow"
   - Give it a name: "Campus Safety Alert Handler"
3. **Add Webhook trigger**:
   - Click "+" to add a node
   - Search for "Webhook"
   - Select "Webhook" as the trigger
4. **Configure the Webhook**:
   - Set Method: `POST`
   - Copy your webhook URL
5. **Update your dashboard.py**:
   ```python
   N8N_WEBHOOK_URL = "your_webhook_url_here"
   ```
6. **Add nodes for automation** (examples below)

### Webhook Testing Node (Simple)

Add a simple response node to verify the webhook works:

```
1. Webhook trigger (receives POST)
   ↓
2. Respond to Webhook node
   - Response Code: 200
   - Response Body: {"status": "success", "message": "Alert received"}
```

---

## Step 3: Test Webhook Manually

### Using Python Script

Create a test script to send a sample alert to n8n:

```python
import requests
import json

webhook_url = "https://your-webhook-url-here"

alert_data = {
    "time": "14:23:45",
    "location": "Building A entrance",
    "confidence": 0.92,
    "caption": "Two individuals engaged in physical altercation",
    "alert_text": "CRITICAL INCIDENT: Physical altercation detected. Recommend immediate security response.",
    "processing_mode": "Test Alert"
}

response = requests.post(webhook_url, json=alert_data)
print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")
```

### Using cURL

```bash
curl -X POST "https://your-webhook-url-here" \
  -H "Content-Type: application/json" \
  -d '{
    "time": "14:23:45",
    "location": "Building A entrance",
    "confidence": 0.92,
    "caption": "Test alert",
    "alert_text": "This is a test"
  }'
```

**Expected Response:**
```
200 OK
{"status": "success", "message": "Alert received"}
```

---

## Step 4: Monitor Webhook Calls

### Check N8N Execution History

1. Go to your n8n workflow
2. Click **"Executions"** tab at the top
3. You should see:
   - ✅ Successful executions (green)
   - ❌ Failed executions (red)
   - Timestamp of each call
   - Request/Response data

### What to Look For

**Successful Alert:**
```
✅ EXECUTION 2026-04-29 14:23:45
   Status: Success
   Duration: 234ms
   Input: {"time": "14:23:45", "location": "Building A", ...}
   Output: {"status": "success", ...}
```

**Failed Alert:**
```
❌ EXECUTION 2026-04-29 14:24:10
   Status: Error
   Error: "Webhook validation failed"
```

---

## Step 5: Real-World Verification

### Test with Streamlit Dashboard

The **best way to verify** n8n integration is to use the dashboard:

1. Start Streamlit:
   ```bash
   streamlit run dashboard.py
   ```

2. Upload an incident image

3. Click "🔍 Analyze Media & Generate Alert"

4. Check for these confirmations:
   ```
   ✅ Alert sent to n8n for email notifications
   ✅ Alert with image sent to Telegram security group
   🚨 ACTIVE ALERT at [location]
   ```

5. **Verify in N8N**:
   - Go to your n8n workflow
   - Click "Executions"
   - You should see a new execution with your alert data

---

## Step 6: Build Automation Workflows

Once verified, you can add automation to your n8n workflow:

### Example: Send Email on Alert

```
Webhook (Receive Alert)
    ↓
Filter (Check if Confidence > 0.8)
    ↓
Email (Send to security@university.edu)
    ↓
Respond to Webhook
```

### Example: Create Incident Ticket

```
Webhook (Receive Alert)
    ↓
Format Data
    ↓
HTTP Request (POST to Jira API)
    ↓
Respond to Webhook
```

### Example: Log to Database

```
Webhook (Receive Alert)
    ↓
Insert Row into MySQL/PostgreSQL
    ↓
Respond to Webhook
```

---

## Troubleshooting N8N Issues

### Issue: Webhook Returns 404

**Problem**: Your webhook URL is not found
**Solution**:
1. Check that the webhook exists in n8n
2. Verify the URL is copied correctly (no extra spaces)
3. Make sure the workflow is active
4. Test with curl from command line

### Issue: Webhook Returns 500 Error

**Problem**: There's an error in your n8n workflow
**Solution**:
1. Check the workflow for errors
2. Look at the executions log for error details
3. Test with a simple webhook (just Respond node)
4. Build up complexity slowly

### Issue: No Executions Appearing

**Problem**: Alerts aren't reaching n8n
**Solution**:
1. Verify webhook URL in dashboard.py
2. Check network connectivity
3. Test webhook manually with curl
4. Check n8n workflow is active/published
5. Look for timeout errors in Streamlit logs

### Issue: Webhook Timeout

**Problem**: N8N takes too long to respond
**Solution**:
1. Simplify your n8n workflow
2. Remove slow HTTP calls
3. Check n8n server status
4. Increase timeout in Streamlit code

---

## Verification Checklist

Use this checklist to ensure everything is working:

- [ ] N8N account created and logged in
- [ ] Webhook created in n8n
- [ ] Webhook URL updated in dashboard.py
- [ ] Webhook responds with 200 OK
- [ ] Can see executions in n8n dashboard
- [ ] Test alert sent via Streamlit
- [ ] Alert appears in n8n executions
- [ ] Telegram alert also received (dual-channel)
- [ ] No errors in Streamlit console
- [ ] No errors in n8n executions log

---

## Testing Workflow

### Complete End-to-End Test

1. **Start all services**:
   ```bash
   # Terminal 1: Streamlit
   streamlit run dashboard.py
   
   # Terminal 2: Verify environment
   python test_telegram.py  # Should pass
   ```

2. **Upload test image to Streamlit**

3. **Click "Analyze Media & Generate Alert"**

4. **Verify alerts in all channels**:
   - ✅ Streamlit displays alert
   - ✅ Telegram group receives image with alert
   - ✅ N8N executions log shows new execution
   - ✅ N8N response status is 200 OK

5. **Check n8n workflow output**:
   - Go to n8n > Your Workflow > Executions
   - Click on latest execution
   - Verify alert data is received correctly
   - Check if any automation actions triggered

---

## Example N8N Workflows

### Simple Echo Workflow (Test)

```
[Webhook] → [Respond to Webhook]
Response: {"status": "success", "received": true}
```

### Email Notification Workflow

```
[Webhook]
    ↓
[Filter] (if confidence > 0.7)
    ↓
[Send Email]
    ├─ To: security@university.edu
    ├─ Subject: "Campus Safety Alert - {{location}}"
    └─ Body: "{{caption}}\n\n{{alert_text}}"
    ↓
[Log to Database]
    ├─ Table: incidents
    └─ Columns: timestamp, location, confidence, alert_text
    ↓
[Respond to Webhook]
```

### Multi-Channel Notification

```
[Webhook]
    ├→ [Send Email] → Email
    ├→ [HTTP POST] → Slack
    ├→ [HTTP POST] → Your API
    └→ [Insert to Database]
    ↓
[Respond to Webhook] (after all complete)
```

---

## Monitoring & Debugging

### View Webhook Request Data in N8N

1. Open your workflow
2. Add a "Webhook" trigger
3. Click the trigger node
4. Look at **Recent Requests**
5. Expand a request to see:
   - Headers
   - Body (your alert data)
   - Query parameters

### Enable Debug Logging

In your dashboard.py, enable logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Now you'll see all HTTP requests and responses
```

---

## N8N Best Practices

1. **Test Webhooks First**: Use curl or Postman before connecting Streamlit
2. **Start Simple**: Begin with just a Respond node, add complexity gradually
3. **Use Filters**: Filter alerts by confidence level or incident type
4. **Set Timeouts**: N8N nodes should complete within seconds
5. **Log Everything**: Store incidents in database for audits
6. **Error Handling**: Add error handling branches for failed operations
7. **Monitor Executions**: Regularly check execution logs for issues
8. **Test Regularly**: Periodically send test alerts to verify everything works

---

## Production Checklist

Before deploying to production:

- [ ] N8N workflow fully tested
- [ ] All automation actions working
- [ ] Error handling implemented
- [ ] Email templates configured
- [ ] Database logging enabled
- [ ] Monitoring and alerts set up
- [ ] Backup webhook URL configured (if using redundancy)
- [ ] Rate limiting configured (if needed)
- [ ] Security: webhook validation enabled
- [ ] Documentation updated

---

## Additional Resources

- **N8N Documentation**: https://docs.n8n.io/
- **Webhook Nodes**: https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base-webhook/
- **HTTP Requests**: https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base-httprequest/
- **N8N Community**: https://community.n8n.io/

---

## Support

If you encounter issues:

1. Check **N8N Execution History** for errors
2. Verify **Webhook URL** in dashboard.py matches n8n
3. Test **webhook manually** with curl
4. Check **network connectivity**
5. Review **error messages** in both Streamlit and n8n
6. Enable **debug logging** for detailed information

---

**Your n8n integration is crucial for automating campus security responses. Regular verification ensures your system stays operational!** 🛡️🔄
