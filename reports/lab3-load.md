# ITCS355 Lab 3 — Load Test

## Latency target

The target was defined before measurement: **p95 < 200 ms**.

The test used k6 against the local FastAPI serving service at `http://localhost:8080/predict`, with 60 seconds per concurrency level.

## Results

| VUs | Requests | Throughput (req/s) | p50 (ms) | p95 (ms) | p99 (ms) | Error rate |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 703 | 11.716 | 86.76 | 104.81 | 124.72 | 0% |
| 10 | 658 | 10.904 | 915.68 | 1105.51 | 1180.79 | 0% |
| 50 | 808 | 13.046 | 3919.41 | 4560.32 | 4857.48 | 0% |

## Breaking point

At **1 VU**, the p95 target was met. At **10 VUs**, p95 exceeded the 200 ms target, so the breaking point was **between 1 and 10 VUs** in the tested levels. No errors were observed at any tested level.

## Reproduction


- `make serve`
- `make loadtest`
