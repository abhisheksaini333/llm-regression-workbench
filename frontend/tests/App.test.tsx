import React from "react";
import { render, screen, cleanup } from "@testing-library/react";
import { afterEach, expect, test, vi } from "vitest";
import { App } from "../src/App";
afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
});
test("empty workspace explains how to add evaluation runs", async () => {
  vi.stubGlobal(
    "fetch",
    vi.fn().mockResolvedValue({ ok: true, json: async () => [] })
  );
  render(<App />);
  expect(
    await screen.findByText("Start with two evaluation runs")
  ).toBeTruthy();
});
test("server errors surface as recoverable messages", async () => {
  vi.stubGlobal(
    "fetch",
    vi
      .fn()
      .mockResolvedValue({
        ok: false,
        json: async () => ({ error: "Database unavailable" }),
      })
  );
  render(<App />);
  expect(await screen.findByRole("alert")).toHaveProperty(
    "textContent",
    "Database unavailable"
  );
});
