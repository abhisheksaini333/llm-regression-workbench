import React from "react";
import { render, screen, fireEvent, cleanup } from "@testing-library/react";
import { afterEach, expect, test } from "vitest";
import { Comparison } from "../src/Comparison";
afterEach(cleanup);
const data: any = {
  overall: {
    baseline: 0.25,
    candidate: 0.75,
    delta: 0.5,
    interval: { low: 0.2, high: 0.8 },
  },
  gate: {
    passed: false,
    failures: [{ slice: "critical", reason: "quality regression" }],
  },
  operations: {
    candidate: { p95_ms: 40, total_tokens: 20, usage_kinds: ["tokens"] },
  },
  slices: { critical: { count: 1, baseline: 1, candidate: 0, delta: -1 } },
  tasks: { tool: { count: 1, baseline: 1, candidate: 0, delta: -1 } },
  cases: [
    {
      case_id: "bad",
      delta: -1,
      baseline: {
        score: 1,
        output: "safe",
        task: "tool",
        slices: ["critical"],
      },
      candidate: { score: 0, output: "unsafe" },
    },
  ],
};
test("gate stays blocked when aggregate improves and critical filter links to case", () => {
  render(<Comparison data={data} />);
  expect(screen.getByText("Release blocked")).toBeTruthy();
  expect(screen.getByText("+50.0 pp")).toBeTruthy();
  fireEvent.click(screen.getByRole("button", { name: "critical" }));
  expect(screen.getByText("bad")).toBeTruthy();
  expect(screen.getByText("unsafe")).toBeTruthy();
});
