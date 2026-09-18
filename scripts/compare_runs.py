from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        default="reports/tune_remote_checkpoint.json",
    )
    parser.add_argument(
        "--metric",
        default="val_roc_auc",
    )
    parser.add_argument(
        "--out",
        default="reports/lab2-comparison.md",
    )
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        state = json.load(f)

    trials = [
        t for t in state.get("trials", [])
        if t.get("success", False)
    ]

    if not trials:
        raise RuntimeError("No successful trials found.")

    rows = []

    for t in trials:
        params = t["params"]

        rows.append({
            "trial": t["trial"],
            "run_id": t["run_id"],
            "job_id": t["job_id"],
            "n_estimators": params["n_estimators"],
            "max_depth": params["max_depth"],
            "min_samples_leaf": params["min_samples_leaf"],
            "seed": t["seed"],
            "instance": t["instance"],
            "spot": t["spot"],
            "duration_s": t["duration_s"],
            "cost_thb": t["cost_thb"],
            "val_roc_auc": t["val_roc_auc"],
            "val_pr_auc": t["val_pr_auc"],
            "test_roc_auc": t["test_roc_auc"],
            "test_pr_auc": t["test_pr_auc"],
            "data_fingerprint": t["data_fingerprint"],
            "image_digest": t["image_digest"],
        })

    table = pd.DataFrame(rows)

    table = table.sort_values(
        args.metric,
        ascending=False,
    ).reset_index(drop=True)

    best = table.iloc[0]

    total_cost = table["cost_thb"].sum()
    monthly_cost = float(best["cost_thb"])

    lines = []

    lines.append("# Lab 2 — Remote Hyperparameter Comparison")
    lines.append("")
    lines.append(f"**Trials:** {len(table)}")
    lines.append(
        f"**Total estimated tuning cost:** {total_cost:.4f} THB"
    )
    lines.append(
        f"**Instance:** {table.iloc[0]['instance']}"
    )
    lines.append(
        f"**Spot:** {'Yes' if table.iloc[0]['spot'] else 'No'}"
    )
    lines.append("")

    lines.append("## Trial results")
    lines.append("")
    lines.append(
        table.to_markdown(
            index=False,
            floatfmt=".4f",
        )
    )
    lines.append("")

    lines.append("## Selected configuration")
    lines.append("")

    lines.append(
        "Selected by highest validation ROC-AUC: "
        f"Trial {int(best['trial'])} "
        f"(`n_estimators={int(best['n_estimators'])}`, "
        f"`max_depth={int(best['max_depth'])}`, "
        f"`min_samples_leaf={int(best['min_samples_leaf'])}`)."
    )
    lines.append("")

    lines.append(
        f"- Validation ROC-AUC: {best['val_roc_auc']:.4f}"
    )
    lines.append(
        f"- Test ROC-AUC: {best['test_roc_auc']:.4f}"
    )
    lines.append(
        f"- Training cost: {best['cost_thb']:.4f} THB"
    )
    lines.append("")

    lines.append("## Selection justification")
    lines.append("")

    lines.append(
        f"The selected configuration was chosen because it achieved "
        f"the highest validation ROC-AUC among the {len(table)} "
        f"remote trials. Its validation ROC-AUC was "
        f"{best['val_roc_auc']:.4f}, while the test ROC-AUC was "
        f"{best['test_roc_auc']:.4f}. "
        f"The tuning study used the same seed (20260101) for all "
        f"configurations, so seed variance cannot be estimated from "
        f"this study alone. "
        f"The selected configuration cost {best['cost_thb']:.4f} THB "
        f"per training run, so one monthly retraining run would be "
        f"approximately {monthly_cost:.4f} THB at the same estimated "
        f"Spot rate and duration. "
        f"This choice could be wrong if the validation split does not "
        f"represent future production data, or if another seed produces "
        f"a meaningfully different result. "
        f"A future check with multiple seeds and newer data could "
        f"change the selected configuration."
    )
    lines.append("")

    lines.append("## Lineage")
    lines.append("")

    lines.append(
        f"- Data fingerprint: `{best['data_fingerprint']}`"
    )
    lines.append(
        f"- Image digest: `{best['image_digest']}`"
    )
    lines.append(
        f"- MLflow run ID: `{best['run_id']}`"
    )
    lines.append(
        f"- Training job ID: `{best['job_id']}`"
    )
    lines.append(
        f"- Seed: `{int(best['seed'])}`"
    )

    Path(args.out).write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print(
        f"wrote {args.out} ({len(table)} trials)"
    )


if __name__ == "__main__":
    main()
