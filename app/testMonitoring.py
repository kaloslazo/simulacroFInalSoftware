from .monitoring import ServiceMonitor
import time

def test_service_monitor():
    monitor = ServiceMonitor()
    
    # Probar registro de peticiones exitosas
    monitor.record_request(duration=0.0005, success=True)
    monitor.record_request(duration=0.0008, success=True)
    
    # Probar registro de errores
    monitor.record_request(duration=0.002, success=False)
    
    metrics = monitor.get_metrics()
    assert "availability" in metrics
    assert "reliability" in metrics
    assert "avg_response_time" in metrics
    assert metrics["total_requests"] == 3
    assert metrics["failed_requests"] == 1

def test_monitor_cleanup():
    monitor = ServiceMonitor(window_size=1)  # 1 segundo de ventana
    monitor.record_request(duration=0.001, success=True)
    
    # Esperar a que expire la ventana
    time.sleep(1.1)
    
    metrics = monitor.get_metrics()
    assert metrics["requests_last_hour"] == 0

def test_latency_calculation():
    monitor = ServiceMonitor()
    
    # Registrar peticiones con diferentes latencias
    monitor.record_request(duration=0.0005, success=True)
    monitor.record_request(duration=0.0008, success=True)
    monitor.record_request(duration=0.0012, success=True)
    
    metrics = monitor.get_metrics()
    assert 0.0005 <= metrics["avg_response_time"] <= 0.0012
    assert metrics["latency_p95"] is not None

def test_metrics_cache():
    monitor = ServiceMonitor()
    monitor.record_request(duration=0.001, success=True)
    
    # Primera llamada a métricas
    metrics1 = monitor.get_metrics()
    # Segunda llamada inmediata (debería usar caché)
    metrics2 = monitor.get_metrics()
    
    assert metrics1 == metrics2