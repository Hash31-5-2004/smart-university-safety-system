# Performance Evaluation - Quick Start Guide

## 📊 How to Evaluate Your System

### Option 1: Run Full Evaluation (Recommended)
```bash
# Activate your environment
source venv/bin/activate

# Run comprehensive evaluation
python evaluate_performance.py

# Results saved to: performance_results/performance_report_YYYYMMDD_HHMMSS.json
```
**Time**: ~10-15 minutes  
**What it tests**: CV, RAG, Agent system, and full pipeline  
**Output**: JSON report with all metrics

---

### Option 2: Quick Benchmark (Fast Test)
```bash
python metrics_tracker.py
```
**Time**: ~2-3 minutes  
**What it tests**: Quick performance snapshot  
**Output**: Console metrics + CSV export

---

### Option 3: Continuous Monitoring (Production)
```bash
# In your main application loop, add:
from metrics_tracker import MetricsTracker

tracker = MetricsTracker()

# Log metrics after each operation:
tracker.log_cv_metrics(fps=25, avg_latency=0.04, memory_gb=1.5)
tracker.log_incident(
    incident_type="fight",
    confidence=0.85,
    response_time=4.2,
    location="Building A"
)

# Generate periodic reports:
tracker.generate_report(hours=24)  # Daily summary
tracker.export_metrics()  # Export for analysis
```

---

## 🎯 Evaluation Checklist

### Before Running Tests
- [ ] Ensure all dependencies are installed: `pip install -r requirements.txt`
- [ ] Check that GROQ_API_KEY is set in .env
- [ ] Verify UCSD dataset is downloaded in `data/raw/ucsd/`
- [ ] Ensure Telegram bot token configured (if testing integration)

### During Tests
- Monitor system resources:
  ```bash
  # In another terminal
  watch -n 1 'free -h && nvidia-smi'  # GPU memory
  # OR
  watch -n 1 'free -h && top -b -n 1 | head -20'  # CPU memory
  ```

### After Tests
- [ ] Review `performance_results/performance_report_*.json`
- [ ] Check if metrics meet targets (see table below)
- [ ] Compare with previous runs (look for trends)
- [ ] Identify bottlenecks

---

## 📈 Key Performance Targets

| Component | Metric | Target | Critical |
|-----------|--------|--------|----------|
| **CV Module** | FPS | 20+ | >15 |
| | Latency | <40ms | <100ms |
| | Memory | <2GB | <4GB |
| **RAG Pipeline** | Response Time | 1-2s | <5s |
| | Queries/Sec | >0.5 | >0.2 |
| **Agent System** | Response Time | <5s | <15s |
| | Success Rate | >90% | >80% |
| **Telegram** | Delivery Rate | >99% | >95% |
| | Latency | <10s | <30s |
| **Full Pipeline** | End-to-End | <10s | <20s |
| **System** | Uptime | 99%+ | 95%+ |

---

## 🔍 Interpreting Results

### Good Performance ✅
```json
{
  "cv_performance": {
    "avg_inference_time": 0.038,
    "fps": 26.3,
    "total_tests": 10
  },
  "rag_performance": {
    "avg_response_time": 1.45,
    "queries_per_second": 0.69,
    "total_queries": 5
  }
}
```
✓ CV: 26.3 FPS exceeds 20 FPS target  
✓ RAG: 1.45s response is within 1-2s target

### Needs Optimization ⚠️
```json
{
  "cv_performance": {
    "avg_inference_time": 0.15,
    "fps": 6.7,
    "total_tests": 10
  }
}
```
✗ CV: 6.7 FPS below 20 FPS target  
→ **Action**: Optimize model (quantization, batch processing, etc.)

---

## 📊 What Each Metric Means

### CV Metrics
- **FPS (Frames Per Second)**: How many video frames can be analyzed per second
  - Low FPS = model too slow or hardware underpowered
  - Solution: Use faster model, GPU acceleration, or reduce resolution

- **Inference Latency**: Time to process ONE frame
  - Should be <50ms for smooth real-time processing
  - If >100ms: bottleneck is model or hardware

- **Memory**: RAM/GPU memory used during processing
  - Monitor for memory leaks
  - If growing over time: there's a leak

### RAG Metrics
- **Response Time**: Time from query to complete recommendation
  - Breakdown: embedding (100-300ms) + retrieval (50-100ms) + generation (500-1000ms)
  - If >3s: embedding model or LLM is slow

- **Queries/Second**: Throughput capability
  - >0.5 QPS = can handle ~1 incident per 2 seconds

### Agent Metrics
- **Success Rate**: % of incidents successfully processed
  - <90% indicates bugs or edge cases

- **Response Time**: Total time for agent coordination
  - Should be faster than CV+RAG combined due to parallelization

---

## 🛠️ Troubleshooting

### Issue: CV FPS is too low
```python
# Check what's bottlenecking
# 1. Profile individual components
import cProfile
cProfile.run('detector.generate_event_description(...)')

# 2. Options to improve:
# - Reduce input image resolution
# - Use quantized model
# - Enable GPU acceleration
# - Implement frame skipping (every 3rd frame)
# - Use model ensemble reduction
```

### Issue: RAG responses are slow
```python
# 1. Check FAISS index performance
# 2. Cache frequent queries
# 3. Use faster embedding model (e.g., all-MiniLM-L12-v2)
# 4. Reduce retrieved documents (k=3 instead of k=5)
# 5. Use faster LLM (smaller model)
```

### Issue: Telegram delivery failing
```python
# 1. Check internet connection
# 2. Verify Telegram bot token is valid
# 3. Check rate limits (max 30 msgs/sec)
# 4. Implement exponential backoff retry
# 5. Monitor Telegram API status
```

---

## 📈 Tracking Performance Over Time

### Create a tracking script:
```python
from metrics_tracker import MetricsTracker
import schedule
import time

tracker = MetricsTracker()

def periodic_test():
    tester = PerformanceTester(tracker)
    tester.run_quick_benchmark()

# Run every hour
schedule.every().hour.do(periodic_test)

while True:
    schedule.run_pending()
    time.sleep(60)
```

### Analyze trends:
```bash
# Export and analyze
python -c "
from metrics_tracker import MetricsTracker
tracker = MetricsTracker()

# Get stats from last 24 hours
cv_stats = tracker.get_statistics('cv', window_hours=24)
rag_stats = tracker.get_statistics('rag', window_hours=24)

print('CV Performance Trend:')
print(f'  FPS: {cv_stats.get(\"fps\", {})}')
print('RAG Performance Trend:')
print(f'  Response Time: {rag_stats.get(\"response_time_ms\", {})}')
"
```

---

## ✅ Production Readiness Checklist

System is production-ready when:
- [ ] CV FPS ≥ 20 (or at least ≥15)
- [ ] CV memory stable (no growth over time)
- [ ] RAG response time <2 seconds
- [ ] Agent success rate >90%
- [ ] Telegram delivery >99%
- [ ] End-to-end latency <10 seconds
- [ ] Zero critical errors in 24-hour test
- [ ] Dashboard loads in <2 seconds
- [ ] System uptime >99% in test period
- [ ] Monitoring/logging configured

---

## 📞 Support

For detailed metrics explanation, see: `PERFORMANCE_EVALUATION.md`  
For evaluation code, see: `evaluate_performance.py`  
For metric tracking, see: `metrics_tracker.py`
