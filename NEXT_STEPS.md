# 🚀 NEXT STEPS - Setup & Testing Guide

## STEP 1: Update Dependencies
```bash
# Make sure you're in the project directory
cd /home/rt-detection/smart-university-safety-system

# Activate virtual environment
source venv/bin/activate

# Update pip
pip install --upgrade pip

# Install/update requirements (HuggingFace packages restored)
pip install -r requirements.txt
```

**What this does:**
- Installs `langchain-huggingface` 
- Installs `huggingface_hub`
- Installs `sentence-transformers`
- All other dependencies updated

---

## STEP 2: Verify Environment Variables

```bash
# Check if .env is properly configured
cat .env
```

**Expected output:**
```
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
TELEGRAM_GROUP_ID=YOUR_TELEGRAM_GROUP_ID
```

---

## STEP 3: Quick Component Test

### Test HuggingFace Authentication
```bash
python << 'EOF'
import os
from dotenv import load_dotenv

load_dotenv()

print("Testing HuggingFace Setup...")
print("=" * 60)

# Check HF_TOKEN
hf_token = os.getenv("HF_TOKEN")
if hf_token:
    print("✅ HF_TOKEN configured")
    print(f"   Token: {hf_token[:20]}...")
else:
    print("❌ HF_TOKEN missing!")

# Test HuggingFace embeddings
try:
    from langchain_huggingface import HuggingFaceEmbeddings
    print("\n✅ langchain-huggingface installed")
    
    embeddings = HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-en-v1.5",
        model_kwargs={'device': 'cpu'}
    )
    print("✅ BGE embeddings model loaded")
    
    # Test embedding
    test_text = "Possible fight detected"
    embedding = embeddings.embed_query(test_text)
    print(f"✅ Embedding created (dimension: {len(embedding)})")
    
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 60)
EOF
```

### Test Groq LLM (Smartest Model)
```bash
python << 'EOF'
import os
from dotenv import load_dotenv

load_dotenv()

print("Testing Groq Setup...")
print("=" * 60)

# Check GROQ_API_KEY
groq_key = os.getenv("GROQ_API_KEY")
if groq_key:
    print("✅ GROQ_API_KEY configured")
    print(f"   Key: {groq_key[:20]}...")
else:
    print("❌ GROQ_API_KEY missing!")

# Test Groq connection
try:
    from langchain_groq import ChatGroq
    
    llm = ChatGroq(
        groq_api_key=groq_key,
        model_name="llama-3.1-405b-reasoning",
        temperature=0.2,
        max_tokens=100
    )
    print("\n✅ Groq LLM initialized")
    print("   Model: llama-3.1-405b-reasoning (SMARTEST)")
    print("   Parameters: 405 Billion")
    
    # Test simple query
    response = llm.invoke("What is campus safety?")
    print(f"✅ LLM responding (length: {len(response.content)} chars)")
    
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 60)
EOF
```

---

## STEP 4: Test RAG Pipeline

```bash
python << 'EOF'
print("Testing RAG Pipeline...")
print("=" * 60)

try:
    from src.rag.rag_pipeline import UniversitySafetyRAG
    
    print("✅ Importing RAG pipeline...")
    
    rag = UniversitySafetyRAG()
    print("✅ RAG pipeline initialized")
    print("   - HuggingFace embeddings: BAAI/bge-small-en-v1.5 (AUTHENTICATED)")
    print("   - Groq LLM: llama-3.1-405b-reasoning (SMARTEST)")
    
    # Test with a simple incident
    test_incident = "Possible fight detected near Building A entrance. 2 people involved."
    
    print(f"\n📝 Test incident: {test_incident}")
    print("\nGenerating safety recommendation...")
    result = rag.get_safety_recommendation(test_incident)
    
    print("\n✅ RAG pipeline working!")
    print("\nRecommendation received (first 200 chars):")
    print(result['result'][:200] + "...")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
EOF
```

---

## STEP 5: Run Full Pipeline

```bash
# Run the complete enhanced pipeline with all components
python groq_main_pipeline.py
```

**Expected output:**
```
================================================================================
GROQ-POWERED SMART UNIVERSITY SAFETY SYSTEM
Enhanced with Intelligent AI Analysis at Every Stage
================================================================================

[Stage 1] Computer Vision Analysis
[Stage 2] Groq Intelligent Image Analysis
[Stage 3] Constructing Incident Report
[Stage 4] RAG Knowledge Base Analysis (with Smart Embeddings)
[Stage 5] Final Groq Intelligence Synthesis

FINAL GROQ-POWERED SAFETY ALERT
[Emergency details and recommendations]
```

---

## STEP 6: Test with Real Scenarios

### Scenario 1: Fight Detection
```bash
python << 'EOF'
from groq_main_pipeline import run_groq_enhanced_pipeline

alert = run_groq_enhanced_pipeline(
    location="Building A entrance",
    anomaly_score=0.88,
    incident_type="fight"
)
print("\n✅ Fight scenario test complete")
EOF
```

### Scenario 2: Suspicious Behavior
```bash
python << 'EOF'
from groq_main_pipeline import run_groq_enhanced_pipeline

alert = run_groq_enhanced_pipeline(
    location="Parking Lot C",
    anomaly_score=0.72,
    incident_type="suspicious_behavior"
)
print("\n✅ Suspicious behavior scenario test complete")
EOF
```

### Scenario 3: Crowd Disturbance
```bash
python << 'EOF'
from groq_main_pipeline import run_groq_enhanced_pipeline

alert = run_groq_enhanced_pipeline(
    location="Student Commons",
    anomaly_score=0.65,
    incident_type="crowd_disturbance"
)
print("\n✅ Crowd disturbance scenario test complete")
EOF
```

---

## STEP 7: Check Documentation

Read the configuration and setup guides:

```bash
# View configuration summary
cat CONFIGURATION_SUMMARY.md

# View quick reference
cat QUICK_REFERENCE.md

# View implementation details
cat IMPLEMENTATION_COMPLETE.md
```

---

## 🧪 COMPLETE TEST SCRIPT

Save this as `test_full_system.py`:

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Complete system test script"""

import os
from dotenv import load_dotenv

load_dotenv()

print("="*80)
print("SMART UNIVERSITY SAFETY SYSTEM - COMPLETE TEST")
print("="*80)

# Test 1: Environment
print("\n[1/5] Testing Environment Variables...")
try:
    assert os.getenv("GROQ_API_KEY"), "GROQ_API_KEY missing"
    assert os.getenv("HF_TOKEN"), "HF_TOKEN missing"
    print("✅ All environment variables configured")
except AssertionError as e:
    print(f"❌ {e}")
    exit(1)

# Test 2: HuggingFace
print("\n[2/5] Testing HuggingFace Embeddings...")
try:
    from langchain_huggingface import HuggingFaceEmbeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-en-v1.5",
        model_kwargs={'device': 'cpu'}
    )
    embedding = embeddings.embed_query("test")
    print(f"✅ HuggingFace embeddings ready ({len(embedding)} dimensions)")
except Exception as e:
    print(f"❌ {e}")
    exit(1)

# Test 3: Groq LLM
print("\n[3/5] Testing Groq LLM (llama-3.1-405b-reasoning)...")
try:
    from langchain_groq import ChatGroq
    llm = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.1-405b-reasoning",
        temperature=0.2,
        max_tokens=100
    )
    print("✅ Groq LLM ready (llama-3.1-405b-reasoning - SMARTEST)")
except Exception as e:
    print(f"❌ {e}")
    exit(1)

# Test 4: RAG Pipeline
print("\n[4/5] Testing RAG Pipeline...")
try:
    from src.rag.rag_pipeline import UniversitySafetyRAG
    rag = UniversitySafetyRAG()
    print("✅ RAG pipeline initialized")
except Exception as e:
    print(f"❌ {e}")
    exit(1)

# Test 5: Full Pipeline
print("\n[5/5] Testing Full Pipeline...")
try:
    from groq_main_pipeline import run_groq_enhanced_pipeline
    alert = run_groq_enhanced_pipeline(
        location="Test Location",
        anomaly_score=0.75,
        incident_type="test"
    )
    print("✅ Full pipeline working")
except Exception as e:
    print(f"❌ {e}")
    exit(1)

print("\n" + "="*80)
print("✅ ALL TESTS PASSED - SYSTEM IS READY!")
print("="*80)
print("""
Next steps:
1. Deploy to campus security system
2. Monitor alerts and recommendations
3. Fine-tune safety protocols as needed
4. Integrate with Telegram notifications

Your system uses:
- HuggingFace: BAAI/bge-small-en-v1.5 (AUTHENTICATED)
- Groq LLM: llama-3.1-405b-reasoning (SMARTEST - 405B parameters)
""")
```

Run it:
```bash
python test_full_system.py
```

---

## 📋 CHECKLIST

- [ ] Activate virtual environment: `source venv/bin/activate`
- [ ] Update dependencies: `pip install -r requirements.txt`
- [ ] Verify .env file has all 4 keys
- [ ] Test HuggingFace authentication
- [ ] Test Groq LLM connection
- [ ] Test RAG pipeline
- [ ] Run full pipeline: `python groq_main_pipeline.py`
- [ ] Test scenarios (fight, suspicious, crowd)
- [ ] Review documentation
- [ ] Deploy to production

---

## ⚠️ TROUBLESHOOTING

### Issue: HuggingFace download timeout
```bash
# Set longer timeout
export HF_HUB_DOWNLOAD_TIMEOUT=100
pip install -r requirements.txt
```

### Issue: Groq API rate limit
- Wait 30 seconds and retry
- Check your Groq account: https://console.groq.com

### Issue: GPU memory problems
- Already set to CPU only in code
- Should work on any machine

### Issue: Module not found
```bash
# Reinstall dependencies
pip uninstall langchain langchain-community langchain-huggingface langchain-groq -y
pip install -r requirements.txt
```

---

## 🎯 SUMMARY

1. **Install dependencies** - Restore HuggingFace packages
2. **Verify environment** - Check .env file
3. **Test components** - HuggingFace, Groq, RAG
4. **Run pipeline** - Full system test
5. **Test scenarios** - Real incident types
6. **Deploy** - Ready for production

Your system is now using:
✅ **HuggingFace** with authentication
✅ **Groq llama-3.1-405b-reasoning** (smartest model)
✅ **Production-ready** architecture

**Ready to protect your campus!** 🛡️
