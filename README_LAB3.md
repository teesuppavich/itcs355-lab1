# ITCS355 Lab 3 — Serving and Load Testing

## Overview

This README documents the experiments and results for ITCS355 Lab 3.

The existing `README.md` for Lab 1 and Lab 2 is not modified.

## Deployment

- Region: `asia-southeast1`
- Endpoint: `itcs355-lab3-endpoint`
- Endpoint ID: `4583056934663356416`
- Model ID: `5746131329641086976`
- Serving image: `itcs355-lab3-serving:v2`
- Machine type: `e2-standard-4`
- Minimum replicas: 1
- Maximum replicas: 1

The deployed endpoint was verified with three smoke-test predictions.

The Lab 2 registered model was not modified.

## Latency Target

The latency target was defined before testing:

**p95 < 200 ms**


## Concurrency Experiment

The k6 test used 60-second runs at 1, 10, and 50 virtual users (VUs).

| VUs | Requests | Throughput (req/s) | Avg (ms) | p50 (ms) | p95 (ms) | p99 (ms) | Error rate |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 703 | 11.716 | 85.02 | 86.76 | 104.81 | 124.72 | 0% |
| 10 | 658 | 10.904 | 914.64 | 915.68 | 1105.51 | 1180.79 | 0% |
| 50 | 808 | 13.046 | 3816.67 | 3919.41 | 4560.32 | 4857.48 | 0% |

At 1 VU, the p95 target was met. At 10 and 50 VUs, the p95 target was exceeded even though the request error rate remained 0%.

The tested breaking point can therefore be localized to **between 1 and 10 VUs**. More intermediate concurrency levels would be required to identify the exact VU at which the target is crossed.

The load-test script is `loadtest/k6.js`.

Full test command:

```bash
make loadtest
```

## Batch Experiment

The batch experiment compared one `/predict/batch` request containing 100 rows with 100 sequential `/predict` requests containing the same rows.

Five iterations were measured for each method.

| Method | Requests per iteration | Avg total time for 100 rows | p95 |
|---|---:|---:|---:|
| 100 single `/predict` calls | 100 | 8535.4 ms | 8986 ms |
| One `/predict/batch` call | 1 | 105.6 ms | 125.8 ms |

The batch request reduced total elapsed time by approximately **98.8%**, or about **80.8x faster** in this sequential comparison.

This comparison is specifically between 100 sequential single requests and one batch request; it does not represent 100 concurrent requests.

Commands:

```bash
k6 run -e MODE=single -e TARGET=http://localhost:8080/predict loadtest/batch_compare.js
k6 run -e MODE=batch -e TARGET=http://localhost:8080/predict/batch loadtest/batch_compare.js
```

The experiment script is `loadtest/batch_compare.js`.

## Payload-Size Experiment

The request schema rejects unknown fields, so payload size was increased by using a longer numeric representation while keeping the value valid.

Payloads from approximately 10 KB to 1 MB were tested.

| Payload size | Avg latency (ms) | p95 (ms) |
|---:|---:|---:|
| 9.9 KB | 78.51 | 94.26 |
| 49.0 KB | 85.43 | 89.54 |
| 97.8 KB | 101.01 | 96.65 |
| 244.3 KB | 78.67 | 91.70 |
| 488.4 KB | 88.53 | 99.41 |
| 976.7 KB | 87.27 | 98.10 |

No clear serialization-dominated region was observed up to approximately 1 MB.

Therefore, within the tested range, there was no measured payload-size breaking point.

## Instance-Size Experiment

The Vertex endpoint was first measured using `e2-standard-4`, then the same registered model was deployed using `e2-standard-8`.

Both tests used 20 sequential prediction requests after one warm-up request.

### e2-standard-4

| Metric | Result |
|---|---:|
| Average | 583.68 ms |
| p50 | 584.91 ms |
| p95 | 652.28 ms |
| Minimum | 480.80 ms |
| Maximum | 673.38 ms |

### e2-standard-8

| Metric | Result |
|---|---:|
| Average | 597.66 ms |
| p50 | 589.42 ms |
| p95 | 704.77 ms |
| Minimum | 461.86 ms |
| Maximum | 763.67 ms |

In this experiment, `e2-standard-8` did not reduce latency. Average latency increased by about 2.4%, while p95 increased by about 8.0% compared with `e2-standard-4`.

The official Vertex AI pricing table lists `e2-standard-8` at approximately twice the hourly machine price of `e2-standard-4`. Therefore, the relative machine-cost change is approximately **+100%**.

No unverified THB price was added to `src/costs.py`.

After the experiment, traffic was returned to `e2-standard-4` and the temporary `e2-standard-8` deployment was undeployed.


## Overall Findings

1. The p95 latency target of 200 ms was met at 1 VU but exceeded at 10 and 50 VUs.
2. The tested concurrency breaking point lies between 1 and 10 VUs.
3. Batching 100 rows was substantially faster than sending 100 sequential single requests.
4. No clear serialization-dominated region was observed for payloads up to approximately 1 MB.
5. Increasing the Vertex instance from `e2-standard-4` to `e2-standard-8` did not improve latency in the measured workload, while the machine cost is approximately twice as high.
6. The final endpoint configuration was restored to `e2-standard-4`.

## Reproduction Commands

Start the local service:

```bash
make serve
```

Run the concurrency test:

```bash
make loadtest
```

Run the batch comparison:

```bash
k6 run -e MODE=single -e TARGET=http://localhost:8080/predict loadtest/batch_compare.js
k6 run -e MODE=batch -e TARGET=http://localhost:8080/predict/batch loadtest/batch_compare.js
```

Run the Vertex smoke test:

```bash
PYTHONPATH=. python scripts/smoke.py --endpoint "projects/581504912225/locations/asia-southeast1/endpoints/4583056934663356416"
```

The final endpoint should use the Lab 3 model with `e2-standard-4`.

## Canary and Rollback

Baseline model: `5746131329641086976`; canary model: `4937453721551372288`.

Traffic was split at 90% baseline / 10% canary, and both deployments had one available e2-standard-4 replica.

Detection used aggregate **log loss** only, without using `model_version`; baseline reference was 0.270641 and the detection threshold was 0.271640.

At 250 requests log loss was 0.266780; at 500 requests it reached 0.280905, so degradation was detected after **17.3 seconds** at 500 requests.

Detection could be faster with a shorter monitoring window, a more sensitive predefined threshold, or more frequent labelled online evaluation.

At 50/50 traffic, the degraded model would contribute a larger share of requests, so the aggregate metric would be expected to move toward the canary behaviour more quickly.

Rollback evidence: `2026-09-25T08:46:00Z` rollback started and `2026-09-25T08:46:02Z` ended; the endpoint then showed baseline deployment `1602923026553241600 = 100%` traffic.

The canary deployment was subsequently undeployed, leaving only the baseline deployment active.

## Cost per 1,000 Predictions

Instance hourly rate: **6.4 THB/hour** for e2-standard-4. Measured throughput at the target-meeting 1-VU level: **11.716 req/s**.

Using the project cost formula, cost per 1,000 predictions is **3.0348 THB at 5% utilisation, 0.6070 THB at 25% utilisation, and 0.1897 THB at 80% utilisation**.

The stated working assumption is **25% utilisation**, giving **0.6070 THB per 1,000 predictions**; utilisation is the most fragile part of this estimate because an always-on endpoint still incurs hourly cost when lightly used.

Using the Lab scaffold assumption that a batch run costs 0.5 hours of endpoint compute, the break-even point is approximately **0.0017407 req/s, or 150 requests/day**; below this volume, scheduled batch inference is cheaper than keeping the endpoint warm.
