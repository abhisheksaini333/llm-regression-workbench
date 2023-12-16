FROM node:16.16.0-bullseye-slim AS web
WORKDIR /web
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci --no-audit --no-fund
COPY frontend/ ./
RUN npm run build

FROM python:3.10.9-slim-bullseye
WORKDIR /app
COPY regression_workbench/ ./regression_workbench/
COPY scripts/ ./scripts/
COPY fixtures/ ./fixtures/
COPY --from=web /web/dist ./frontend/dist
RUN mkdir /data && chown 65532:65532 /data
USER 65532:65532
EXPOSE 8765
HEALTHCHECK --interval=15s --timeout=3s CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8765/api/runs',timeout=2)"
CMD ["python", "-m", "regression_workbench.cli", "serve", "--host", "0.0.0.0", "--db", "/data/runs.db", "--policy", "fixtures/gate-policy.json"]
