"""Lab 2 — reload the registered Vertex AI model by version and score 5 held-out rows."""

import argparse
import tempfile
from pathlib import Path

import joblib
from google.cloud import aiplatform, storage

from src import config, data


def download_registered_model(artifact_uri: str) -> Path:
    """Download model.joblib from the artifact URI stored in Vertex Model Registry."""

    if not artifact_uri.startswith("gs://"):
        raise ValueError(f"Unsupported artifact URI: {artifact_uri}")

    uri = artifact_uri[len("gs://"):]
    bucket_name, prefix = uri.split("/", 1)

    client = storage.Client()
    bucket = client.bucket(bucket_name)

    blob = bucket.blob(f"{prefix.rstrip('/')}/model.joblib")

    tmp_dir = Path(tempfile.mkdtemp(prefix="lab2-reload-"))
    model_path = tmp_dir / "model.joblib"

    blob.download_to_filename(str(model_path))

    return model_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model-id",
        default="97210022034931712",
        help="Vertex AI Model Registry model ID",
    )
    parser.add_argument(
        "--version",
        default="1",
        help="Registered model version",
    )
    parser.add_argument(
        "--rows",
        type=int,
        default=5,
        help="Number of held-out rows to score",
    )
    args = parser.parse_args()

    cfg = config.load(strict=False)

    aiplatform.init(
        project=cfg.project_id,
        location=cfg.region,
    )

    print(
        f"Loading Vertex AI Model Registry model "
        f"{args.model_id}, version {args.version}"
    )

    registry = aiplatform.ModelRegistry(
        model=args.model_id,
        project=cfg.project_id,
        location=cfg.region,
    )

    model = registry.get_model(version=args.version)

    print(f"Registered model: {model.resource_name}")
    print(f"Version: {model.version_id}")
    print(f"Artifact URI: {model.gca_resource.artifact_uri}")

    model_path = download_registered_model(
        model.gca_resource.artifact_uri
    )

    print(f"Downloaded registered artifact to: {model_path}")

    # Load held-out test data.
    df = data.load_raw(cfg.raw_path)
    _, _, test_df = data.split(df, seed=20260101)

    sample = test_df.head(args.rows)

    loaded_model = joblib.load(model_path)

    preds = loaded_model.predict_proba(
        sample[data.FEATURES]
    )[:, 1]

    print("\nPredictions:")

    for rid, p in zip(sample[data.ID], preds):
        print(f"  reading {rid}: p(failure)={p:.4f}")

    print(
        f"\nPASS  Vertex AI registered model version "
        f"{args.version} reloaded and scored {len(sample)} held-out rows"
    )


if __name__ == "__main__":
    main()
