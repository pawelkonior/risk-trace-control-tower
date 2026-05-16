import http from "k6/http";
import { check, sleep } from "k6";
import { Rate, Trend } from "k6/metrics";

const errorRate = new Rate("errors");
const calcDuration = new Trend("rwa_calculation_duration", true);

// Stress test — find the breaking point
// Run manually: k6 run --env TARGET_URL=https://api.yourdomain.com k6/stress-test.js
export const options = {
  scenarios: {
    stress: {
      executor: "ramping-vus",
      startVUs: 0,
      stages: [
        { duration: "2m", target: 50 },
        { duration: "5m", target: 50 },
        { duration: "2m", target: 100 },
        { duration: "5m", target: 100 },
        { duration: "2m", target: 200 },
        { duration: "5m", target: 200 },
        { duration: "5m", target: 0 },
      ],
      gracefulRampDown: "60s",
    },
  },
  thresholds: {
    // Softer thresholds — we want to see where it breaks, not fail fast
    http_req_duration: ["p(95)<10000"],
    http_req_failed: ["rate<0.10"],
    errors: ["rate<0.10"],
  },
};

const BASE_URL = __ENV.TARGET_URL || "http://localhost:8000";

export default function () {
  const res = http.get(`${BASE_URL}/v1/health`);
  check(res, { "status 200": (r) => r.status === 200 });
  errorRate.add(res.status !== 200);
  calcDuration.add(res.timings.duration);
  sleep(0.1);

  const exp = http.get(`${BASE_URL}/v1/exposures`, {
    headers: { Accept: "application/json" },
    timeout: "10s",
  });
  check(exp, { "exposures not 5xx": (r) => r.status < 500 });
  errorRate.add(exp.status >= 500);

  sleep(0.5);
}

export function handleSummary(data) {
  return {
    "k6-stress-summary.json": JSON.stringify(data, null, 2),
  };
}
