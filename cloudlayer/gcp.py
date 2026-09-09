"""GCP adapter. Implement upload/download/push_image for Lab 1."""
from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from cloudlayer.base import CloudAdapter


class GcpAdapter(CloudAdapter):
    def _bucket_and_prefix(self) -> tuple[str, str]:
        parsed = urlparse(self.cfg.blob_uri)
        bucket = parsed.netloc
        prefix = parsed.path.lstrip("/")
        return bucket, prefix

    def upload(self, local_path: str, key: str) -> str:
        from google.cloud import storage

        bucket_name, prefix = self._bucket_and_prefix()
        full_key = f"{prefix}/{key}" if prefix else key

        client = storage.Client(project=self.cfg.project_id)
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(full_key)
        blob.upload_from_filename(local_path)

        return f"gs://{bucket_name}/{full_key}"

    def download(self, uri: str, local_path: str) -> None:
        from google.cloud import storage

        parsed = urlparse(uri)
        bucket_name = parsed.netloc
        blob_key = parsed.path.lstrip("/")

        Path(local_path).parent.mkdir(parents=True, exist_ok=True)

        client = storage.Client(project=self.cfg.project_id)
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(blob_key)
        blob.download_to_filename(local_path)

    def push_image(self, local_tag: str) -> str:
        name, _, tag = local_tag.partition(":")
        remote_tag = f"{self.cfg.container_registry}/{name}:{tag}"

        subprocess.run(["docker", "tag", local_tag, remote_tag], check=True)
        subprocess.run(["docker", "push", remote_tag], check=True)

        result = subprocess.run(
            ["docker", "inspect", "--format={{index .RepoDigests 0}}", remote_tag],
            check=True,
            capture_output=True,
            text=True,
        )
        digest_ref = result.stdout.strip()
        return digest_ref

    # submit_training / register_model  -> Lab 2 (Vertex custom training + Model Registry)
    # deploy / invoke                   -> Lab 3 (Vertex Endpoint)
    # emit_metric                       -> Lab 4 (Cloud Monitoring time series)
    # generate                          -> Lab 5 (managed LLM endpoint; read usageMetadata for tokens)
    # teardown                          -> Lab 5 (filter resources by label)
