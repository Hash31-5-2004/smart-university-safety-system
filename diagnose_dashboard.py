#!/usr/bin/env python3
"""
Diagnostic script to verify Streamlit dashboard setup
Tests all components individually before running the full dashboard
"""

import os
import sys
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

load_dotenv()


def check_environment():
    """Check environment variables."""
    print("\n" + "="*70)
    print("🔧 CHECKING ENVIRONMENT VARIABLES")
    print("="*70)
    
    required_vars = {
        "TELEGRAM_BOT_TOKEN": "Telegram bot token",
        "TELEGRAM_GROUP_ID": "Telegram group ID",
        "GROQ_API_KEY": "Groq LLM API key"
    }
    
    all_set = True
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value:
            masked = value[:10] + "..." if len(value) > 13 else "***"
            print(f"✅ {var}: {masked}")
        else:
            print(f"❌ {var}: NOT SET")
            all_set = False
    
    return all_set


def check_dependencies():
    """Check if all required packages are installed."""
    print("\n" + "="*70)
    print("📦 CHECKING DEPENDENCIES")
    print("="*70)
    
    required_packages = {
        "streamlit": "Streamlit",
        "telegram": "Python Telegram Bot",
        "PIL": "Pillow",
        "torch": "PyTorch",
        "transformers": "Transformers",
        "langchain": "LangChain",
        "faiss": "FAISS",
        "groq": "Groq SDK"
    }
    
    all_installed = True
    for package, name in required_packages.items():
        try:
            __import__(package)
            print(f"✅ {name}")
        except ImportError:
            print(f"❌ {name} - NOT INSTALLED")
            all_installed = False
    
    return all_installed


def check_telegram():
    """Check Telegram service."""
    print("\n" + "="*70)
    print("🤖 CHECKING TELEGRAM SERVICE")
    print("="*70)
    
    try:
        from src.integrations.telegram_service import get_telegram_service
        service = get_telegram_service()
        print("✅ Telegram service initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Telegram service failed: {str(e)}")
        return False


def check_cv_detector():
    """Check CV detector."""
    print("\n" + "="*70)
    print("🎯 CHECKING COMPUTER VISION DETECTOR")
    print("="*70)
    
    try:
        from src.cv_detection.anomaly_detector import CampusAnomalyDetector
        print("Loading CV detector (this may take a moment)...")
        cv = CampusAnomalyDetector(data_root="data/raw/ucsd")
        print("✅ CV detector initialized successfully")
        return True
    except Exception as e:
        print(f"❌ CV detector failed: {str(e)}")
        return False


def check_rag_system():
    """Check RAG system."""
    print("\n" + "="*70)
    print("📚 CHECKING RAG SYSTEM")
    print("="*70)
    
    try:
        from src.rag.rag_pipeline import UniversitySafetyRAG
        print("Loading RAG system (this may take a moment)...")
        rag = UniversitySafetyRAG()
        print("✅ RAG system initialized successfully")
        return True
    except Exception as e:
        print(f"❌ RAG system failed: {str(e)}")
        return False


def check_n8n_webhook():
    """Check N8N webhook URL format."""
    print("\n" + "="*70)
    print("🔗 CHECKING N8N WEBHOOK URL")
    print("="*70)
    
    # Read from dashboard.py to check URL
    try:
        with open("dashboard.py", "r") as f:
            content = f.read()
            if "N8N_WEBHOOK_URL" in content:
                # Extract the URL
                import re
                match = re.search(r'N8N_WEBHOOK_URL\s*=\s*"([^"]+)"', content)
                if match:
                    url = match.group(1)
                    print(f"Found N8N URL: {url[:50]}...")
                    
                    if url.startswith("https://"):
                        print("✅ URL starts with https:// (correct)")
                    elif url.startswith("hhttps://"):
                        print("❌ URL has typo: hhttps:// (should be https://)")
                        return False
                    elif url.startswith("http://"):
                        print("⚠️  URL uses http:// (should be https://)")
                    else:
                        print("❌ URL format is invalid")
                        return False
                    
                    return True
    except Exception as e:
        print(f"⚠️  Could not check URL: {str(e)}")
    
    return None


def main():
    """Run all checks."""
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*18 + "DASHBOARD DIAGNOSTIC CHECK" + " "*24 + "║")
    print("╚" + "="*68 + "╝")
    
    results = {}
    
    # Run checks
    results["Environment Variables"] = check_environment()
    results["Dependencies"] = check_dependencies()
    results["N8N Webhook URL"] = check_n8n_webhook()
    
    # Only check services if dependencies are OK
    if results["Dependencies"]:
        results["Telegram Service"] = check_telegram()
        results["CV Detector"] = check_cv_detector()
        results["RAG System"] = check_rag_system()
    else:
        print("\n⚠️  Skipping service checks due to missing dependencies")
    
    # Summary
    print("\n" + "="*70)
    print("📊 DIAGNOSTIC SUMMARY")
    print("="*70)
    
    for check_name, result in results.items():
        if result is True:
            status = "✅ OK"
        elif result is False:
            status = "❌ FAILED"
        else:
            status = "⚠️  SKIPPED"
        print(f"{check_name}: {status}")
    
    print("="*70)
    
    # Recommendations
    print("\n💡 RECOMMENDATIONS:")
    
    if not results.get("Environment Variables", False):
        print("  1. Set up your .env file with required variables:")
        print("     cp .env.example .env")
        print("     # Edit .env and add your credentials")
    
    if not results.get("Dependencies", False):
        print("  2. Install missing dependencies:")
        print("     pip install -r requirements.txt")
    
    if results.get("N8N Webhook URL") == False:
        print("  3. Fix the N8N URL typo in dashboard.py (hhttps → https)")
    
    if results.get("Telegram Service") == False:
        print("  4. Check your Telegram configuration in .env")
    
    if not results.get("CV Detector", False):
        print("  5. Verify data/raw/ucsd/ directory exists with UCSD dataset")
    
    if not results.get("RAG System", False):
        print("  6. Verify data/knowledge_base/ has .txt files")
    
    print("\n" + "="*70)
    
    # Check if ready to run dashboard
    if all(v for v in results.values() if v is not None and v is not None):
        print("✅ All checks passed! Ready to run:")
        print("   streamlit run dashboard.py")
    else:
        failed = [k for k, v in results.items() if v == False]
        if failed:
            print(f"❌ {len(failed)} check(s) failed: {', '.join(failed)}")
            print("   Fix the issues above before running the dashboard")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
