import http from "k6/http";
import { check, sleep } from "k6";
import { Rate, Trend } from "k6/metrics";

const errorRate = new Rate("errors");
const calcDuration = new Trend("rwa_calculation_duration", true);

export const options = {
  vus: 1,
  iterations: 10,
  thresholds: {
    http_req_failed: ["rate<0.01"],
    http_req_duration: ["p(95)<2000"],
    errors: ["rate<0.01"],
  },
};

const BASE_URL = __ENV.TARGET_URL || "http://localhost:8000";

export default function () {
  // Health check
  const health = http.get(`${BASE_URL}/v1/health`);
  check(health, {
    "health status 200": (r) => r.status === 200,
    "health response time <500ms": (r) => r.timings.duration < 500,
  });
  errorRate.add(health.status !== 200);

  sleep(0.5);

  // RWA exposures endpoint
  const exposures = http.get(`${BASE_URL}/v1/exposures`, {
    headers: { Accept: "application/json" },
  });
  check(exposures, {
    "exposures status 200 or 404": (r) =>
      r.status === 200 || r.status === 404,
    "exposures response time <2000ms": (r) => r.timings.duration < 2000,
  });
  calcDuration.add(exposures.timings.duration);
  errorRate.add(exposures.status >= 500);

  sleep(1);
}

export function handleSummary(data) {
  return {
    "k6-smoke-summary.json": JSON.stringify(data, null, 2),
    stdout: textSummary(data, { indent: " ", enableColors: false }),
  };
}

function textSummary(data, opts) {
  const { metrics } = data;
  const lines = [
    `\nSmoke Test Summary`,
    `==================`,
    `http_req_duration p(95): ${metrics.http_req_duration?.values?.["p(95)"]?.toFixed(2)}ms`,
    `http_req_failed rate:    ${(metrics.http_req_failed?.values?.rate * 100)?.toFixed(2)}%`,
    `errors rate:             ${(metrics.errors?.values?.rate * 100)?.toFixed(2)}%`,
    `iterations:              ${metrics.iterations?.values?.count}`,
  ];
  return lines.join("\n");
}
