#!/usr/bin/env python3
"""
Telemetry Server - Prometheus Metrics Exporter
"""

import logging
import threading
import os

logger = logging.getLogger(__name__)

_server_started = False
_server_lock = threading.Lock()

def start_telemetry_server(port: int = 8000):
    """Start the Prometheus HTTP server."""
    global _server_started
    with _server_lock:
        if _server_started:
            return
        
        try:
            from prometheus_client import start_http_server
            start_http_server(port)
            _server_started = True
            logger.info(f"🔭 Telemetry: Prometheus metrics server started on port {port}")
        except Exception as e:
            logger.error(f"🔭 Telemetry: Failed to start metrics server: {e}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    start_telemetry_server()
    import time
    while True:
        time.sleep(1)