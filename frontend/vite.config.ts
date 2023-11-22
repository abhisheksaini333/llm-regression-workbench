import { defineConfig } from "vitest/config";
export default defineConfig({
  server: { proxy: { "/api": "http://127.0.0.1:8765" } },
  test: {
    environment: "jsdom",
    include: ["tests/**/*.test.tsx"],
    threads: false,
  },
});
