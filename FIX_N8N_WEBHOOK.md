# 🔧 Fix N8N Webhook 404 Error - Quick Guide

## 🚨 **THE PROBLEM**

Your current webhook URL in `dashboard.py` is **WRONG**:
```python
# ❌ CURRENT (WRONG)
N8N_WEBHOOK_URL = "https://hash314151.app.n8n.cloud/webhook-test/home/rt-detection/smart-university-safety-system/src/agents/alert_agent.py"
```

**Why it's wrong:**
- ❌ Has `/webhook-test/` instead of `/webhook/`
- ❌ Contains file system paths (`/home/rt-detection/...`)
- ❌ This format causes **404 Not Found** errors

---

## ✅ **THE SOLUTION (3 Simple Steps)**

### **Step 1️⃣: Get the Correct URL from N8N**

1. Go to https://app.n8n.cloud
2. Open your workflow (e.g., "Security Alert Emails")
3. **Click the "Webhook" node** (the very first node)
4. Look at the **right panel**
5. Find the field labeled **"Webhook URL"**
6. **Copy the entire URL** from that field

**It should look like this (simple and short):**
```
✅ https://hash314151.app.n8n.cloud/webhook/security-alert-emails
✅ https://hash314151.app.n8n.cloud/webhook/campus-safety
✅ https://hash314151.app.n8n.cloud/webhook/incident-alerts
```

### **Step 2️⃣: Update dashboard.py**

Open `dashboard.py` and find line ~30:

```python
# OLD (DELETE THIS):
N8N_WEBHOOK_URL = "https://hash314151.app.n8n.cloud/webhook-test/home/rt-detection/smart-university-safety-system/src/agents/alert_agent.py"

# NEW (PASTE YOUR URL HERE):
N8N_WEBHOOK_URL = "https://hash314151.app.n8n.cloud/webhook/YOUR_WEBHOOK_NAME"
```

Replace `YOUR_WEBHOOK_NAME` with whatever appears in your N8N webhook node.

### **Step 3️⃣: Test It**

#### **Option A: Quick Test with Python Script**
```bash
python diagnose_n8n_webhook.py "https://hash314151.app.n8n.cloud/webhook/security-alert-emails"
```

Replace the URL with your actual webhook URL from Step 1.

#### **Option B: Test with curl**
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"test":"data"}' \
  "https://hash314151.app.n8n.cloud/webhook/security-alert-emails"
```

#### **Option C: Test with Streamlit**
```bash
streamlit run dashboard.py
```

Upload an image and watch:
- ✅ Telegram alert should work (already working)
- ✅ N8N alert should work (after fixing URL)

---

## 📸 **N8N Webhook Node Screenshot Reference**

When you click on the Webhook node in N8N, you should see:

```
┌─────────────────────────────────┐
│      Webhook Node Settings      │
├─────────────────────────────────┤
│ HTTP Method: POST               │
│ Test URL:                       │
│ https://hash314151.app.n8n...   │ ← COPY THIS!
│ Webhook URL:                    │
│ https://hash314151.app.n8n...   │ ← OR THIS!
│                                 │
│ [Copy] button                   │
└─────────────────────────────────┘
```

**Copy either "Test URL" or "Webhook URL"** - they should be the same format.

---

## ✨ **After You Fix It**

Once you update the URL and restart Streamlit:

1. Upload an image to the dashboard
2. You should see:
   - ✅ CV Analysis (anomaly detected)
   - ✅ RAG Recommendations (safety tips)
   - ✅ Telegram Alert (image + caption sent to group)
   - ✅ N8N Webhook (data sent to workflow)

---

## 🆘 **Still Getting 404?**

### **Common Fixes:**

1. **Make sure N8N workflow is "Published"**
   - Look for green "Published" indicator

2. **Make sure N8N workflow is "Active"**
   - Toggle it off and on if needed

3. **Copy URL exactly** (with no extra spaces)
   - Don't manually type it - use copy button

4. **Use the correct HTTP method**
   - Should be **POST** (not GET)

5. **Check your webhook name**
   - Your URL might be:
     - `/webhook/security-alerts`
     - `/webhook/campus-safety` 
     - `/webhook/incident-alerts`
   - (depends on what you named it in N8N)

---

## 📝 **Quick Checklist**

- [ ] Opened N8N workflow
- [ ] Clicked Webhook node
- [ ] Copied Webhook URL from right panel
- [ ] Updated N8N_WEBHOOK_URL in dashboard.py
- [ ] Saved dashboard.py
- [ ] Restarted Streamlit (`streamlit run dashboard.py`)
- [ ] Tested with an image upload
- [ ] Got 200 response (not 404)

---

## 🎯 **Expected N8N Webhook URL Format**

| Component | Current ❌ | Correct ✅ |
|-----------|-----------|----------|
| Protocol | `https://` | `https://` |
| Host | `hash314151` | `hash314151` |
| Domain | `app.n8n.cloud` | `app.n8n.cloud` |
| Path | `/webhook-test/home/...` | `/webhook/security-alerts` |

**Key difference:** Simple path like `/webhook/name` NOT `/webhook-test/file/paths`

---

## 💡 **Why This Happened**

The original URL was likely:
- A test webhook URL that got corrupted
- Or file paths accidentally concatenated to the webhook URL
- Or an old format from a different N8N version

N8N webhook URLs are **always short and simple** - they only contain the webhook name, not file paths.

