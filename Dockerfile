FROM python:3.11-buster

COPY src/ticker /

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN ls -al
RUN pip install -r requirements.txt
RUN opentelemetry-bootstrap --action=install

ENV OTEL_RESOURCE_ATTRIBUTES=service.name=ticker,service.group=acornworks 
ENV OTEL_EXPORTER_OTLP_ENDPOINT=http://host.docker.internal:4318

ENTRYPOINT ["/bin/sh"]
CMD ["-c", "opentelemetry-instrument --traces_exporter otlp_proto_http --metrics_exporter otlp_proto_http waitress-serve --host 0.0.0.0 --port 8080 app:app"]

