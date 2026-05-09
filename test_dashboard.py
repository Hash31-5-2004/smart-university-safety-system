#!/usr/bin/env python3
"""
Test script for the updated dashboard functionality
"""
import os
import sys
sys.path.append('src')

from dotenv import load_dotenv
from src.rag.rag_pipeline import UniversitySafetyRAG
from src.agents.multi_agent_system import MultiAgentSafetySystem

load_dotenv()

def test_rag_query():
    """Test the RAG query functionality"""
    print("🧪 Testing RAG Query Functionality...")
    rag_system = UniversitySafetyRAG()

    test_questions = [
        "What are the NIST guidelines for incident response?",
        "How should access control be implemented according to NIST?"
    ]

    for question in test_questions:
        print(f"\n❓ Testing: {question}")
        try:
            result = rag_system.get_safety_recommendation(question)
            print("✅ RAG query successful")
            print(f"Response preview: {result['result'][:100]}...")
        except Exception as e:
            print(f"❌ RAG query failed: {e}")

def test_multi_agent_system():
    """Test the multi-agent system initialization"""
    print("\n🤖 Testing Multi-Agent System...")
    try:
        system = MultiAgentSafetySystem()
        print("✅ Multi-agent system initialized successfully")

        # Test system status
        status = system.get_system_status()
        print(f"System status: {status['status']}")
        print(f"Agents: {len(status['agents'])} configured")

    except Exception as e:
        print(f"❌ Multi-agent system failed: {e}")

def test_dashboard_components():
    """Test dashboard-specific components"""
    print("\n📊 Testing Dashboard Components...")

    # Test knowledge base document count
    try:
        knowledge_base_path = "data/knowledge_base"
        if os.path.exists(knowledge_base_path):
            txt_files = [f for f in os.listdir(knowledge_base_path) if f.endswith(".txt")]
            print(f"✅ Knowledge base contains {len(txt_files)} documents")
            print("Documents:", txt_files[:5], "..." if len(txt_files) > 5 else "")
        else:
            print("❌ Knowledge base directory not found")
    except Exception as e:
        print(f"❌ Knowledge base check failed: {e}")

    # Test FAISS index
    try:
        index_path = "data/processed/faiss_index"
        if os.path.exists(index_path):
            print("✅ FAISS vector index exists")
        else:
            print("❌ FAISS index not found")
    except Exception as e:
        print(f"❌ FAISS index check failed: {e}")

if __name__ == "__main__":
    print("🚀 Testing Updated Dashboard Functionality")
    print("=" * 50)

    test_rag_query()
    test_multi_agent_system()
    test_dashboard_components()

    print("\n" + "=" * 50)
    print("🎉 Dashboard testing completed!")
    print("\n📋 Dashboard should now include:")
    print("  • RAG knowledge base query section")
    print("  • Multi-agent system toggle")
    print("  • Enhanced processing with NIST guidelines")
    print("  • Document count display")
    print("\n🌐 Dashboard running at: http://localhost:8501")