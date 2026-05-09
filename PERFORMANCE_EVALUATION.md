# Smart University Safety System - Performance Evaluation Guide

## Overview
This guide provides metrics and methodologies to evaluate your system's performance across all components.

---

## 1. COMPUTER VISION (CV) ANOMALY DETECTION

### Key Metrics

#### Inference Performance
- **Frames Per Second (FPS)**: How many frames can be processed per second
  - Target: 20+ FPS for real-time monitoring
  - Formula: `1 / average_inference_time`
  
- **Inference Latency**: Time to process one frame
  - Target: <50ms for real-time
  - Measure using: `time.perf_counter()`

- **Memory Usage**: GPU/CPU memory during inference
  - Monitor with: `torch.cuda.memory_allocated()` or `psutil`
  - Target: <2GB for CPU, <4GB for GPU

#### Detection Accuracy (requires labeled test set)
- **True Positive Rate (TPR)**: % of actual anomalies correctly detected
  - Formula: `TP / (TP + FN)`
  - Target: >85%

- **False Positive Rate (FPR)**: % of normal scenes incorrectly flagged
  - Formula: `FP / (FP + TN)`
  - Target: <5%

- **Confidence Calibration**: How well confidence scores match actual probability of anomaly
  - Tool: Reliability diagrams, Expected Calibration Error (ECE)

### How to Evaluate
```python
# 1. Collect test images from UCSD dataset
# 2. Run inference on each
# 3. Calculate FPS and latency averages
# 4. If labels available, calculate precision/recall
```

---

## 2. RAG PIPELINE

### Key Metrics

#### Response Quality
- **Retrieval Precision**: % of top-k documents relevant to incident
  - Target: >80%
  - Manual evaluation: Rate each retrieved doc as relevant/irrelevant

- **Recommendation Relevance**: Whether suggestions match incident type
  - Evaluate manually or with semantic similarity scoring
  - Target: >85% relevance

- **Response Completeness**: Does recommendation cover all safety aspects?
  - Checklist-based evaluation

#### Performance Metrics
- **Query Latency**: Time from query to full recommendation
  - Target: 1-2 seconds
  - Breakdown: 
    - Embedding time: ~100-300ms
    - Retrieval time: ~50-100ms
    - LLM generation time: ~500-1000ms

- **Throughput**: Queries processed per second
  - Formula: `1 / average_response_time`
  - Target: >0.5 QPS

- **FAISS Index Performance**: Vector similarity search speed
  - Target: <100ms for retrieval

### How to Evaluate
```python
# 1. Create test query set with known good responses
# 2. Measure response times
# 3. Evaluate recommendation quality (manual)
# 4. Calculate retrieval precision
```

---

## 3. MULTI-AGENT SYSTEM

### Key Metrics

#### Response Quality
- **Alert Accuracy**: % of incidents correctly classified and alerted
  - Formula: `correct_alerts / total_incidents`
  - Target: >90%

- **False Alert Rate**: % of non-incidents triggering alerts
  - Target: <2%

- **Alert Timeliness**: Time from detection to alert sent
  - Target: <5 seconds end-to-end

#### Agent Coordination
- **Agent Response Times**:
  - CV Agent: Time to process video frame
  - RAG Agent: Time to generate recommendation
  - Coordinator: Time to orchestrate response

- **Message Overhead**: Extra time due to inter-agent communication
  - Should be <10% of total response time

#### Failure Handling
- **Error Recovery Rate**: % of failures that self-recover
  - Target: >95%

- **Timeout Incidents**: % of calls timing out
  - Target: <1%

### How to Evaluate
```python
# 1. Simulate multiple incident scenarios
# 2. Measure response times for each agent
# 3. Verify correctness of alerts
# 4. Test failure scenarios (network down, API limits)
```

---

## 4. TELEGRAM INTEGRATION

### Key Metrics

#### Delivery Performance
- **Message Delivery Rate**: % of alerts successfully sent
  - Target: 99.5%+
  
- **Delivery Latency**: Time from alert generation to user receipt
  - Target: <10 seconds

- **Retry Success Rate**: % of failed sends that succeed on retry
  - Target: >98%

#### Reliability
- **API Error Rate**: % of Telegram API calls that fail
  - Monitor Telegram response codes
  - Target: <0.5%

- **Rate Limit Violations**: Times API rate limits were hit
  - Target: 0 or very rare

### How to Evaluate
```python
# 1. Send test messages to Telegram
# 2. Log delivery timestamps
# 3. Inject network failures and test recovery
# 4. Monitor API response codes and error rates
```

---

## 5. DASHBOARD (Streamlit)

### Key Metrics

#### Performance
- **Page Load Time**: Time to render dashboard
  - Target: <2 seconds

- **Update Latency**: Time from new alert to dashboard update
  - Target: <1 second

- **Dashboard Responsiveness**: UI interaction delay
  - Target: <500ms

#### User Experience
- **Data Accuracy**: Dashboard displays match actual system state
  - Cross-verify with logs

- **Completeness**: All important metrics visible
  - Checklist of required visualizations

---

## 6. END-TO-END PIPELINE

### Key Metrics

#### Total Latency (incident → user alert)
- **Detection → Alert**: Full pipeline response time
  - Target: <10 seconds
  - Breakdown:
    - Video capture/processing: 1-2s
    - Anomaly detection: 1-2s
    - RAG processing: 1-2s
    - Telegram delivery: <1s
    - Dashboard update: 1s

#### System Reliability
- **Uptime**: % of time system is operational
  - Target: 99%+

- **Critical Error Rate**: Unrecoverable errors per day
  - Target: 0

### How to Evaluate
```python
# 1. Run end-to-end tests with real incidents
# 2. Measure total time from detection to user notification
# 3. Monitor system logs for errors
# 4. Run 24-hour uptime test
```

---

## 7. BENCHMARKING TARGETS

| Component | Metric | Current | Target |
|-----------|--------|---------|--------|
| CV | FPS | ? | 20+ |
| CV | Latency | ? | <50ms |
| CV | Memory | ? | <2GB |
| RAG | Response Time | ? | 1-2s |
| RAG | Relevance | ? | >85% |
| Agent | Alert Accuracy | ? | >90% |
| Agent | Response Time | ? | <5s |
| Telegram | Delivery Rate | ? | 99.5%+ |
| Pipeline | End-to-End | ? | <10s |
| System | Uptime | ? | 99%+ |

---

## 8. TESTING PROCEDURES

### Quick Performance Test (5 min)
```bash
python evaluate_performance.py
# Runs basic benchmarks on all components
```

### Comprehensive Test (30 min)
1. Run 100 images through CV module
2. Process 50 varied queries through RAG
3. Simulate 20 incident scenarios
4. Measure end-to-end pipeline timing

### Production Validation (24+ hours)
1. Deploy to production environment
2. Monitor all metrics continuously
3. Log all errors and anomalies
4. Generate daily performance reports

---

## 9. PERFORMANCE OPTIMIZATION RECOMMENDATIONS

### CV Module
- [ ] Profile inference bottlenecks (CPU vs memory vs I/O)
- [ ] Consider model quantization for faster inference
- [ ] Implement frame skipping for lower FPS cameras
- [ ] Use GPU acceleration if available

### RAG Pipeline
- [ ] Cache frequent queries
- [ ] Batch process multiple incidents
- [ ] Optimize FAISS index parameters
- [ ] Use a faster embedding model if needed

### Agent System
- [ ] Parallelize agent execution where possible
- [ ] Reduce inter-agent communication overhead
- [ ] Implement request batching
- [ ] Use async/await for I/O operations

### Integration
- [ ] Implement message queuing (RabbitMQ, Kafka)
- [ ] Use connection pooling
- [ ] Add database caching layer
- [ ] Implement circuit breaker pattern

---

## 10. MONITORING & LOGGING

### Metrics to Log
- Timestamp of every alert
- Incident type and confidence score
- Response time per component
- Any errors or warnings
- User interactions (dashboard clicks, etc.)

### Log Aggregation
- Store metrics in JSON/CSV for analysis
- Use database (PostgreSQL) for long-term storage
- Implement automated alerts for anomalies

### Visualization
- Create dashboards showing:
  - Incident timeline
  - Response time trends
  - Error rates
  - System health
  - Alert distribution by type/location

---

## 11. SAMPLE EVALUATION SCRIPT USAGE

```bash
# Run evaluation
python evaluate_performance.py

# View results
cat performance_results/performance_report_*.json | python -m json.tool

# Analyze trends
python analyze_performance_trends.py
```

---

## 12. SUCCESS CRITERIA

System is ready for production when:
- ✅ CV FPS > 15 (can handle 1080p @ 30fps)
- ✅ Anomaly detection precision > 85%
- ✅ False alert rate < 2%
- ✅ RAG response time < 2 seconds
- ✅ End-to-end pipeline < 10 seconds
- ✅ Telegram delivery rate > 99%
- ✅ System uptime > 99%
- ✅ No critical unrecoverable errors in 24hr test
