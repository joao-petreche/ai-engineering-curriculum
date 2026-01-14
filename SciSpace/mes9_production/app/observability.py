"""Observability setup: metrics, tracing, logging."""

import logging
import json
from pythonjsonlogger import jsonlogger
from typing import Literal

from prometheus_client import Counter, Histogram, Gauge
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader


# Prometheus metrics
request_count = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)

request_latency = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency",
    ["method", "endpoint"],
    buckets=(0.01, 0.05, 0.1, 0.5, 1.0, 2.5, 5.0)
)

error_count = Counter(
    "errors_total",
    "Total errors",
    ["error_type"]
)

active_connections = Gauge(
    "active_connections",
    "Active database connections"
)


def setup_logging(log_level: str | Literal["DEBUG", "INFO", "WARNING", "ERROR"]) -> logging.Logger:
    """Setup structured JSON logging."""
    logger = logging.getLogger("bps-api")
    logger.setLevel(log_level)
    
    # Remove default handlers
    logger.handlers.clear()
    
    # JSON handler
    json_handler = logging.StreamHandler()
    json_formatter = jsonlogger.JsonFormatter(
        fmt="%(timestamp)s %(level)s %(name)s %(message)s",
        timestamp=True
    )
    json_handler.setFormatter(json_formatter)
    logger.addHandler(json_handler)
    
    return logger


def setup_observability(service_name: str):
    """Setup OpenTelemetry tracing and metrics."""
    
    # Jaeger exporter
    jaeger_exporter = JaegerExporter(
        agent_host_name="localhost",
        agent_port=6831,
    )
    
    # Trace provider
    trace_provider = TracerProvider()
    trace_provider.add_span_processor(
        BatchSpanProcessor(jaeger_exporter)
    )
    trace.set_tracer_provider(trace_provider)
    
    # Metrics (Prometheus is collected via /metrics endpoint)
    # For advanced setup with Jaeger metrics, use additional exporters
