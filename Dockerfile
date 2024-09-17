FROM python:3.11-slim

ARG WORK_SPACE=/workspace
WORKDIR ${WORK_SPACE}
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=$PYTHONPATH:${WORK_SPACE}

COPY requirements.txt ${WORK_SPACE}/requirements.txt
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN python -m spacy download en_core_web_sm

COPY books ${WORK_SPACE}/books
COPY templates ${WORK_SPACE}/templates
COPY static ${WORK_SPACE}/static
COPY lib ${WORK_SPACE}/lib
COPY config.py ${WORK_SPACE}/config.py
COPY main.py ${WORK_SPACE}/main.py

CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:8000", "--access-logfile", "-", "-k", "gevent", "--worker-connections=100"]