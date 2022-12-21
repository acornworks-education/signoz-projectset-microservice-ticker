import logging

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http._log_exporter import (
    OTLPLogExporter
)
from opentelemetry.sdk._logs import (
    LoggerProvider,
    LoggingHandler
)
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter
)

def init():
    trace.set_tracer_provider(TracerProvider())
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(ConsoleSpanExporter())
    )

    logger_provider = LoggerProvider(
        resource=Resource.create(
            {
                'service.name': 'ticker',
                'service.group': 'acornworks'
            }
        ),
    )
    set_logger_provider(logger_provider)

    exporter = OTLPLogExporter()
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(exporter))
    handler = LoggingHandler(level=logging.INFO, logger_provider=logger_provider)

    # Attach OTLP handler to root logger
    logging.getLogger().addHandler(handler)
