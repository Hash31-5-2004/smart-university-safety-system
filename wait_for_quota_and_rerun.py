#!/usr/bin/env python3
"""
Groq Quota Reset Monitor & Auto-Runner
Monitors for quota reset and automatically runs Stage 2 evaluation with 70B model
"""

import time
import sys
import subprocess
from datetime import datetime
from pathlib import Path

def run_stage2_evaluation():
    """Run comprehensive evaluation with 70B model"""
    print("\n" + "="*80)
    print("🚀 RUNNING COMPREHENSIVE EVALUATION WITH 70B MODEL")
    print("="*80)
    print(f"⏰ Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("📍 Model: llama-3.3-70b-versatile (for superior accuracy)")
    print("="*80 + "\n")
    
    try:
        result = subprocess.run(
            [sys.executable, "comprehensive_evaluation_suite.py"],
            cwd=Path(__file__).parent,
            capture_output=False
        )
        
        if result.returncode == 0:
            print("\n" + "="*80)
            print("✅ EVALUATION COMPLETED SUCCESSFULLY")
            print("="*80)
            print("📊 Results saved to: performance_results/")
            print("\nExpected improvements:")
            print("  • Stage 2 Response Accuracy: 58% → 75%+ (better model)")
            print("  • Stage 2 Query Latency: 6.7s (longer but more accurate)")
            print("  • Overall Score: 15/18 (83%) → 16-17/18 (89-94%)")
            print("="*80 + "\n")
            return True
        else:
            print("\n❌ Evaluation failed with exit code:", result.returncode)
            return False
            
    except Exception as e:
        print(f"\n❌ Error running evaluation: {str(e)}")
        return False


def check_quota_available():
    """
    Quick check if Groq quota is available
    Returns True if we can make API calls, False if rate limited
    """
    print("\n🔍 Checking Groq API quota availability...")
    
    try:
        # Try a simple import to test API connectivity
        from src.rag.rag_pipeline import UniversitySafetyRAG
        
        rag = UniversitySafetyRAG()
        
        # Try a single quick query to test if quota is available
        test_query = "Campus safety protocol"
        response = rag.rag.llm.invoke(test_query)
        
        print("✅ Quota available! API is responding.")
        return True
        
    except Exception as e:
        error_str = str(e)
        if "429" in error_str or "rate_limit" in error_str:
            print("⏳ Rate limit still active - quota not yet reset")
            return False
        else:
            # Other error, but quota might still be available
            print(f"⚠️  Error checking quota: {error_str[:100]}")
            return False


def wait_for_quota_reset(check_interval=60, max_wait=3600):
    """
    Wait for Groq quota to reset
    check_interval: seconds between checks (default 60)
    max_wait: maximum seconds to wait (default 1 hour)
    """
    print("\n" + "="*80)
    print("⏳ GROQ QUOTA RESET MONITOR")
    print("="*80)
    print(f"📍 Checking every {check_interval} seconds")
    print(f"⏰ Max wait: {max_wait/60:.0f} minutes")
    print("="*80)
    
    start_time = time.time()
    check_count = 0
    
    while True:
        elapsed = time.time() - start_time
        check_count += 1
        
        print(f"\n[Check #{check_count}] {datetime.now().strftime('%H:%M:%S')} - Elapsed: {elapsed/60:.1f}min")
        
        if check_quota_available():
            print("\n" + "🎉 "*20)
            print("✅ QUOTA RESET DETECTED!")
            print("🎉 "*20)
            return True
        
        if elapsed > max_wait:
            print(f"\n⏰ Max wait time ({max_wait/60:.0f}min) exceeded")
            print("Manual check needed or try again later")
            return False
        
        print(f"⏳ Waiting {check_interval}s before next check...")
        time.sleep(check_interval)


def main():
    """Main execution"""
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*78 + "║")
    print("║" + "  ⏳ GROQ QUOTA RESET MONITOR - AUTO RUNNER".center(78) + "║")
    print("║" + " "*78 + "║")
    print("╚" + "="*78 + "╝")
    
    print(f"\n📊 Current Status:")
    print(f"   Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print(f"   Model: llama-3.3-70b-versatile (switched back)")
    print(f"   Goal: Re-run Stage 2 with full accuracy")
    
    # Check if quota is already available
    print("\n🔍 Initial quota check...")
    if check_quota_available():
        print("✅ Quota is available RIGHT NOW!")
        if wait_for_quota_reset(check_interval=5, max_wait=60):
            return run_stage2_evaluation()
    else:
        print("⏳ Quota not yet reset, will monitor...")
        if wait_for_quota_reset():
            return run_stage2_evaluation()
        else:
            print("\n⚠️  Timeout waiting for quota reset")
            print("You can manually run when quota resets:")
            print("  python comprehensive_evaluation_suite.py")
            return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
