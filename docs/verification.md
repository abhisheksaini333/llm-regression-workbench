# Verification and evidence boundaries

| Requirement | Evidence | Boundary |
| --- | --- | --- |
| Stable identities | Case-order invariance, changed-content and provider-output hash tests | Meaningful input changes intentionally create new run identities |
| Four task families | 24 owned cases: six each for extraction, schema, summary and tools | Rules measure declared constraints, not general understanding |
| Critical regression gate | Demo mean 0.1667 → 0.8333 while critical mean 1.0 → 0.0; CLI/browser block release | Demo provider outputs are authored fixtures |
| Actual model runs | Three FLAN-T5-small CPU runs, 72 generations, repeated baseline identical | Structured/tool tasks fail; candidate blocked |
| Uncertainty | Paired bootstrap, task/slice comparisons, sample-size gate | Fixed small fixture set, not a representative population |
| Redaction | Nested keys, bearer/provider tokens and configured values tested before persistence | Arbitrary secrets require explicit configuration |
| Restart recovery | Subprocess killed after one persisted case; SQLite reclaimed; two final rows | An external invocation can repeat after a crash |
| Retry fencing | Expired/replaced workers cannot append attempts or results | Lease must exceed maximum provider request duration |
| Review concurrency | Two SQLite connections race on one revision: one save, one conflict | Reviewer names are labels, not authenticated identities |
| Review analysis | Browser saves A/B label, reload retains it, disagreement appears; calibration tests | Demonstration labels are not an independent human study |
| HTTP/browser | Three journeys: failed gate examples, review/disagreement, 390px mobile layout | Trusted same-origin local workspace |
| Distribution | Clean Python 3.10 wheel install; non-root Docker build and runtime checks | Container excludes optional model weights and Torch |

The suite contains 94 Python tests and four React component tests. Browser tests use the actual HTTP service and SQLite. GitHub Actions repeats the deterministic tests, browser journeys and build; hosted workflow results are separate from local verification.

Actual model prompts, outputs, scores, intervals and measurements are in `evidence/flan-t5-small.json`. Re-run `scripts/measure_model.py` for an independent record. Model loading is excluded from its generation/evaluation wall time.
