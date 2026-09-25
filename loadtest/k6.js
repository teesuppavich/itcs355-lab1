// ITCS355 Lab 3 — load test.
//
// k6 run -e TARGET=http://localhost:8080/predict -e VUS=10 loadtest/k6.js

import http from 'k6/http';
import { check } from 'k6';
import { Trend, Rate } from 'k6/metrics';

const latency = new Trend('predict_latency_ms');
const failures = new Rate('predict_failures');

export const options = {
  vus: Number(__ENV.VUS || 10),
  duration: __ENV.DURATION || '60s',

  summaryTrendStats: [
    'avg',
    'min',
    'med',
    'max',
    'p(90)',
    'p(95)',
    'p(99)',
  ],

  thresholds: {
    'predict_latency_ms': ['p(95)<200'],
    'predict_failures': ['rate<0.01'],
  },
};

const payload = JSON.stringify({
  temp_c: 78.4,
  vibration_mm_s: 3.1,
  pressure_kpa: 315.2,
  hours_since_service: 4200,
  load_pct: 68.0,
  ambient_humidity: 55.0,
});

export default function () {
  const res = http.post(__ENV.TARGET, payload, {
    headers: { 'Content-Type': 'application/json' },
  });

  latency.add(res.timings.duration);
  failures.add(res.status !== 200);

  check(res, {
    'status is 200': (r) => r.status === 200,
    'probability present': (r) =>
      r.status === 200 && r.json('probability') !== undefined,
    'version reported': (r) =>
      r.headers['X-Model-Version'] !== undefined,
  });
}
