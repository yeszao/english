FROM python:3.11-slim

ARG WORK_SPACE=/workspace
WORKDIR ${WORK_SPACE}
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=$PYTHONPATH:${WORK_SPACE}

COPY requirements.txt ${WORK_SPACE}/requirements.txt
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt
#RUN python -m spacy download en_core_web_sm

COPY src ${WORK_SPACE}/src

CMD ["gunicorn", "src.main:app", "--bind", "0.0.0.0:8000", "--access-logfile", "-", "-k", "gevent", "--worker-connections=100"]