from __future__ import annotations

import os
import tempfile

import joblib
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel

MODEL_PATH = os.environ.get("MODEL_PATH", "/models/model.joblib")
AIP_STORAGE_URI = os.environ.get("AIP_STORAGE_URI")


def load_model():
    # Local / image-bundled model
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)

    # Vertex AI model artifact
    if AIP_STORAGE_URI:
        from google.cloud import storage

        uri = AIP_STORAGE_URI.removeprefix("gs://")
        bucket_name, _, prefix = uri.partition("/")

        blob_name = f"{prefix.rstrip('/')}/model.joblib"
        blob_name = blob_name.lstrip("/")

        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(blob_name)

        with tempfile.NamedTemporaryFile(suffix=".joblib") as tmp:
            blob.download_to_filename(tmp.name)
            return joblib.load(tmp.name)

    raise FileNotFoundError(
        f"Model not found at {MODEL_PATH} and AIP_STORAGE_URI is not set"
    )


model = load_model()

app = FastAPI()


class PredictRequest(BaseModel):
    instances: list[list[float]]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/ready")
def ready():
    return {"status": "ready"}


@app.post("/predict")
def predict(request: PredictRequest):
    X = np.asarray(request.instances, dtype=float)
    probabilities = model.predict_proba(X)[:, 1]

    return {
        "predictions": probabilities.tolist()
    }
