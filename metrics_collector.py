import time
from datetime import datetime
import json
import os
from typing import Dict, Any, List, Optional
from logger_config import get_logger

logger = get_logger(__name__)

class MetricsCollector:
    def __init__(self):
        self.metrics_dir = "metrics"
        os.makedirs(self.metrics_dir, exist_ok=True)
        self._initialize_metrics_file()

    def _initialize_metrics_file(self):
        """Initialize metrics file for the current day"""
        self.current_date = datetime.now().strftime("%Y%m%d")
        self.metrics_file = os.path.join(self.metrics_dir, f"metrics_{self.current_date}.json")
        
        if not os.path.exists(self.metrics_file):
            with open(self.metrics_file, 'w') as f:
                json.dump([], f)

    def _rotate_metrics_file(self):
        """Check and rotate metrics file if date has changed"""
        current_date = datetime.now().strftime("%Y%m%d")
        if current_date != self.current_date:
            self._initialize_metrics_file()

    def record_metric(self, 
                     metric_name: str, 
                     value: Any, 
                     tags: Dict[str, str] = None,
                     timestamp: Optional[float] = None) -> None:
        """Record a metric with the given name and value"""
        try:
            self._rotate_metrics_file()
            
            metric = {
                'name': metric_name,
                'value': value,
                'timestamp': timestamp or time.time(),
                'tags': tags or {}
            }

            with open(self.metrics_file, 'r+') as f:
                metrics = json.load(f)
                metrics.append(metric)
                f.seek(0)
                json.dump(metrics, f)
                f.truncate()

            logger.debug(f"Recorded metric: {metric}")
        except Exception as e:
            logger.error(f"Error recording metric: {e}")

    def get_metrics(self, 
                   metric_name: Optional[str] = None, 
                   start_time: Optional[float] = None,
                   end_time: Optional[float] = None,
                   tags: Optional[Dict[str, str]] = None) -> List[Dict[str, Any]]:
        """Retrieve metrics based on filters"""
        try:
            with open(self.metrics_file, 'r') as f:
                metrics = json.load(f)

            filtered_metrics = metrics
            
            if metric_name:
                filtered_metrics = [m for m in filtered_metrics if m['name'] == metric_name]
            
            if start_time:
                filtered_metrics = [m for m in filtered_metrics if m['timestamp'] >= start_time]
            
            if end_time:
                filtered_metrics = [m for m in filtered_metrics if m['timestamp'] <= end_time]
            
            if tags:
                filtered_metrics = [
                    m for m in filtered_metrics 
                    if all(m['tags'].get(k) == v for k, v in tags.items())
                ]

            return filtered_metrics
        except Exception as e:
            logger.error(f"Error retrieving metrics: {e}")
            return []

    def calculate_statistics(self, metrics: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate basic statistics for numerical metrics"""
        try:
            values = [float(m['value']) for m in metrics if isinstance(m['value'], (int, float))]
            
            if not values:
                return {}

            return {
                'count': len(values),
                'min': min(values),
                'max': max(values),
                'average': sum(values) / len(values)
            }
        except Exception as e:
            logger.error(f"Error calculating statistics: {e}")
            return {}

class CallMetrics:
    def __init__(self):
        self.metrics_collector = MetricsCollector()

    def record_call_duration(self, call_id: str, duration: float):
        """Record the duration of a call"""
        self.metrics_collector.record_metric(
            'call_duration',
            duration,
            tags={'call_id': call_id}
        )

    def record_speech_recognition_time(self, call_id: str, duration: float):
        """Record the time taken for speech recognition"""
        self.metrics_collector.record_metric(
            'speech_recognition_time',
            duration,
            tags={'call_id': call_id}
        )

    def record_ai_processing_time(self, call_id: str, duration: float):
        """Record the time taken for AI processing"""
        self.metrics_collector.record_metric(
            'ai_processing_time',
            duration,
            tags={'call_id': call_id}
        )

    def record_error(self, call_id: str, error_type: str):
        """Record an error occurrence"""
        self.metrics_collector.record_metric(
            'error_count',
            1,
            tags={'call_id': call_id, 'error_type': error_type}
        )

    def get_call_statistics(self, start_time: Optional[float] = None) -> Dict[str, Any]:
        """Get statistics for all calls"""
        metrics = self.metrics_collector.get_metrics('call_duration', start_time=start_time)
        return self.metrics_collector.calculate_statistics(metrics)

    def get_error_rate(self, start_time: Optional[float] = None) -> float:
        """Calculate error rate"""
        total_calls = len(self.metrics_collector.get_metrics('call_duration', start_time=start_time))
        total_errors = len(self.metrics_collector.get_metrics('error_count', start_time=start_time))
        
        if total_calls == 0:
            return 0.0
            
        return total_errors / total_calls
