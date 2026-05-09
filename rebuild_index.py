#!/usr/bin/env python3
"""
Script to rebuild the FAISS index with updated knowledge base
"""
import sys
import os
sys.path.append('src')

from rag.rag_pipeline import UniversitySafetyRAG

def rebuild_index():
    print("🔄 Rebuilding FAISS index with updated knowledge base...")

    # Initialize RAG system
    rag = UniversitySafetyRAG()

    # Force rebuild by calling load_vectorstore (since index doesn't exist)
    rag.load_vectorstore()

    print("✅ FAISS index rebuilt successfully!")
    print("📊 Knowledge base now includes NIST security guidelines alongside campus safety protocols")

    # Test the enhanced system
    test_query(rag)

def test_query(rag):
    print("\n🧪 Testing enhanced RAG system...")
    test_questions = [
        "What are the NIST guidelines for incident response?",
        "How should access control be implemented according to NIST?",
        "What contingency planning measures are recommended?"
    ]

    for question in test_questions:
        print(f"\n❓ Question: {question}")
        try:
            response = rag.get_safety_recommendation(question)
            print(f"🤖 Response: {response[:200]}..." if len(response) > 200 else f"🤖 Response: {response}")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    rebuild_index()