#!/usr/bin/env python3
"""
Test script for the Smart University Safety System
Tests the complete pipeline with a sample image from the UCSD dataset
"""

from src.cv_detection.anomaly_detector import CampusAnomalyDetector
from src.rag.rag_pipeline import UniversitySafetyRAG
import os

def test_full_pipeline():
    """Test the complete CV + RAG pipeline with a dataset image"""
    print("🧪 TESTING SMART UNIVERSITY SAFETY SYSTEM")
    print("=" * 60)

    # Initialize systems
    print("🔧 Initializing systems...")
    cv_detector = CampusAnomalyDetector()
    rag_system = UniversitySafetyRAG()
    print("✅ Systems ready\n")

    # Test image
    test_image = "test_image.png"
    location = "Building A entrance"

    if not os.path.exists(test_image):
        print(f"❌ Test image not found: {test_image}")
        print("Please run: cp data/raw/ucsd/UCSD_Anomaly_Dataset.v1p2/UCSDped1/Train/Train001/001.tif test_image.tif")
        print("Then: python3 -c \"from PIL import Image; Image.open('test_image.tif').save('test_image.png', 'PNG')\"")
        return

    print(f"📸 Testing with image: {test_image}")
    print(f"📍 Location: {location}")
    print("-" * 40)

    # Step 1: Process image with CV system
    print("🤖 Step 1: Computer Vision Analysis")
    event_dict = cv_detector.process_image_and_generate_event(test_image, location)

    print(f"   📝 Caption: {event_dict.get('caption', 'No caption')}")
    print(f"   🎯 Event: {event_dict['event']}")
    print(f"   📊 Confidence: {event_dict['confidence']:.3f}")
    print(f"   📍 Location: {event_dict['location']}")
    print()

    # Step 2: Create incident description for RAG
    print("📋 Step 2: Creating Incident Description")
    if "caption" in event_dict:
        incident_text = f"{event_dict['caption']}. {event_dict['event']} at {location}. Confidence: {event_dict['confidence']}"
    else:
        incident_text = f"{event_dict['event']} at {location}. Confidence: {event_dict['confidence']}"

    print(f"   📄 Description: {incident_text}")
    print()

    # Step 3: Get RAG safety recommendations
    print("🧠 Step 3: AI Safety Analysis & Recommendations")
    result = rag_system.get_safety_recommendation(incident_text)

    print("🚨 AI-GENERATED SAFETY ALERT:")
    print("=" * 60)
    print(result['result'])
    print("=" * 60)

    print("\n✅ Pipeline test completed successfully!")
    return event_dict, result

if __name__ == "__main__":
    test_full_pipeline()