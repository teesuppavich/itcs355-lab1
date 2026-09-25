from src import config
from cloudlayer.factory import get_adapter


def main():
    cfg = config.load()
    adapter = get_adapter(cfg)

    image_uri = (
        "asia-southeast1-docker.pkg.dev/"
        "itcs355-6688097/itcs355/itcs355-lab1@sha256:"
        "0b54b73ddb9f6bd5206e85dd5a4696cad1c1874808ddc59860249b32b34a8296"
    )

    args = {
        "n_estimators": 100,
        "max_depth": 2,
        "min_samples_leaf": 5,
        "seed": 20260101,
        "run_name": "lab3-canary-worse",
        "blob_uri": cfg.blob_uri,
        "metrics_out": "/tmp/metrics.json",
        "git_commit": "b21c82ef7171fed28533b52eca4cdfa20a57f1a0",
    }

    print("Submitting Vertex AI training job...")
    job_id = adapter.submit_training(image_uri, args)
    print(f"JOB_ID={job_id}")

    print("Waiting for training job...")
    result = adapter.wait_training(job_id)
    print(result)


if __name__ == "__main__":
    main()
