import { expect, test } from "@playwright/test";

const primaryViews = ["Home", "RWA Dashboard", "Data Lineage", "RWA Intelligence Briefing"];

test("shows only working primary views in the sidebar", async ({ page }) => {
  await page.goto("/#/home");

  const primaryNav = page.getByRole("navigation", { name: "Primary" });
  await expect(page).toHaveTitle(/RiskTrace Control Tower/);
  await expect(page.getByRole("heading", { name: "Home" })).toBeVisible();
  await expect(page.getByRole("main").getByRole("img", { name: "RiskTrace Control Tower" })).toBeVisible();
  await expect(primaryNav.getByRole("link")).toHaveText(primaryViews);
});

test("navigates between working views and breadcrumbs", async ({ page }) => {
  await page.goto("/#/home");

  const primaryNav = page.getByRole("navigation", { name: "Primary" });

  await primaryNav.getByRole("link", { name: "RWA Dashboard" }).click();
  await expect(page).toHaveURL(/#\/dashboard$/);
  await expect(page.getByRole("heading", { level: 1, name: "RWA Dashboard" })).toBeVisible();
  await expect(page.getByText("TOTAL RWA", { exact: true })).toBeVisible();
  await page.getByRole("button", { name: "Export Report" }).click();
  await expect(page.getByRole("status")).toContainText("Data is being processed.");

  await primaryNav.getByRole("link", { name: "Data Lineage" }).click();
  await expect(page).toHaveURL(/#\/lineage$/);
  await expect(page.getByRole("heading", { level: 1, name: "Data Lineage" })).toBeVisible();
  await expect(page.getByText("calc-trace-7f3a9b21").first()).toBeVisible();
  await page.getByRole("button", { name: "Legend" }).click();
  await expect(page.getByLabel("Lineage flow legend")).toBeVisible();
  await page.getByRole("button", { name: "Export Lineage Report" }).click();
  await expect(page.getByRole("status")).toContainText(
    "Data is being processed. We will email a...k...@risktrace.com when the task is complete.",
  );

  await primaryNav.getByRole("link", { name: "RWA Intelligence Briefing" }).click();
  await expect(page).toHaveURL(/#\/briefing$/);
  await expect(page.getByRole("heading", { level: 1, name: "5. RWA Intelligence Briefing" })).toBeVisible();
  await expect(page.getByText("Total RWA (Current)")).toBeVisible();
  await page.getByRole("button", { name: "Export Board Pack" }).first().click();
  await expect(page.getByRole("status")).toContainText("Data is being processed.");

  await page.getByRole("navigation", { name: "Breadcrumb" }).getByRole("link", { name: "RWA Dashboard" }).click();
  await expect(page).toHaveURL(/#\/dashboard$/);

  await page.getByRole("navigation", { name: "Breadcrumb" }).getByRole("link", { name: "Home" }).click();
  await expect(page).toHaveURL(/#\/home$/);
  await expect(page.getByRole("heading", { name: "Home" })).toBeVisible();
});

test("opens top bar controls with Postgres-backed data", async ({ page }) => {
  await page.goto("/#/home");

  await page.getByRole("button", { name: /Reporting Date/ }).click();
  const calendar = page.getByLabel("Reporting calendar");
  await expect(calendar).toBeVisible();
  await expect(calendar.getByText("March 2026")).toBeVisible();
  await expect(calendar.getByRole("button", { name: "2026-03-31" })).toBeEnabled();
  await expect(calendar.getByRole("button", { name: "2026-03-30" })).toBeDisabled();

  await page.getByRole("button", { name: "Notifications" }).click();
  await expect(page.getByLabel("Notifications panel")).toContainText("Data quality review");

  await page.getByRole("button", { name: "Help" }).click();
  await expect(page.getByLabel("Help panel")).toContainText("RWA Dashboard");
  await page.getByRole("button", { name: /RWA Dashboard/ }).click();
  await expect(page.getByRole("status")).toContainText("Help topic opened.");

  await page.getByRole("button", { name: "AK" }).click();
  await expect(page.getByLabel("User menu")).toContainText("Preferences");
  await page.getByRole("button", { name: /Preferences/ }).click();
  await expect(page.getByRole("status")).toContainText("User preferences opened.");

  await page.getByRole("button", { name: "Search" }).click();
  await page.getByPlaceholder("Search metrics, exposures, traces").fill("capital");
  await expect(page.getByLabel("Search panel")).toContainText("Capital Buffer");
});

test("changes dashboard filters, tabs and chart controls", async ({ page }) => {
  await page.goto("/#/dashboard");
  const totalRwaCard = page.locator(".metric-card").filter({ hasText: "TOTAL RWA" });
  const baseTotalRwa = await totalRwaCard.textContent();

  await expect(page.getByRole("heading", { level: 1, name: "RWA Dashboard" })).toBeVisible();

  await page.getByRole("button", { name: "MTD" }).click();
  await expect(page.getByRole("status")).toContainText("Dashboard period applied.");
  await expect.poll(() => totalRwaCard.textContent()).not.toBe(baseTotalRwa);

  await page.getByRole("button", { name: /Scenario Base Case/ }).click();
  await page.getByRole("menuitem", { name: "Stress" }).click();
  await expect(page.getByRole("button", { name: /Scenario Stress/ })).toBeVisible();
  await expect(page.getByRole("status")).toContainText("Dashboard filter applied.");

  await page.getByRole("button", { name: /Business Unit All/ }).click();
  await page.getByRole("menuitem", { name: "Corporate Banking" }).click();
  await expect(page.getByRole("button", { name: /Business Unit Corporate Banking/ })).toBeVisible();

  await page.getByRole("button", { name: /Currency PLN/ }).click();
  await page.getByRole("menuitem", { name: "EUR" }).click();
  await expect(page.getByRole("button", { name: /Currency EUR/ })).toBeVisible();
  await expect(totalRwaCard).toContainText("EUR");

  await page.getByRole("button", { name: "Reset Filters" }).click();
  await expect(page.getByRole("button", { name: /Scenario Base Case/ })).toBeVisible();
  await expect(page.getByRole("button", { name: /Business Unit All/ })).toBeVisible();
  await expect(page.getByRole("button", { name: /Currency PLN/ })).toBeVisible();
  await expect.poll(() => totalRwaCard.textContent()).toBe(baseTotalRwa);

  await page.locator(".exposure-donut-card").getByRole("button", { name: /Corporate/ }).click();
  await expect(page.locator(".exposure-donut-card .donut-center")).toContainText("Corporate");

  await page.getByRole("button", { name: "Collapse navigation" }).click();
  await expect(page.getByRole("button", { name: "Expand navigation" })).toBeVisible();
});

test("switches lineage and briefing controls", async ({ page }) => {
  test.setTimeout(120_000);

  await page.goto("/#/lineage");

  await page.getByRole("button", { name: "Table" }).click();
  await expect(page.getByRole("columnheader", { name: "Primary Evidence" })).toBeVisible();
  await page.getByRole("button", { name: "Graph" }).click();
  await expect(page.getByLabel("Calculation lineage graph")).toBeVisible();
  await page.getByRole("button", { name: "Copy Calculation Trace ID" }).click();
  await expect(page.getByRole("status")).toContainText("Lineage value copied.");
  await page.getByRole("button", { name: "Download All Artifacts" }).click();
  await expect(page.getByRole("status")).toContainText("a...k...@risktrace.com");
  await page.getByRole("button", { name: "View Full Upstream Lineage" }).click();
  await expect(page.getByRole("status")).toContainText("Data is being processed.");

  await page.goto("/#/briefing");
  await expect(page.getByRole("heading", { level: 1, name: "5. RWA Intelligence Briefing" })).toBeVisible();
  await expect(page.getByRole("button", { name: "Explain RWA Movement" })).toBeVisible();
  await expect(page.getByRole("button", { name: "Generate Board Commentary" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "AI Executive Commentary" })).toBeVisible();
  await expect(page.getByRole("button", { name: "Regenerate" })).toBeVisible({
    timeout: 90_000,
  });
  await expect(page.getByRole("tablist", { name: "Commentary views" })).toBeVisible();
  await expect(page.locator(".ai-commentary-panel")).toContainText("Commentary generated on");
  await page.getByRole("tab", { name: "CRO View" }).click();
  await expect(page.getByRole("tab", { name: "CRO View" })).toHaveAttribute(
    "aria-selected",
    "true",
  );
  await expect(page.locator(".ai-commentary-panel")).toContainText(/risk|validation|review/i);
  await page.getByRole("button", { name: "Regenerate" }).click();
  await expect(page.getByRole("status")).toContainText("Generating AI Executive Commentary...");
  await expect(page.getByRole("button", { name: "Thinking..." })).toBeDisabled();
  await expect(page.getByRole("button", { name: "Regenerate" })).toBeVisible({
    timeout: 90_000,
  });

  await expect(page.getByRole("heading", { name: "Regulatory Watch" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Data Quality Findings" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Management Action Simulator" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Evidence & Traceability" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Board Pack" })).toBeVisible();
  await expect(page.getByRole("button", { name: "Simulate All" })).toBeDisabled();
});
