# Operating and recovering the local workspace

## Start and stop

Run `python3 scripts/demo.py`, build the frontend, then run `python3 -m regression_workbench.cli serve --policy fixtures/gate-policy.json`. Stop with Ctrl-C. The default database is `.local/runs.db`; use `--db` consistently for another workspace. The frontend development proxy is for read-only iteration; run the built same-origin workspace to save review labels.

## Resume interrupted work

Rerun the same `run` command with the same dataset, configuration, provider artifacts and seed. Previously persisted cases are skipped. An expired lease can be reclaimed; an active lease rejects a second worker. Normal interruption releases the lease as failed, while a killed process leaves the lease until expiry (300 seconds by default in the SDK). Never edit ownership fields in SQLite to bypass an active worker.

Provider retry failures count across resumes. After exhaustion the case is persisted with score zero and an error status, so comparison cannot quietly drop failures. To retry with a repaired provider or a different budget, make an explicit new configuration/revision or experiment seed and keep the prior run as evidence.

The process-recovery test kills a subprocess after case A is persisted and before B completes, then resumes the same database. It verifies exactly two distinct result rows. A response generated immediately before a crash may be requested again; external invocation is not exactly once.

## Backup and restore

```sh
python3 -m regression_workbench.cli backup .local/backup.db
```

The SQLite backup API produces a consistent snapshot while the database is open. Stop the service before replacing its database with a backup, and preserve the old database together with its WAL/SHM files. Start against the restored copy with `--db`; verify run counts and review revisions. Do not copy only an actively written `.db` file and assume its WAL is included. A source cannot be its own backup destination.

## Docker demo

```sh
docker build -t llm-regression-workbench .
docker volume create regression-data
docker run --rm -v regression-data:/data llm-regression-workbench \
  python scripts/demo.py --db /data/runs.db
docker run --rm --name regression-workbench \
  -p 127.0.0.1:8765:8765 -v regression-data:/data llm-regression-workbench
```

The image runs as UID 65532, includes the built browser and Python core, and has a health check. It intentionally omits optional model weights and Torch. Keep the host port bound to loopback: the API has no identity provider or multi-user access controls. Host and Origin checks expect port 8765 when using these commands.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Incomplete comparison | Both runs must have all cases persisted and `complete` status |
| Dataset mismatch | Re-run both configurations against exactly the same fixture revision |
| Run leased elsewhere | Wait for the existing worker or its lease expiration |
| Review revision conflict | Reload the review before choosing again; another label edit won |
| Review returns 403 | Use the built workspace at its local origin; do not POST from another site |
| Unknown token accounting | Fixture usage estimates words; use a model/provider returning actual token counts |
| Model quality near zero | Inspect raw outputs; small models often fail strict JSON and tool protocols |
| Browser cannot load | Run `npm ci && npm run build` in `frontend` and use the service's URL |

No hosted API keys are needed. Never include secrets in configuration, fixture examples or reviewer notes. The CI workflow uses fixture inference; the optional actual-model measurement command is a separate, reproducible check.
