FROM python:3.11-buster

COPY src/ticker /

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN ls -al
RUN pip install -r requirements.txt

ENTRYPOINT ["/bin/sh"]
CMD ["-c", "waitress-serve --host 0.0.0.0 --port 8080 app:app"]

