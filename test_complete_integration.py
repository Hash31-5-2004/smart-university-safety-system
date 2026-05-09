#!/usr/bin/env python3
"""
Complete Integration Test
Tests Streamlit dashboard with Telegram image alerts and N8N
"""

import os
import sys
import tempfile
from pathlib import Path
from dotenv import load_dotenv
from PIL import Image
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.integrations.telegram_service import get_telegram_service
from src.rag.rag_pipeline import UniversitySafetyRAG
from src.cv_detection.anomaly_detector import CampusAnomalyDetector


def create_test_image(width=640, height=480, image_type="normal"):
    """Create a test image for analysis."""
    
    # Create numpy array for image
    if image_type == "normal":
        # Create a normal scene
        img_array = np.random.randint(100, 150, (height, width, 3), dtype=np.uint8)
    elif image_type == "anomaly":
        # Create an image with some anomalies
        img_array = np.random.randint(100, 150, (height, width, 3), dtype=np.uint8)
        # Add some "unusual" patterns
        img_array[100:200, 200:300, :] = [50, 50, 50]  # Dark spot
        img_array[250:350, 100:200, :] = [255, 0, 0]    # Red area
    else:
        img_array = np.ones((height, width, 3), dtype=np.uint8) * 128
    
    # Convert to PIL Image
    img = Image.fromarray(img_array)
    
    # Save to temp file
    temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
    img.save(temp_file.name)
    
    return temp_file.name


def test_telegram_service():
    """Test Telegram service."""
    print("\n" + "="*70)
    print("🤖 TESTING TELEGRAM SERVICE")
    print("="*70)
    
    try:
        service = get_telegram_service()
        print("✅ Telegram service initialized")
        
        # Create test image
        test_image = create_test_image(image_type="normal")
        print(f"✅ Test image created: {test_image}")
        
        # Test alert with image
        print("\n📤 Sending test alert with image...")
        success = service.send_alert_with_image_sync(
            image_path=test_image,
            incident_type="Integration Test",
            location="Testing Lab",
            confidence=0.85,
            priority="MEDIUM",
            description="This is a comprehensive integration test alert",
            recommendations="Verify image appears correctly in Telegram group"
        )
        
        if success:
            print("✅ Alert with image sent successfully to Telegram!")
            return True
        else:
            print("❌ Failed to send alert with image")
            return False
            
    except Exception as e:
        print(f"❌ Telegram test failed: {str(e)}")
        return False
    finally:
        # Cleanup
        try:
            os.unlink(test_image)
        except:
            pass


def test_rag_system():
    """Test RAG system."""
    print("\n" + "="*70)
    print("📚 TESTING RAG SYSTEM")
    print("="*70)
    
    try:
        print("Loading RAG system...")
        rag = UniversitySafetyRAG()
        print("✅ RAG system loaded")
        
        test_query = "What should security do if there's an unauthorized person in a restricted area?"
        print(f"\n🔍 Testing query: {test_query}")
        
        result = rag.get_safety_recommendation(test_query)
        
        if result and "result" in result:
            print("✅ RAG query successful")
            print(f"\n📖 Response preview:")
            response_text = result["result"]
            preview = response_text[:200] + "..." if len(response_text) > 200 else response_text
            print(preview)
            return True
        else:
            print("❌ RAG query failed")
            return False
            
    except Exception as e:
        print(f"❌ RAG test failed: {str(e)}")
        return False


def test_cv_detector():
    """Test CV detector."""
    print("\n" + "="*70)
    print("🎯 TESTING COMPUTER VISION DETECTOR")
    print("="*70)
    
    try:
        print("Loading CV detector...")
        cv = CampusAnomalyDetector(data_root="data/raw/ucsd")
        print("✅ CV detector loaded")
        
        # Create test image
        test_image = create_test_image(image_type="anomaly")
        print(f"✅ Test image created: {test_image}")
        
        # Process image
        print("\n🔍 Processing image for anomalies...")
        result = cv.process_image_and_generate_event(
            image_path=test_image,
            location="Testing Area"
        )
        
        if result:
            print("✅ Image processed successfully")
            print(f"   Event: {result.get('event', 'N/A')}")
            print(f"   Confidence: {result.get('confidence', 'N/A'):.2f}")
            print(f"   Caption: {result.get('caption', 'N/A')}")
            return True
        else:
            print("❌ Image processing failed")
            return False
            
    except Exception as e:
        print(f"❌ CV test failed: {str(e)}")
        return False
    finally:
        try:
            os.unlink(test_image)
        except:
            pass


def test_complete_workflow():
    """Test complete workflow: image → CV → RAG → Telegram."""
    print("\n" + "="*70)
    print("🔄 TESTING COMPLETE WORKFLOW")
    print("="*70)
    
    try:
        print("1️⃣  Creating test image...")
        test_image = create_test_image(image_type="anomaly")
        
        print("2️⃣  Loading CV detector...")
        cv = CampusAnomalyDetector(data_root="data/raw/ucsd")
        
        print("3️⃣  Analyzing image with CV...")
        cv_result = cv.process_image_and_generate_event(
            image_path=test_image,
            location="Integration Test Lab"
        )
        
        if not cv_result:
            print("❌ CV analysis failed")
            return False
        
        print(f"   ✅ Detected: {cv_result.get('event')}")
        
        print("4️⃣  Loading RAG system...")
        rag = UniversitySafetyRAG()
        
        # Create incident query
        incident_text = (
            f"{cv_result.get('caption', 'Anomaly detected')}. "
            f"{cv_result.get('event')} at Integration Test Lab. "
            f"Confidence: {cv_result.get('confidence', 0):.2f}."
        )
        
        print("5️⃣  Querying RAG for recommendations...")
        rag_result = rag.get_safety_recommendation(incident_text)
        
        if not rag_result:
            print("❌ RAG query failed")
            return False
        
        print("   ✅ Recommendations received")
        
        print("6️⃣  Sending alert to Telegram with image...")
        telegram_service = get_telegram_service()
        
        success = telegram_service.send_alert_with_image_sync(
            image_path=test_image,
            incident_type=cv_result.get('event', 'Anomaly Detected'),
            location="Integration Test Lab",
            confidence=cv_result.get('confidence', 0.5),
            priority="MEDIUM",
            description=cv_result.get('caption', ''),
            recommendations=rag_result.get('result', '')[:500]  # First 500 chars
        )
        
        if success:
            print("   ✅ Alert sent to Telegram with image!")
            print("\n🎉 Complete workflow successful!")
            return True
        else:
            print("❌ Failed to send Telegram alert")
            return False
            
    except Exception as e:
        print(f"❌ Complete workflow test failed: {str(e)}")
        return False
    finally:
        try:
            os.unlink(test_image)
        except:
            pass


def test_n8n_webhook():
    """Test N8N webhook connectivity."""
    print("\n" + "="*70)
    print("🔗 TESTING N8N WEBHOOK")
    print("="*70)
    
    try:
        import requests
        
        webhook_url = "https://hash3040531.app.n8n.cloud/webhook-test/home/rt-detection/smart-university-safety-system/src/agents/alert_agent.py"
        
        print(f"Testing webhook: {webhook_url[:50]}...")
        
        test_payload = {
            "time": "14:23:45",
            "location": "Integration Test",
            "confidence": 0.85,
            "caption": "Test alert from integration test",
            "alert_text": "This is a test alert",
            "processing_mode": "Integration Test"
        }
        
        response = requests.post(webhook_url, json=test_payload, timeout=10)
        
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ N8N webhook is accessible and responding")
            return True
        else:
            print(f"⚠️  N8N returned status {response.status_code}")
            print(f"   This may indicate a configuration issue")
            print(f"   Check N8N_VERIFICATION.md for setup instructions")
            return False
            
    except Exception as e:
        print(f"⚠️  Could not connect to N8N webhook: {str(e)}")
        print("   This is OK if N8N is not yet configured")
        print("   See N8N_VERIFICATION.md for setup instructions")
        return False


def main():
    """Run all tests."""
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*15 + "COMPLETE INTEGRATION TEST SUITE" + " "*21 + "║")
    print("╚" + "="*68 + "╝")
    
    load_dotenv()
    
    results = {}
    
    # Run tests
    results["Telegram Service"] = test_telegram_service()
    results["RAG System"] = test_rag_system()
    results["CV Detector"] = test_cv_detector()
    results["Complete Workflow"] = test_complete_workflow()
    results["N8N Webhook"] = test_n8n_webhook()
    
    # Summary
    print("\n" + "="*70)
    print("📊 TEST SUMMARY")
    print("="*70)
    
    passed = 0
    failed = 0
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print("="*70)
    print(f"Results: {passed} passed, {failed} failed out of {len(results)} tests")
    
    if passed == len(results):
        print("\n🎉 All tests passed! Your system is fully integrated.")
    else:
        print(f"\n⚠️  {failed} test(s) failed. Check output above for details.")
    
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
