FROM python:3.9-alpine

LABEL description="OPA Alfred"
LABEL github="https://github.com/dolevf/Open-Policy-Agent-Alfred"
LABEL maintainers="Dolev Farhi"

ARG OPA_BINARY="0.41.0"
ARG TARGET_FOLDER=/app

WORKDIR $TARGET_FOLDER/

RUN mkdir /app/bin
RUN apk add --update curl
RUN curl -L -o bin/opa https://openpolicyagent.org/downloads/v$OPA_BINARY/opa_linux_amd64_static
RUN chmod u+x bin/opa

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY core /app/core
COPY static /app/static
COPY templates /app/templates
COPY temp /app/temp
COPY config.py /app
COPY setup.py /app
COPY alfred.py /app
COPY version.py /app

RUN python3 setup.py
RUN chown -R nobody. /app

USER nobody

EXPOSE 5000/tcp

CMD ["python3", "alfred.py"]