# Performance Evaluation Checklist - 5-Stage Strategy

## Pre-Evaluation Preparation

- [ ] Environment activated: `source venv/bin/activate`
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] GROQ_API_KEY configured in `.env`
- [ ] UCSD dataset available at `data/raw/ucsd/`
- [ ] Telegram credentials ready (if testing Stage 4)
- [ ] Dashboard running on Streamlit (if testing Stage 5)
- [ ] System resources available (4GB+ RAM for tests)

---

## STAGE 1: Computer Vision (CV) Detection Module

### 1.1 Precision/Recall Evaluation
**Command:**
```bash
python -c "
from comprehensive_evaluation_suite import Stage1_CVDetectionEvaluation
stage = Stage1_CVDetectionEvaluation()
stage.evaluate_precision_recall(test_images_limit=50)
print('\nResults:', stage.results['precision_recall'])
"
```

**Expected Output:**
- [ ] Precision: >0.85 ✓
- [ ] Recall: >0.85 ✓
- [ ] F1 Score: >0.85 ✓
- [ ] Status: PASSED

**If Failed:**
- [ ] Review misclassifications
- [ ] Check confidence thresholds
- [ ] Consider threshold adjustment
- [ ] Analyze false positive cases

---

### 1.2 Confidence Calibration Evaluation
**Command:**
```bash
python -c "
from comprehensive_evaluation_suite import Stage1_CVDetectionEvaluation
stage = Stage1_CVDetectionEvaluation()
stage.evaluate_confidence_calibration()
print('ECE:', stage.results['confidence_calibration']['expected_calibration_error'])
"
```

**Expected Output:**
- [ ] Expected Calibration Error (ECE): <0.1 ✓
- [ ] Status: WELL_CALIBRATED

**If Failed:**
- [ ] Consider temperature scaling
- [ ] Retrain with confidence penalty
- [ ] Use Platt scaling or isotonic regression

---

### 1.3 Latency Evaluation (FPS)
**Command:**
```bash
python -c "
from comprehensive_evaluation_suite import Stage1_CVDetectionEvaluation
stage = Stage1_CVDetectionEvaluation()
stage.evaluate_latency(num_frames=50)
print('FPS:', stage.results['latency']['fps'])
print('Avg Latency:', stage.results['latency']['avg_latency_ms'], 'ms')
"
```

**Expected Output:**
- [ ] FPS: ≥20 ✓
- [ ] Avg Latency: <50ms ✓
- [ ] P95 Latency: <100ms ✓
- [ ] Status: REALTIME

**If Failed (FPS <20):**
- [ ] Profile code to find bottleneck
- [ ] Consider GPU acceleration
- [ ] Try model quantization
- [ ] Reduce input resolution
- [ ] Implement batch processing

---

### 1.4 Memory Usage Evaluation
**Command:**
```bash
python -c "
from comprehensive_evaluation_suite import Stage1_CVDetectionEvaluation
stage = Stage1_CVDetectionEvaluation()
stage.evaluate_memory_usage(num_frames=30)
print('Avg Memory:', stage.results['memory_usage']['avg_memory_gb'], 'GB')
print('Peak Memory:', stage.results['memory_usage']['max_memory_gb'], 'GB')
"
```

**Expected Output:**
- [ ] Device: GPU or CPU detected ✓
- [ ] Avg Memory: <2GB ✓
- [ ] Peak Memory: <4GB ✓
- [ ] Status: EFFICIENT

**If Failed (Memory >4GB):**
- [ ] Check for memory leaks
- [ ] Reduce batch size
- [ ] Use smaller model
- [ ] Enable garbage collection

**Stage 1 Summary:**
- [ ] All 4 sub-evaluations completed
- [ ] All metrics within targets
- [ ] No critical errors
- [ ] Ready for Stage 2

---

## STAGE 2: RAG Pipeline Performance

### 2.1 Relevance Score Evaluation
**Command:**
```bash
python -c "
from comprehensive_evaluation_suite import Stage2_RAGPipelineEvaluation
stage = Stage2_RAGPipelineEvaluation()
stage.evaluate_relevance_score()
print('Avg Relevance:', stage.results['relevance_score']['avg_relevance'])
"
```

**Expected Output:**
- [ ] Avg Relevance: >0.80 ✓
- [ ] All incident types >0.75
- [ ] Status: PASSED

**If Failed:**
- [ ] Review knowledge base documents
- [ ] Check embedding quality
- [ ] Consider FAISS parameter tuning
- [ ] Verify document preprocessing

---

### 2.2 Response Accuracy Evaluation
**Command:**
```bash
python -c "
from comprehensive_evaluation_suite import Stage2_RAGPipelineEvaluation
stage = Stage2_RAGPipelineEvaluation()
stage.evaluate_response_accuracy()
print('Accuracy:', stage.results['response_accuracy']['avg_accuracy'])
"
```

**Expected Output:**
- [ ] Accuracy: >0.75 ✓
- [ ] Status: PASSED

**If Failed:**
- [ ] Review recommendations
- [ ] Improve knowledge base
- [ ] Adjust prompt template
- [ ] Check LLM quality

---

### 2.3 Query Latency Evaluation
**Command:**
```bash
python -c "
from comprehensive_evaluation_suite import Stage2_RAGPipelineEvaluation
stage = Stage2_RAGPipelineEvaluation()
stage.evaluate_query_latency(num_queries=20)
print('Avg Response Time:', stage.results['query_latency']['avg_latency_s'], 's')
print('QPS:', stage.results['query_latency']['queries_per_second'])
"
```

**Expected Output:**
- [ ] Avg Response: <2s ✓
- [ ] QPS: >0.5 ✓
- [ ] Status: FAST

**If Failed (Response >2s):**
- [ ] Profile to identify bottleneck
- [ ] Cache frequent queries
- [ ] Use faster embedding model
- [ ] Optimize FAISS index
- [ ] Try smaller LLM

---

### 2.4 Embedding Quality Evaluation
**Command:**
```bash
python -c "
from comprehensive_evaluation_suite import Stage2_RAGPipelineEvaluation
stage = Stage2_RAGPipelineEvaluation()
stage.evaluate_embedding_quality()
print('Separation:', stage.results['embedding_quality']['separation'])
"
```

**Expected Output:**
- [ ] Similar Score: >0.85 ✓
- [ ] Dissimilar Score: <0.3 ✓
- [ ] Separation: >0.6 ✓
- [ ] Status: GOOD_QUALITY

**If Failed:**
- [ ] Try different embedding model
- [ ] Fine-tune embedding model
- [ ] Improve data preprocessing

**Stage 2 Summary:**
- [ ] All 4 sub-evaluations completed
- [ ] All metrics within targets
- [ ] Ready for Stage 3

---

## STAGE 3: Multi-Agent System

### 3.1 Agent Response Times Evaluation
**Command:**
```bash
python -c "
from comprehensive_evaluation_suite import Stage3_MultiAgentEvaluation
stage = Stage3_MultiAgentEvaluation()
stage.evaluate_agent_response_times()
print('Total Time:', stage.results['agent_response_times']['total']['avg_time_s'], 's')
"
```

**Expected Output:**
- [ ] CV Agent: 1-2s ✓
- [ ] RAG Agent: 1-2s ✓
- [ ] Alert Agent: <1s ✓
- [ ] Total: <5s ✓

---

### 3.2 Communication Efficiency Evaluation
**Command:**
```bash
python -c "
from comprehensive_evaluation_suite import Stage3_MultiAgentEvaluation
stage = Stage3_MultiAgentEvaluation()
stage.evaluate_communication_efficiency()
print('Overhead:', stage.results['communication_efficiency']['communication_overhead_percent'], '%')
"
```

**Expected Output:**
- [ ] Overhead: <10% ✓
- [ ] Status: EFFICIENT

---

### 3.3 Alert Accuracy Evaluation
**Command:**
```bash
python -c "
from comprehensive_evaluation_suite import Stage3_MultiAgentEvaluation
stage = Stage3_MultiAgentEvaluation()
stage.evaluate_alert_accuracy()
print('Accuracy:', stage.results['alert_accuracy']['accuracy_percent'], '%')
"
```

**Expected Output:**
- [ ] Accuracy: >90% ✓
- [ ] Precision: >85% ✓
- [ ] Recall: >85% ✓

---

### 3.4 False Positive Rate Evaluation
**Command:**
```bash
python -c "
from comprehensive_evaluation_suite import Stage3_MultiAgentEvaluation
stage = Stage3_MultiAgentEvaluation()
stage.evaluate_false_positive_rate()
print('FPR:', stage.results['false_positive_rate']['fpr_percent'], '%')
"
```

**Expected Output:**
- [ ] FPR: <2% ✓
- [ ] Status: LOW_FPR

**Stage 3 Summary:**
- [ ] All 4 sub-evaluations completed
- [ ] All metrics within targets
- [ ] Ready for Stage 4

---

## STAGE 4: Telegram Integration

### 4.1 Message Delivery Rate Evaluation
**Command:**
```bash
python -c "
from comprehensive_evaluation_suite import Stage4_TelegramIntegrationEvaluation
stage = Stage4_TelegramIntegrationEvaluation()
stage.evaluate_message_delivery()
print('Delivery Rate:', stage.results['message_delivery']['delivery_rate_percent'], '%')
"
```

**Expected Output:**
- [ ] Delivery Rate: >99.5% ✓
- [ ] Status: EXCELLENT

---

### 4.2 Delivery Latency Evaluation
**Command:**
```bash
python -c "
from comprehensive_evaluation_suite import Stage4_TelegramIntegrationEvaluation
stage = Stage4_TelegramIntegrationEvaluation()
stage.evaluate_delivery_latency()
print('Avg Latency:', stage.results['delivery_latency']['avg_latency_s'], 's')
"
```

**Expected Output:**
- [ ] Avg Latency: <10s ✓
- [ ] P95: <10s ✓
- [ ] Status: FAST

---

### 4.3 Error Handling Evaluation
**Command:**
```bash
python -c "
from comprehensive_evaluation_suite import Stage4_TelegramIntegrationEvaluation
stage = Stage4_TelegramIntegrationEvaluation()
stage.evaluate_error_handling()
print('Recovery Rate:', stage.results['error_handling']['recovery_rate_percent'], '%')
"
```

**Expected Output:**
- [ ] Recovery Rate: >95% ✓
- [ ] Status: ROBUST

**Stage 4 Summary:**
- [ ] All 3 sub-evaluations completed
- [ ] All metrics within targets
- [ ] Ready for Stage 5

---

## STAGE 5: Dashboard (Streamlit)

### 5.1 Page Load Time Evaluation
**Command:**
```bash
python -c "
from comprehensive_evaluation_suite import Stage5_DashboardEvaluation
stage = Stage5_DashboardEvaluation()
stage.evaluate_page_load_time()
print('Avg Load Time:', stage.results['page_load_time']['avg_load_time_s'], 's')
"
```

**Expected Output:**
- [ ] Avg Load: <2s ✓
- [ ] Max Load: <3s ✓
- [ ] Status: FAST

---

### 5.2 Data Display Accuracy Evaluation
**Command:**
```bash
python -c "
from comprehensive_evaluation_suite import Stage5_DashboardEvaluation
stage = Stage5_DashboardEvaluation()
stage.evaluate_data_display_accuracy()
print('Accuracy:', stage.results['data_display_accuracy']['accuracy_percent'], '%')
"
```

**Expected Output:**
- [ ] Accuracy: >99% ✓
- [ ] Status: ACCURATE

---

### 5.3 User Responsiveness Evaluation
**Command:**
```bash
python -c "
from comprehensive_evaluation_suite import Stage5_DashboardEvaluation
stage = Stage5_DashboardEvaluation()
stage.evaluate_user_responsiveness()
print('Responsive Scenarios:', stage.results['user_responsiveness']['responsive_below_500ms'])
"
```

**Expected Output:**
- [ ] Responsive at: ≥3 load levels ✓
- [ ] Status: RESPONSIVE

**Stage 5 Summary:**
- [ ] All 3 sub-evaluations completed
- [ ] All metrics within targets

---

## COMPREHENSIVE FULL EVALUATION

### Run All 5 Stages at Once
```bash
python comprehensive_evaluation_suite.py
```

**Expected Runtime:** 30-45 minutes

**Output:**
- `performance_results/comprehensive_evaluation_YYYYMMDD_HHMMSS.json`

### Verify Output
```bash
# View report
python -c "
import json
with open('performance_results/comprehensive_evaluation_*.json') as f:
    data = json.load(f)
    for stage in data['stages']:
        print(f\"\n{stage['stage']}:\")
        print(f\"  Status: {stage['status']}\")
        print(f\"  Errors: {len(stage['errors'])}\")
"
```

---

## FINAL SUCCESS CHECKLIST

- [ ] **Stage 1**: CV Detection - ALL PASSED
  - [ ] Precision/Recall >85%
  - [ ] Confidence Calibration: ECE <0.1
  - [ ] Latency: FPS ≥20
  - [ ] Memory: Peak <4GB

- [ ] **Stage 2**: RAG Pipeline - ALL PASSED
  - [ ] Relevance >0.80
  - [ ] Accuracy >75%
  - [ ] Query Latency <2s
  - [ ] Embedding Quality: Separation >0.6

- [ ] **Stage 3**: Multi-Agent - ALL PASSED
  - [ ] Agent Times: CV <2s, RAG <2s, Alert <1s
  - [ ] Communication Overhead <10%
  - [ ] Alert Accuracy >90%
  - [ ] FPR <2%

- [ ] **Stage 4**: Telegram - ALL PASSED
  - [ ] Delivery Rate >99.5%
  - [ ] Latency <10s
  - [ ] Recovery Rate >95%

- [ ] **Stage 5**: Dashboard - ALL PASSED
  - [ ] Page Load <2s
  - [ ] Data Accuracy >99%
  - [ ] User Responsiveness: 3+ load levels

---

## PRODUCTION READINESS SIGN-OFF

System is PRODUCTION READY when:
- [ ] All 5 stages evaluated
- [ ] All metrics within targets (no YELLOW/RED)
- [ ] No critical errors
- [ ] End-to-end latency <10s
- [ ] System uptime >99% in 24-hour test
- [ ] False positive rate <2%
- [ ] Message delivery >99.5%

**Status:** _______________  
**Date:** _______________  
**Approved By:** _______________  

---

## TROUBLESHOOTING

### Common Issues

**Issue: Stage 1 FPS too low**
```
Solution: Try GPU, quantization, or batch processing
```

**Issue: Stage 2 responses slow**
```
Solution: Cache queries, faster embedding model
```

**Issue: Stage 3 accuracy low**
```
Solution: Review confidence thresholds, check data quality
```

**Issue: Stage 4 delivery failures**
```
Solution: Check rate limits, network, API key
```

**Issue: Stage 5 dashboard slow**
```
Solution: Lazy load components, optimize database queries
```

---

## QUICK REFERENCE

| Stage | Component | Target | Check Command |
|-------|-----------|--------|---------------|
| 1 | Precision | >85% | `stage.results['precision_recall']['precision']` |
| 1 | Recall | >85% | `stage.results['precision_recall']['recall']` |
| 1 | FPS | ≥20 | `stage.results['latency']['fps']` |
| 1 | Memory | <4GB | `stage.results['memory_usage']['max_memory_gb']` |
| 2 | Relevance | >0.80 | `stage.results['relevance_score']['avg_relevance']` |
| 2 | Latency | <2s | `stage.results['query_latency']['avg_latency_s']` |
| 3 | Accuracy | >90% | `stage.results['alert_accuracy']['accuracy_percent']` |
| 3 | FPR | <2% | `stage.results['false_positive_rate']['fpr_percent']` |
| 4 | Delivery | >99.5% | `stage.results['message_delivery']['delivery_rate_percent']` |
| 5 | Load Time | <2s | `stage.results['page_load_time']['avg_load_time_s']` |

---

**Document Version**: 1.0  
**Last Updated**: April 29, 2026  
**Evaluation Strategy**: 5-Stage Comprehensive  
