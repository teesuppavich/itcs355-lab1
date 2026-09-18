# ITCS355 Lab 2 — Hyperparameter Study and Model Registry

## Overview

This lab performs a remote hyperparameter study using Vertex AI. The goal is to compare different model configurations under a fixed compute budget and register the selected model with its training information.

## Hyperparameter Study

The study used 12 remote training trials with three hyperparameters:

* `n_estimators`: 100, 300
* `max_depth`: 4, 8, 12
* `min_samples_leaf`: 1, 5

All trials used the same seed (`20260101`) and the same data version so that the configurations could be compared fairly.

Training was performed on Vertex AI using `e2-standard-4` Spot compute. The total estimated cost of the 12 trials was approximately 1.06 THB, which was below the 150 THB budget.

## Selected Model

The selected configuration was:

* `n_estimators=100`
* `max_depth=4`
* `min_samples_leaf=5`
* Seed: `20260101`

It achieved:

* Validation ROC-AUC: `0.8426`
* Test ROC-AUC: `0.8533`

The selected model was registered in Vertex AI Model Registry as:

* Model ID: `97210022034931712`
* Version: `1`
* Alias: `staging`

The selection was based on validation performance, while also considering the small difference between the top configurations. The selected configuration had a validation ROC-AUC of 0.8426, while another configuration achieved 0.8424. This difference is very small, so the result could change with another seed or a different validation sample.

## Model Lineage

The registered model contains the following lineage information:

| Item               | Value                                                                            |
| ------------------ | -------------------------------------------------------------------------------- |
| Git commit         | `b21c82ef7171fed28533b52eca4cdfa20a57f1a0`                                       |
| Data version       | `422cccb9136e8140`                                                               |
| MLflow run ID      | `4f6a4bd74e64430893d63d035691dce9`                                               |
| Training job ID    | `projects/581504912225/locations/asia-southeast1/customJobs/6825318210099740672` |
| Image digest       | `sha256:0b54b73ddb9f6bd5206e85dd5a4696cad1c1874808ddc59860249b32b34a8296`        |
| Seed               | `20260101`                                                                       |
| Validation ROC-AUC | `0.84259989736441`                                                               |
| Test ROC-AUC       | `0.8532857870606215`                                                             |

## Model Promotion

In a real organization, model promotion should be limited to an authorized ML platform/MLOps owner or model release approver. The person responsible for approving the model should review the evidence before promoting it.

The required evidence should include the model version, Git commit, data version, MLflow run ID, training job ID, container image digest, seed, validation and test metrics, and the hyperparameter comparison report. The model should also pass the registry reload check using held-out data.

## Reload Check

The registered model can be reloaded by its Vertex AI Model Registry version and used to score five held-out rows.

Run:

```bash
PYTHONPATH=. python scripts/reload_check.py \
  --model-id 97210022034931712 \
  --version 1 \
  --rows 5
```

The check successfully retrieved Version 1 from Vertex AI Model Registry and produced predictions for five held-out rows.

## Training Cost

The 12-trial tuning study had an estimated total cost of approximately `1.06 THB`.

The selected configuration cost approximately `0.1359 THB` per training run under the same estimated Spot rate and duration. A monthly retraining run at the same cost would therefore be approximately `0.1359 THB` per month.

## Known Limitation

All tuning trials used the same seed, so seed-to-seed variance was not measured as part of the 12-trial search. A future study using multiple seeds and newer production data could result in a different selected configuration.
