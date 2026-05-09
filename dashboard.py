import io
import streamlit as st
import os
import tempfile
from datetime import datetime
from pathlib import Path
import requests  # Added for n8n webhooks
from PIL import Image
from src.rag.rag_pipeline import UniversitySafetyRAG
from src.cv_detection.anomaly_detector import CampusAnomalyDetector
from src.integrations.telegram_service import get_telegram_service

st.set_page_config(page_title="Smart University Safety System", page_icon="🛡️", layout="wide")

st.title("🛡️ Smart University Safety & Emergency System")
st.markdown("**RAG-Powered AI Agent for Campus Incident Analysis**")
st.caption("Student: Mohamed Ahmed Ibrahim | ID: 22101115")

# Initialize systems
@st.cache_resource
def get_systems():
    try:
        rag = UniversitySafetyRAG()
        cv = CampusAnomalyDetector(data_root="data/raw/ucsd")
        return rag, cv
    except Exception as e:
        st.error(f"❌ Failed to initialize core systems: {str(e)}")
        st.stop()

rag_system, cv_detector = get_systems()

# n8n Configuration
N8N_WEBHOOK_URL = "https://hash314151.app.n8n.cloud/webhook/home/rt-detection/smart-university-safety-system/src/agents/alert_agent.py"  # Update with your n8n URL
N8N_API_KEY = os.getenv("N8N_API_KEY", "")  # Optional: for authenticated webhooks

def send_alert_to_n8n(alert_data):
    """Send alert data to n8n for workflow processing."""
    try:
        headers = {"Content-Type": "application/json"}
        if N8N_API_KEY:
            headers["Authorization"] = f"Bearer {N8N_API_KEY}"
        
        response = requests.post(N8N_WEBHOOK_URL, json=alert_data, headers=headers, timeout=10)
        if response.status_code == 200:
            st.info("✅ Alert sent to n8n for email notifications")
        else:
            st.warning(f"⚠️ n8n webhook failed: {response.status_code}")
    except Exception as e:
        st.warning(f"⚠️ Failed to send to n8n: {str(e)}")

def send_alert_to_telegram(image_path, location, confidence, event_type, caption, alert_text):
    """Send alert with image to Telegram security group."""
    try:
        # Determine priority level based on confidence and event type
        event_lower = event_type.lower()
        if confidence > 0.9 or any(k in event_lower for k in ["fight", "assault", "weapon"]):
            priority = "CRITICAL"
        elif confidence > 0.7 or any(k in event_lower for k in ["fall", "medical", "injury"]):
            priority = "HIGH"
        elif confidence > 0.5:
            priority = "MEDIUM"
        else:
            priority = "LOW"
        
        telegram_service = get_telegram_service()
        
        # Truncate recommendations to fit Telegram's 1024 character limit
        # Keep only the first actionable items (most important)
        max_recommendations_length = 300
        if len(alert_text) > max_recommendations_length:
            # Extract first few sentences or lines
            lines = alert_text.split('\n')
            truncated = []
            total_length = 0
            for line in lines:
                if total_length + len(line) + 1 <= max_recommendations_length:
                    truncated.append(line)
                    total_length += len(line) + 1
                else:
                    break
            recommendations = '\n'.join(truncated)
            if total_length < len(alert_text):
                recommendations += "\n[See dashboard for full details]"
        else:
            recommendations = alert_text
        
        success = telegram_service.send_alert_with_image_sync(
            image_path=image_path,
            incident_type=event_type,
            location=location,
            confidence=confidence,
            priority=priority,
            description=caption,
            recommendations=recommendations
        )
        
        if success:
            st.success("✅ Alert with image sent to Telegram security group")
        else:
            st.warning("⚠️ Failed to send alert to Telegram (check configuration)")
    except Exception as e:
        st.warning(f"⚠️ Failed to send to Telegram: {str(e)}")

# Sidebar
with st.sidebar:
    st.header("📊 System Status")
    st.success("✅ Image/Video Input Ready")
    st.success("✅ Groq RAG Ready")
    num_docs = len([f for f in os.listdir("data/knowledge_base") if f.endswith(".txt")])
    st.info(f"Knowledge Base Documents: {num_docs}")
    
    # Add debug info
    if st.checkbox("🔍 Show Debug Info"):
        st.write("**RAG System:**", "Loaded" if rag_system else "Failed")
        st.write("**CV Detector:**", "Loaded" if cv_detector else "Failed")

st.subheader("📤 Upload Image or Video for Analysis")

st.markdown("#### 🧠 Test the expanded RAG knowledge base")
query_default = "What are the NIST guidelines for incident response?"
rag_question = st.text_input("Ask the knowledge base a safety question", value=query_default)
if st.button("🧪 Run RAG Test Query", key="rag_test"):
    with st.spinner("Querying the expanded knowledge base..."):
        try:
            rag_response = rag_system.get_safety_recommendation(rag_question)
            st.success("✅ RAG query completed")
            st.markdown(f"**Question:** {rag_question}")
            st.markdown(rag_response["result"])
        except Exception as e:
            st.error(f"❌ RAG query failed: {e}")

st.markdown("---")

uploaded_file = st.file_uploader("Upload an image for analysis", type=["png", "jpg", "jpeg", "tif", "bmp"])
if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

    location = st.selectbox("Detected Location", [
        "Building A entrance", "Library side entrance", "Main Courtyard",
        "Building C parking", "Science Lab entrance"
    ])

    if st.button("🔍 Analyze Media & Generate Alert", type="primary", use_container_width=True):
        with st.spinner("Processing image → Detecting anomalies → Generating description → Running RAG..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1] if hasattr(uploaded_file, 'name') else 'png'}") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                temp_path = tmp_file.name

            try:
                event_dict = cv_detector.process_image_and_generate_event(
                    image_path=temp_path,
                    location=location
                )

                if "description" in event_dict and event_dict["description"]:
                    incident_text = (
                        f"{event_dict['description']} "
                        f"Location: {location}. "
                        f"Time: {event_dict.get('time', '')}. "
                        f"Confidence: {event_dict['confidence']:.2f}. "
                        f"Risk level: {event_dict.get('risk_level', 'UNKNOWN')}.")
                elif "caption" in event_dict:
                    incident_text = (
                        f"{event_dict['caption']}. {event_dict['event']} at {location}. "
                        f"Confidence: {event_dict['confidence']:.2f}.")
                else:
                    incident_text = f"{event_dict['event']} at {location}. Confidence: {event_dict['confidence']:.2f}."

                result = rag_system.get_safety_recommendation(incident_text)

                alert_text = result["result"]
                confidence = event_dict["confidence"]
                caption = event_dict.get("caption", "No caption generated")

                st.session_state.last_alert = {
                    "time": datetime.now().strftime("%H:%M:%S"),
                    "location": location,
                    "confidence": confidence,
                    "caption": caption,
                    "alert_text": alert_text,
                    "processing_mode": "Uploaded Image",
                    "image_path": temp_path,
                    "event_type": event_dict.get("event", "Unknown Incident")
                }

                send_alert_to_n8n(st.session_state.last_alert)
                
                # Send alert with image to Telegram
                # Important: Do this BEFORE the finally block deletes the temp file
                send_alert_to_telegram(
                    image_path=temp_path,
                    location=location,
                    confidence=confidence,
                    event_type=event_dict.get("event", "Unknown Incident"),
                    caption=caption,
                    alert_text=alert_text
                )

            except Exception as e:
                st.error(f"❌ Processing failed: {e}")
            finally:
                # Clean up temp file safely
                try:
                    if os.path.exists(temp_path):
                        os.unlink(temp_path)
                except Exception as cleanup_error:
                    print(f"Warning: Could not delete temp file: {cleanup_error}")
                if "test_image" in st.session_state:
                    del st.session_state.test_image
else:
    st.info("Upload an image and click Analyze Media & Generate Alert to start the security review.")

# Display Alert
st.subheader("📢 AI Safety Alert & Recommended Actions")
if "last_alert" in st.session_state:
    a = st.session_state.last_alert
    st.error(f"🚨 ACTIVE ALERT at {a['location']}")
    st.markdown(f"**Time:** {a['time']} | **Confidence:** {a['confidence']:.2f} | **Mode:** {a.get('processing_mode', 'Direct Pipeline')}")
    if "caption" in a:
        st.markdown(f"**Image Description:** {a['caption']}")
    st.markdown(a["alert_text"])
else:
    st.info("Upload an image/video and click **Analyze Media & Generate Alert**")

st.markdown("---")
st.caption("Vision Input → Anomaly Description → RAG + Groq → Smart Alert • Prototype")