import http from 'k6/http';
import { check } from 'k6';
import { Trend, Rate } from 'k6/metrics';

const singleTotal = new Trend('single_100_total_ms');
const batchTotal = new Trend('batch_100_total_ms');
const failures = new Rate('batch_compare_failures');

export const options = {
  vus: 1,
  iterations: 5,
  summaryTrendStats: [
    'avg',
    'min',
    'med',
    'max',
    'p(95)',
  ],
};

function samplePayload() {
  return {
    temp_c: 78.4,
    vibration_mm_s: 3.1,
    pressure_kpa: 315.2,
    hours_since_service: 4200,
    load_pct: 68.0,
    ambient_humidity: 55.0,
  };
}

export default function () {
  const rows = Array.from({ length: 100 }, samplePayload);

  if (__ENV.MODE === 'batch') {
    const start = Date.now();

    const res = http.post(
      __ENV.TARGET,
      JSON.stringify({ rows: rows }),
      {
        headers: { 'Content-Type': 'application/json' },
      }
    );

    const elapsed = Date.now() - start;
    batchTotal.add(elapsed);

    const ok = check(res, {
      'batch status is 200': (r) => r.status === 200,
    });

    failures.add(!ok);
  } else {
    const start = Date.now();
    let allOk = true;

    for (const row of rows) {
      const res = http.post(
        __ENV.TARGET,
        JSON.stringify(row),
        {
          headers: { 'Content-Type': 'application/json' },
        }
      );

      if (res.status !== 200) {
        allOk = false;
      }
    }

    const elapsed = Date.now() - start;
    singleTotal.add(elapsed);

    failures.add(!allOk);
  }
}
