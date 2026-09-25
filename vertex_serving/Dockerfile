FROM python:3.12-slim@sha256:78387bc3881b8273120a12ebe6c1ab22b018ccc2c9adf565ae1ac9b536e184ea

ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV MODEL_PATH=/models/model.joblib

WORKDIR /app

COPY vertex_serving/requirements.txt ./
RUN pip install --require-hashes -r requirements.txt

COPY vertex_serving/predictor.py ./

RUN useradd --create-home --uid 10001 runner \
    && mkdir -p /models \
    && chown -R runner:runner /app /models

COPY vertex_serving/model.joblib /models/model.joblib
RUN chown runner:runner /models/model.joblib

EXPOSE 8080

CMD ["python", "-m", "uvicorn", "predictor:app", "--host", "0.0.0.0", "--port", "8080"]
