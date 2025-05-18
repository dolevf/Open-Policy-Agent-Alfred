FROM python:3-bullseye

LABEL description="OPA Alfred"
LABEL github="https://github.com/dolevf/Open-Policy-Agent-Alfred"
LABEL maintainers="Dolev Farhi"

ARG TARGET_FOLDER=/app

WORKDIR $TARGET_FOLDER/

RUN groupadd -r appuser && useradd -r -g appuser appuser

RUN mkdir /app/bin
RUN apt-get install curl
RUN curl -L -o bin/opa https://openpolicyagent.org/downloads/latest/opa_linux_amd64_static
RUN chmod u+x bin/opa

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY core /app/core
COPY static /app/static
COPY templates /app/templates
COPY temp /app/temp
COPY config.py /app
COPY alfred.py /app
COPY version.py /app

RUN chown -R appuser. /app

USER appuser

EXPOSE 5000/tcp

CMD ["python3", "alfred.py"]
