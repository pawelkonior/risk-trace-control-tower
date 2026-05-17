import http from "k6/http";
import { check, sleep, group } from "k6";
import { Rate, Trend, Counter } from "k6/metrics";

const errorRate = new Rate("errors");
const calcDuration = new Trend("rwa_calculation_duration", true);
const rwaRequests = new Counter("rwa_requests_total");

export const options = {
  scenarios: {
    ramp_up: {
      executor: "ramping-vus",
      startVUs: 0,
      stages: [
        { duration: "2m", target: 10 },
        { duration: "5m", target: 10 },
        { duration: "2m", target: 25 },
        { duration: "5m", target: 25 },
        { duration: "2m", target: 0 },
      ],
      gracefulRampDown: "30s",
    },
  },
  thresholds: {
    // SLO: p95 < 2s (matches Prometheus alert RWACalculationSLOBreach)
    http_req_duration: ["p(95)<2000", "p(99)<5000"],
    http_req_failed: ["rate<0.01"],
    errors: ["rate<0.01"],
    rwa_calculation_duration: ["p(95)<2000"],
  },
};

const BASE_URL = __ENV.TARGET_URL || "http://localhost:8000";

const HEADERS = {
  "Content-Type": "application/json",
  Accept: "application/json",
};

export default function () {
  group("health", () => {
    const res = http.get(`${BASE_URL}/v1/health`);
    check(res, { "health 200": (r) => r.status === 200 });
    errorRate.add(res.status !== 200);
  });

  sleep(0.2);

  group("rwa_exposures", () => {
    const res = http.get(`${BASE_URL}/v1/exposures`, { headers: HEADERS });
    check(res, {
      "exposures 2xx": (r) => r.status >= 200 && r.status < 300,
      "exposures <2s": (r) => r.timings.duration < 2000,
      "content-type json": (r) =>
        r.headers["Content-Type"]?.includes("application/json"),
    });
    calcDuration.add(res.timings.duration);
    rwaRequests.add(1);
    errorRate.add(res.status >= 500);
  });

  sleep(0.5);

  group("rwa_assets", () => {
    const res = http.get(`${BASE_URL}/v1/assets`, { headers: HEADERS });
    check(res, {
      "assets 2xx or 404": (r) =>
        (r.status >= 200 && r.status < 300) || r.status === 404,
      "assets <2s": (r) => r.timings.duration < 2000,
    });
    errorRate.add(res.status >= 500);
    rwaRequests.add(1);
  });

  sleep(1);
}

export function handleSummary(data) {
  return {
    "k6-load-summary.json": JSON.stringify(data, null, 2),
  };
}
