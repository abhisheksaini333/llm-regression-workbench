import { test, expect } from "@playwright/test";
test("aggregate improvement cannot hide critical failures in the browser", async ({
  page,
}) => {
  await page.goto("/");
  await expect(
    page.getByRole("heading", { name: "Release blocked" })
  ).toBeVisible();
  await expect(page.getByText("+66.7 pp", { exact: true })).toBeVisible();
  await page
    .getByRole("button", { name: "critical", exact: true })
    .first()
    .click();
  await expect(page.getByText("4 examples", { exact: true })).toBeVisible();
  await expect(
    page.getByRole("heading", { name: "extract-1", exact: true })
  ).toBeVisible();
  await page.getByLabel("Regressions only").check();
  await expect(page.getByText("4 examples", { exact: true })).toBeVisible();
});
test("blinded review saves a vote and updates judge disagreement", async ({
  page,
}) => {
  await page.goto("/");
  await page.getByRole("button", { name: "Human review", exact: true }).click();
  await page.getByLabel("Reviewer name").fill("browser-demonstration");
  const card = page.locator(".review-card").first();
  await expect(card.getByText("RESPONSE A")).toBeVisible();
  await card
    .getByLabel("Reason for your preference")
    .fill("Demonstration label used to exercise the disagreement workflow.");
  await card.getByRole("button", { name: "Tie", exact: true }).click();
  await expect(card.getByRole("status")).toHaveText("Review saved");
  await page.getByRole("button", { name: "Refresh analysis" }).click();
  await expect(
    page.getByText("1 reviewed observations", { exact: true })
  ).toBeVisible();
  await expect(
    page.getByText("Judge agreement: 0%", { exact: true })
  ).toBeVisible();
  await page.reload();
  await expect(
    page.getByRole("heading", { name: "Release blocked" })
  ).toBeVisible();
});
test("mobile workspace has no horizontal overflow", async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto("/");
  await expect(
    page.getByRole("heading", { name: "Release blocked" })
  ).toBeVisible();
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= innerWidth
    )
  ).toBe(true);
});
