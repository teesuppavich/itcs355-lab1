from __future__ import annotations

import json
import time
from pathlib import Path

from src import config, costs
from cloudlayer.factory import get_adapter


IMAGE_URI = (
    "asia-southeast1-docker.pkg.dev/"
    "itcs355-6688097/itcs355/"
    "itcs355-lab1@sha256:"
    "0b54b73ddb9f6bd5206e85dd5a4696cad1c1874808ddc59860249b32b34a8296"
)

SEARCH_SPACE = {
    "n_estimators": [100, 300],
    "max_depth": [4, 8, 12],
    "min_samples_leaf": [1, 5],
}

CHECKPOINT = Path("reports/tune_remote_checkpoint.json")


def grid():
    trials = []

    for n_estimators in SEARCH_SPACE["n_estimators"]:
        for max_depth in SEARCH_SPACE["max_depth"]:
            for min_samples_leaf in SEARCH_SPACE["min_samples_leaf"]:
                trials.append({
                    "n_estimators": n_estimators,
                    "max_depth": max_depth,
                    "min_samples_leaf": min_samples_leaf,
                })

    return trials


def load_checkpoint():
    if CHECKPOINT.exists():
        return json.loads(CHECKPOINT.read_text())

    return {
        "completed": [],
        "spent_thb": 0.0,
        "trials": [],
    }


def save_checkpoint(state):
    CHECKPOINT.parent.mkdir(parents=True, exist_ok=True)
    CHECKPOINT.write_text(json.dumps(state, indent=2))


def main():

    max_trials = 12

    cfg = config.load(strict=False)
    adapter = get_adapter(cfg)

    budget_thb = 150.0
    instance = "e2-standard-4"

    rate = costs.hourly_rate(
        cfg.provider,
        instance,
        spot=True,
    )

    print(f"Spot rate: {rate:.2f} THB/hour")
    print(f"Budget: {budget_thb:.2f} THB")

    state = load_checkpoint()
    trials = grid()

    for i, params in enumerate(trials[:max_trials]):
        key = json.dumps(params, sort_keys=True)

        if key in state["completed"]:
            print(f"Trial {i}: already completed, skipping.")
            continue

        if state["spent_thb"] >= budget_thb:
            print("Budget exhausted.")
            break

        run_name = f"remote-trial-{i:02d}"

        args = {
            **params,
            "seed": 20260101,
            "experiment": "itcs355-lab2",
            "run_name": run_name,
            "blob_uri": cfg.blob_uri,
            "metrics_out": "/tmp/metrics.json",
            "git_commit": "b21c82ef7171fed28533b52eca4cdfa20a57f1a0",
        }

        print()
        print("=" * 60)
        print(f"Trial {i + 1}/12")
        print(f"Parameters: {params}")
        print(f"Run name: {run_name}")
        print("=" * 60)

        started = time.perf_counter()

        job_id = adapter.submit_training(
            IMAGE_URI,
            args,
        )

        print(f"JOB_ID={job_id}")

        result = adapter.wait_training(job_id)

        elapsed_s = time.perf_counter() - started
        elapsed_h = elapsed_s / 3600.0
        trial_cost = elapsed_h * rate

        # Get metrics produced by the remote training container
        bucket_name, prefix = cfg.blob_uri[5:].split("/", 1)

        from google.cloud import storage

        storage_client = storage.Client(project=cfg.project_id)
        bucket = storage_client.bucket(bucket_name)

        metrics_path = f"{prefix}/vertex-jobs/{run_name}/metrics.json"
        metrics_blob = bucket.blob(metrics_path)

        remote_metrics = json.loads(
            metrics_blob.download_as_bytes().decode("utf-8")
        )

        print(f"State: {result['state']}")
        print(f"Duration: {elapsed_s:.2f} seconds")
        print(f"Estimated cost: {trial_cost:.4f} THB")

        state["spent_thb"] += trial_cost

        state["trials"].append({
            "trial": i,
            "run_name": run_name,
            "job_id": job_id,
            "run_id": remote_metrics["run_id"],
            "params": params,
            "seed": args["seed"],
            "instance": instance,
            "spot": True,
            "duration_s": round(elapsed_s, 3),
            "cost_thb": round(trial_cost, 4),
            "val_roc_auc": remote_metrics["val_roc_auc"],
            "val_pr_auc": remote_metrics["val_pr_auc"],
            "test_roc_auc": remote_metrics["test_roc_auc"],
            "test_pr_auc": remote_metrics["test_pr_auc"],
            "data_fingerprint": remote_metrics["data_fingerprint"],
            "image_digest": IMAGE_URI.split("@")[-1],
            "success": result["success"],
        })

        if result["success"]:
            state["completed"].append(key)

        save_checkpoint(state)

        print(f"Cumulative cost: {state['spent_thb']:.4f} THB")

    print()
    print("=" * 60)
    print("REMOTE TUNING COMPLETE")
    print(f"Spent: {state['spent_thb']:.4f} / {budget_thb:.2f} THB")
    print(f"Completed: {len(state['completed'])} / {len(trials)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
