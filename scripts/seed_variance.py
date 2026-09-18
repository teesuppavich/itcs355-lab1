"""Lab 2 — seed variance check for the chosen config (trial-00).

Run:  python scripts/seed_variance.py

Re-submits n_estimators=100, max_depth=4, min_samples_leaf=1 to Vertex AI with
several seeds, to measure how much test_roc_auc moves from randomness alone.
"""
from __future__ import annotations

import sys
from pathlib import Path as _Path
sys.path.insert(0, str(_Path(__file__).resolve().parents[1]))

import json
import statistics
import time
from pathlib import Path

from src import config
from cloudlayer.factory import get_adapter

IMAGE_URI = (
    "asia-southeast1-docker.pkg.dev/itcs355-6688097/itcs355/itcs355-lab1"
    "@sha256:c45c3829d435b288e25da7bb38d896113fd8ab1d5a7165f2f1c04ae8a2635f47"
)
BASE_PARAMS = {"n_estimators": 100, "max_depth": 4, "min_samples_leaf": 1}
SEEDS = [1, 2, 3, 42]  # 20260101 already have from trial-00, prefilled below

CHECKPOINT = Path("reports/seed_variance_checkpoint.json")

# Already run as trial-00 during the 12-trial study. Prefilled so it counts
# in the variance summary without re-submitting.
TRIAL_00 = {
    "seed": 20260101,
    "job_id": "projects/581504912225/locations/asia-southeast1/customJobs/763473111659053056",
    "run_id": "bd33de7d808a441a90e4eadbbeceada5",
    "val_roc_auc": 0.8424390505441984,
    "test_roc_auc": 0.8518038253137591,
}


def load_checkpoint() -> dict:
    if CHECKPOINT.exists():
        return json.loads(CHECKPOINT.read_text())
    return {"results": [TRIAL_00]}


def save_checkpoint(state: dict) -> None:
    CHECKPOINT.parent.mkdir(parents=True, exist_ok=True)
    CHECKPOINT.write_text(json.dumps(state, indent=2))


def main() -> None:
    cfg = config.load()
    adapter = get_adapter(cfg)
    state = load_checkpoint()
    done_seeds = {r["seed"] for r in state["results"]}
    bucket_path = cfg.blob_uri.removeprefix("gs://")

    for seed in SEEDS:
        if seed in done_seeds:
            print(f"seed {seed}: already done, skipping")
            continue

        run_name = f"seed-var-{seed}"
        gcs_metrics = f"gs://{bucket_path}/vertex-jobs/{run_name}/metrics.json"
        metrics_out = f"/gcs/{bucket_path}/vertex-jobs/{run_name}/metrics.json"

        started = time.perf_counter()
        job_id = adapter.submit_training(IMAGE_URI, {
            **BASE_PARAMS,
            "seed": seed,
            "metrics_out": metrics_out,
        })
        print(f"seed {seed}: submitted {job_id}")

        result = adapter.wait_training(job_id)
        elapsed = time.perf_counter() - started
        print(f"seed {seed}: {result['state']} in {elapsed:.1f}s")

        if not result["success"]:
            print(f"seed {seed}: FAILED, skipping")
            continue

        local_metrics = Path(f"reports/remote-trials/{run_name}.json")
        adapter.download(gcs_metrics, str(local_metrics))
        metrics = json.loads(local_metrics.read_text())

        state["results"].append({"seed": seed, "job_id": job_id, **metrics})
        save_checkpoint(state)

    print("\n=== seed variance summary ===")
    aucs = [r["test_roc_auc"] for r in state["results"]]
    print(f"seeds: {[r['seed'] for r in state['results']]}")
    print(f"test_roc_auc: {[round(a, 4) for a in aucs]}")
    print(f"mean={statistics.mean(aucs):.4f}  stdev={statistics.pstdev(aucs):.4f}  "
          f"range={max(aucs) - min(aucs):.4f}")


if __name__ == "__main__":
    main()
