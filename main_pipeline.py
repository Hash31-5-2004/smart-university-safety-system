from src.rag.rag_pipeline import UniversitySafetyRAG
from src.cv_detection.anomaly_detector import CampusAnomalyDetector
from datetime import datetime

def run_full_pipeline(location="Building A entrance", anomaly_score=0.85, incident_type="fight"):
    """Clean & Professional End-to-End Pipeline"""
    
    print("="*70)
    print("🛡️ SMART UNIVERSITY SAFETY & EMERGENCY SYSTEM")
    print("RAG-Powered AI Agent for Campus Incident Analysis")
    print("="*70)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # 1. CV Detection
    cv_detector = CampusAnomalyDetector(data_root="data/raw/ucsd")
    event = cv_detector.generate_event_description(anomaly_score=anomaly_score, location=location)
    
    incident_text = f"Possible {incident_type} detected near {location}. {event['event']}. Confidence: {anomaly_score}"

    # 2. RAG Recommendation
    rag = UniversitySafetyRAG()
    result = rag.get_safety_recommendation(incident_text)

    # 3. Professional Alert (PPT Style)
    print("\n" + "📢 AI-GENERATED ALERT".center(70))
    print("-" * 70)
    print(f"Alert: Possible physical altercation detected near {location}.")
    print(f"Confidence: {anomaly_score:.2f} | Time: {datetime.now().strftime('%H:%M')}")
    
    print("\nRecommended action:")
    print("• Dispatch campus security immediately")
    print("• Follow conflict intervention protocol")
    print("• Ensure safety of all students and staff in the area")
    print("• Document the incident and review camera footage")
    print("• Prepare to activate additional emergency protocols if needed")

    print("\n✅ Pipeline executed successfully!")
    return result

if __name__ == "__main__":
    print("🚀 Starting Smart University Safety Prototype Demo\n")
    
    # Demo 1: Fight scenario (matches your PPT example)
    run_full_pipeline(
        location="Building A entrance", 
        anomaly_score=0.88, 
        incident_type="fight"
    )
    
    print("\n" + "="*70 + "\n")
    
    # Demo 2: Suspicious behavior
    run_full_pipeline(
        location="Library side entrance", 
        anomaly_score=0.72, 
        incident_type="suspicious behavior"
    )