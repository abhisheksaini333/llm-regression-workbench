import React from "react";
import {
  render,
  screen,
  fireEvent,
  waitFor,
  cleanup,
} from "@testing-library/react";
import { afterEach, expect, test, vi } from "vitest";
import { Review } from "../src/Review";
afterEach(() => {
  cleanup();
  vi.restoreAllMocks();
});
test("review presents neutral choices and persists the selected vote", async () => {
  const onSave = vi.fn().mockResolvedValue({ saved: true, revision: 1 });
  render(
    <Review
      pair={{
        case_id: "case",
        A: "answer one",
        B: "answer two",
        prompt: "Which?",
        revision: 0,
        reviewed: false,
      }}
      onSave={onSave}
    />
  );
  expect(screen.queryByText("BASELINE")).toBeNull();
  fireEvent.click(screen.getByRole("button", { name: "Prefer A" }));
  await waitFor(() => expect(onSave).toHaveBeenCalledWith("A", "", 0));
  expect(await screen.findByText("Review saved")).toBeTruthy();
});
