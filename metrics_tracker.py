#!/usr/bin/env python3
"""
Performance Metrics Tracker
Logs and tracks system performance metrics over time for trend analysis
"""

import json
import time
from datetime import datetime
from pathlib import Path
import statistics
from typing import Dict, List


class MetricsTracker:
    def __init__(self, metrics_file="data/metrics_history.jsonl"):
        self.metrics_file = Path(metrics_file)
        self.metrics_file.parent.mkdir(parents=True, exist_ok=True)
        self.current_metrics = {}
    
    def log_cv_metrics(self, fps: float, avg_latency: float, memory_gb: float):
        """Log CV module metrics"""
        self.current_metrics["cv"] = {
            "timestamp": datetime.now().isoformat(),
            "fps": fps,
            "avg_latency_ms": avg_latency * 1000,
            "memory_gb": memory_gb
        }
        self._append_metric("cv")
        print(f"✓ CV Metrics: FPS={fps:.1f}, Latency={avg_latency*1000:.1f}ms, Memory={memory_gb:.2f}GB")
    
    def log_rag_metrics(self, response_time: float, queries_per_sec: float, relevance_score: float = None):
        """Log RAG pipeline metrics"""
        self.current_metrics["rag"] = {
            "timestamp": datetime.now().isoformat(),
            "response_time_ms": response_time * 1000,
            "queries_per_second": queries_per_sec,
            "relevance_score": relevance_score
        }
        self._append_metric("rag")
        print(f"✓ RAG Metrics: Response={response_time*1000:.1f}ms, QPS={queries_per_sec:.2f}")
    
    def log_agent_metrics(self, response_time: float, success_rate: float, alert_count: int):
        """Log agent system metrics"""
        self.current_metrics["agent"] = {
            "timestamp": datetime.now().isoformat(),
            "response_time_ms": response_time * 1000,
            "success_rate_percent": success_rate,
            "alerts_generated": alert_count
        }
        self._append_metric("agent")
        print(f"✓ Agent Metrics: Response={response_time*1000:.1f}ms, Success={success_rate:.1f}%")
    
    def log_telegram_metrics(self, delivery_rate: float, delivery_latency: float, errors: int = 0):
        """Log Telegram integration metrics"""
        self.current_metrics["telegram"] = {
            "timestamp": datetime.now().isoformat(),
            "delivery_rate_percent": delivery_rate,
            "avg_delivery_latency_s": delivery_latency,
            "error_count": errors
        }
        self._append_metric("telegram")
        print(f"✓ Telegram Metrics: Delivery={delivery_rate:.1f}%, Latency={delivery_latency:.2f}s")
    
    def log_incident(self, incident_type: str, confidence: float, response_time: float, 
                    location: str = None, status: str = "processed"):
        """Log individual incident metrics"""
        incident = {
            "timestamp": datetime.now().isoformat(),
            "incident_type": incident_type,
            "confidence": confidence,
            "response_time_ms": response_time * 1000,
            "location": location,
            "status": status
        }
        self.current_metrics["incident"] = incident
        self._append_metric("incident")
        print(f"✓ Incident: {incident_type} at {location} (Confidence={confidence:.2f}, Time={response_time*1000:.1f}ms)")
    
    def log_error(self, component: str, error_type: str, message: str):
        """Log system errors"""
        error = {
            "timestamp": datetime.now().isoformat(),
            "component": component,
            "error_type": error_type,
            "message": message
        }
        self.current_metrics["error"] = error
        self._append_metric("error")
        print(f"✗ Error in {component}: {error_type} - {message}")
    
    def _append_metric(self, metric_type: str):
        """Append metric to JSON lines file"""
        with open(self.metrics_file, 'a') as f:
            f.write(json.dumps({metric_type: self.current_metrics[metric_type]}) + '\n')
    
    def get_statistics(self, metric_type: str, window_hours: int = 24) -> Dict:
        """Calculate statistics for a metric type over time window"""
        if not self.metrics_file.exists():
            return {}
        
        cutoff_time = datetime.now().timestamp() - (window_hours * 3600)
        values = []
        
        with open(self.metrics_file, 'r') as f:
            for line in f:
                data = json.loads(line)
                if metric_type in data:
                    metric = data[metric_type]
                    timestamp = datetime.fromisoformat(metric["timestamp"]).timestamp()
                    
                    if timestamp >= cutoff_time:
                        # Extract numeric values
                        for key, val in metric.items():
                            if key != "timestamp" and isinstance(val, (int, float)):
                                values.append((key, val))
        
        if not values:
            return {}
        
        # Group by metric name and calculate stats
        stats = {}
        value_dict = {}
        for key, val in values:
            if key not in value_dict:
                value_dict[key] = []
            value_dict[key].append(val)
        
        for key, vals in value_dict.items():
            stats[key] = {
                "min": min(vals),
                "max": max(vals),
                "avg": statistics.mean(vals),
                "median": statistics.median(vals),
                "stddev": statistics.stdev(vals) if len(vals) > 1 else 0,
                "samples": len(vals)
            }
        
        return stats
    
    def generate_report(self, hours: int = 24):
        """Generate comprehensive performance report for last N hours"""
        print("\n" + "="*70)
        print(f"PERFORMANCE REPORT - Last {hours} Hours")
        print("="*70)
        
        metrics_types = ["cv", "rag", "agent", "telegram", "incident", "error"]
        
        for metric_type in metrics_types:
            stats = self.get_statistics(metric_type, hours)
            if stats:
                print(f"\n{metric_type.upper()} Metrics:")
                for metric_name, values in stats.items():
                    print(f"  {metric_name}:")
                    print(f"    Min: {values['min']:.2f} | Max: {values['max']:.2f}")
                    print(f"    Avg: {values['avg']:.2f} | Median: {values['median']:.2f}")
                    print(f"    StdDev: {values['stddev']:.2f} | Samples: {values['samples']}")
        
        print("\n" + "="*70)
    
    def export_metrics(self, output_file: str = None):
        """Export all metrics to CSV for external analysis"""
        if output_file is None:
            output_file = f"metrics_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        import csv
        
        if not self.metrics_file.exists():
            print("No metrics to export")
            return
        
        # Collect all metrics
        all_metrics = []
        with open(self.metrics_file, 'r') as f:
            for line in f:
                data = json.loads(line)
                all_metrics.append(data)
        
        # Export to CSV (flatten structure)
        if all_metrics:
            with open(output_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Timestamp", "Metric_Type", "Metric_Name", "Value"])
                
                for metric in all_metrics:
                    for metric_type, values in metric.items():
                        timestamp = values.get("timestamp", "")
                        for key, val in values.items():
                            if key != "timestamp":
                                writer.writerow([timestamp, metric_type, key, val])
        
        print(f"✓ Metrics exported to {output_file}")


class PerformanceTester:
    """Quick performance tests for benchmark purposes"""
    
    def __init__(self, tracker: MetricsTracker = None):
        self.tracker = tracker or MetricsTracker()
    
    def test_cv_performance(self, num_images: int = 10):
        """Quick CV performance test"""
        print(f"\n🧪 Testing CV performance on {num_images} images...")
        try:
            from src.cv_detection.anomaly_detector import CampusAnomalyDetector
            
            detector = CampusAnomalyDetector()
            times = []
            
            for i in range(num_images):
                start = time.time()
                event = detector.generate_event_description(
                    anomaly_score=0.75, 
                    location="Test"
                )
                times.append(time.time() - start)
            
            avg_time = statistics.mean(times)
            fps = 1.0 / avg_time
            
            self.tracker.log_cv_metrics(
                fps=fps,
                avg_latency=avg_time,
                memory_gb=0.0  # TODO: Add actual measurement
            )
            
        except Exception as e:
            self.tracker.log_error("cv", "TestFailed", str(e))
    
    def test_rag_performance(self, num_queries: int = 5):
        """Quick RAG performance test"""
        print(f"\n🧪 Testing RAG performance on {num_queries} queries...")
        try:
            from src.rag.rag_pipeline import UniversitySafetyRAG
            
            rag = UniversitySafetyRAG()
            rag.load_vectorstore()
            
            test_queries = [
                "Fight detected at Building A",
                "Suspicious person near library",
                "Medical emergency on campus",
                "Theft reported in dormitory",
                "Vehicle accident in parking lot"
            ][:num_queries]
            
            times = []
            for query in test_queries:
                start = time.time()
                result = rag.get_safety_recommendation(query)
                times.append(time.time() - start)
            
            avg_time = statistics.mean(times)
            qps = 1.0 / avg_time
            
            self.tracker.log_rag_metrics(
                response_time=avg_time,
                queries_per_sec=qps
            )
            
        except Exception as e:
            self.tracker.log_error("rag", "TestFailed", str(e))
    
    def run_quick_benchmark(self):
        """Run quick benchmark on all components"""
        print("\n" + "="*70)
        print("⚡ QUICK BENCHMARK")
        print("="*70)
        
        self.test_cv_performance(num_images=5)
        self.test_rag_performance(num_queries=3)
        self.tracker.generate_report(hours=24)


if __name__ == "__main__":
    # Example usage
    tracker = MetricsTracker()
    
    # Log sample metrics
    tracker.log_cv_metrics(fps=25.5, avg_latency=0.039, memory_gb=1.2)
    tracker.log_rag_metrics(response_time=1.35, queries_per_sec=0.74, relevance_score=0.87)
    tracker.log_agent_metrics(response_time=3.1, success_rate=92.5, alert_count=5)
    tracker.log_telegram_metrics(delivery_rate=99.8, delivery_latency=0.8, errors=0)
    tracker.log_incident(
        incident_type="fight",
        confidence=0.88,
        response_time=4.2,
        location="Building A entrance",
        status="processed"
    )
    
    # Generate reports
    tracker.generate_report(hours=24)
    tracker.export_metrics()
    
    # Run quick benchmark
    print("\n" + "="*70)
    tester = PerformanceTester(tracker)
    tester.run_quick_benchmark()
