"""
ENHANCED Smart University Safety System - Groq-Powered Pipeline
Using the SMARTEST available Groq model: llama-3.1-70b-versatile (70B parameters)
This replaces the basic system with intelligent Groq-based analysis at every stage.
"""

from src.rag.rag_pipeline import UniversitySafetyRAG
from src.cv_detection.anomaly_detector import CampusAnomalyDetector
from src.cv_detection.groq_cv_analyzer import GroqCVAnalyzer
from datetime import datetime
import json


def run_groq_enhanced_pipeline(location="Building A entrance", anomaly_score=0.85, 
                                incident_type="fight", image_path=None, caption=None):
    """
    🚀 Enhanced Smart University Safety Pipeline with Groq Intelligence
    
    This pipeline implements:
    1. Computer Vision Detection (BLIP + CLIP)
    2. Groq-Enhanced Image Analysis
    3. RAG-based Safety Recommendations (with BGE embeddings)
    4. Groq LLM for final decision synthesis
    
    Args:
        location: Where the incident occurred
        anomaly_score: Anomaly confidence (0-1)
        incident_type: Type of incident detected
        image_path: Optional path to image for CV analysis
        caption: Optional pre-computed image caption
    
    Returns:
        Comprehensive safety alert with Groq intelligence
    """
    
    print("="*80)
    print("🛡️  GROQ-POWERED SMART UNIVERSITY SAFETY SYSTEM")
    print("Enhanced with Intelligent AI Analysis at Every Stage")
    print("="*80)
    print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # ===== STAGE 1: Computer Vision Analysis =====
    print("📸 STAGE 1: Computer Vision Analysis")
    print("-" * 80)
    
    cv_detector = CampusAnomalyDetector(data_root="data/raw/ucsd")
    groq_analyzer = GroqCVAnalyzer()
    
    # Generate CV-based event
    event = cv_detector.generate_event_description(
        anomaly_score=anomaly_score, 
        location=location
    )
    
    # If image provided, process it
    if image_path:
        print(f"\n📷 Processing image: {image_path}")
        try:
            event = cv_detector.process_image_and_generate_event(image_path, location)
        except Exception as e:
            print(f"⚠️  Image processing failed: {e}")
    
    # If caption provided, use it
    if caption:
        event['caption'] = caption
    
    print(f"\n✅ CV Analysis Complete:")
    print(f"   Event Type: {event.get('event', 'Unknown')}")
    print(f"   Risk Level: {event.get('risk_level', 'UNKNOWN')}")
    print(f"   Confidence: {event.get('confidence', 0.0)}")
    
    # ===== STAGE 2: Groq-Enhanced Image Interpretation =====
    print("\n\n🤖 STAGE 2: Groq Intelligent Image Analysis")
    print("-" * 80)
    
    caption_for_analysis = event.get('caption', event.get('description', ''))
    groq_image_analysis = groq_analyzer.analyze_image_caption(
        caption=caption_for_analysis,
        anomaly_score=anomaly_score,
        location=location
    )
    
    print(f"\n✅ Groq Image Analysis:")
    print(f"   Interpretation: {groq_image_analysis.get('interpretation', 'N/A')}")
    print(f"   Severity: {groq_image_analysis.get('severity', 'N/A')}")
    print(f"   Is Emergency: {groq_image_analysis.get('is_emergency', False)}")
    
    # Merge Groq analysis into event
    event['groq_image_analysis'] = groq_image_analysis
    
    # ===== STAGE 3: Construct Incident Report for RAG =====
    print("\n\n📝 STAGE 3: Constructing Incident Report")
    print("-" * 80)
    
    incident_text = f"""
INCIDENT REPORT - {incident_type.upper()}
Location: {location}
Time: {datetime.now().strftime('%H:%M:%S')}
Confidence Score: {anomaly_score:.2f}
Severity: {groq_image_analysis.get('severity', 'UNKNOWN')}

Description: {event.get('description', '')}

CV Assessment: {event.get('event', '')}

Concerning Behaviors Detected:
{json.dumps(groq_image_analysis.get('concerning_behaviors', []), indent=2)}

Assessment: {groq_image_analysis.get('interpretation', '')}
"""
    
    print("✅ Incident report constructed for RAG pipeline")
    
    # ===== STAGE 4: RAG-Based Safety Recommendations =====
    print("\n\n🔍 STAGE 4: RAG Knowledge Base Analysis (with Smart Embeddings)")
    print("-" * 80)
    
    rag = UniversitySafetyRAG()
    rag_result = rag.get_safety_recommendation(incident_text)
    
    # ===== STAGE 5: Event Refinement with Groq =====
    print("\n\n🎯 STAGE 5: Final Groq Intelligence Synthesis")
    print("-" * 80)
    
    refined_event = groq_analyzer.refine_event_description(event)
    
    if refined_event.get('groq_enhanced'):
        print(f"\n✅ Event Enhanced with Groq Intelligence:")
        print(f"   Summary: {refined_event.get('groq_summary', 'N/A')}")
        print(f"   Threat Level: {refined_event.get('threat_level', 'N/A')}")
        print(f"   Evidence Strength: {refined_event.get('evidence', 'N/A')}")
    
    # ===== FINAL ALERT =====
    print("\n\n" + "="*80)
    print("📢 FINAL GROQ-POWERED SAFETY ALERT")
    print("="*80)
    
    final_alert = {
        "timestamp": datetime.now().isoformat(),
        "location": location,
        "incident_type": incident_type,
        "confidence": anomaly_score,
        "severity": groq_image_analysis.get('severity', 'UNKNOWN'),
        "is_emergency": groq_image_analysis.get('is_emergency', False),
        
        "cv_analysis": {
            "event": event.get('event'),
            "risk_level": event.get('risk_level'),
            "risky_actions": event.get('risky_actions', [])
        },
        
        "groq_image_analysis": {
            "interpretation": groq_image_analysis.get('interpretation'),
            "concerning_behaviors": groq_image_analysis.get('concerning_behaviors'),
            "reasoning": groq_image_analysis.get('reasoning')
        },
        
        "rag_recommendations": rag_result.get('result', 'No recommendations available'),
        
        "refined_summary": refined_event.get('groq_summary', ''),
        "recommended_actions": refined_event.get('recommended_actions', []),
        
        "model_stack": {
            "embeddings": "BAAI/bge-small-en-v1.5 (Smart BGE model - HuggingFace authenticated)",
            "llm": "llama-3.1-70b-versatile (Groq - 70B parameters - SMARTEST AVAILABLE)",
            "cv_models": ["BLIP (image captioning)", "CLIP (anomaly detection)"]
        }
    }
    
    print("\n🚨 ALERT SUMMARY:")
    print(f"Emergency Status: {'🔴 CRITICAL' if final_alert['is_emergency'] else '🟡 ALERT'}")
    print(f"Severity: {final_alert['severity']}")
    print(f"Location: {location}")
    print(f"\nGroq Analysis:")
    print(f"  {groq_image_analysis.get('interpretation', 'N/A')}")
    
    print(f"\n📋 Recommended Actions:")
    for i, action in enumerate(refined_event.get('recommended_actions', []), 1):
        print(f"  {i}. {action}")
    
    print("\n" + "="*80)
    print("✅ Pipeline Complete | All Groq Components Activated")
    print("="*80 + "\n")
    
    return final_alert


def run_simple_groq_pipeline(location="Building A entrance", anomaly_score=0.85, incident_type="fight"):
    """Simplified pipeline using Groq for quick testing"""
    return run_groq_enhanced_pipeline(location, anomaly_score, incident_type)


if __name__ == "__main__":
    print("🚀 Starting Groq-Enhanced Smart University Safety System\n")
    
    # Demo 1: Fight scenario with high confidence
    print("\n" + "="*80)
    print("DEMO 1: Physical Altercation Detected")
    print("="*80 + "\n")
    alert1 = run_simple_groq_pipeline(
        location="Building A entrance", 
        anomaly_score=0.88, 
        incident_type="fight"
    )
    
    # Demo 2: Suspicious activity scenario
    print("\n\n" + "="*80)
    print("DEMO 2: Suspicious Behavior Detected")
    print("="*80 + "\n")
    alert2 = run_simple_groq_pipeline(
        location="Parking Lot C",
        anomaly_score=0.72,
        incident_type="suspicious_behavior"
    )
    
    print("\n✅ All demos completed!")
