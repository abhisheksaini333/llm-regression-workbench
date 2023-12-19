# SDK, dataset and release contracts

A dataset envelope contains `version: 1`, a name and unique case IDs. Each case has `task`, textual `input`, task-specific `expected`, and optional named `slices`.

```json
{
  "version": 1,
  "name": "order-tools",
  "cases": [{
    "id": "lookup-order",
    "task": "tool",
    "input": "Find order 42. Return tool/arguments JSON.",
    "expected": {"tool": "lookup_order", "arguments": {"id": "42"}},
    "slices": ["critical"]
  }]
}
```

Dataset identity hashes canonical JSON with cases sorted by ID. Case ordering does not change identity; input, expected output, slice, name or version changes do. Run identity additionally includes configuration, seed, evaluator version and provider identity. The fixture provider hashes its output map. The local model provider records its artifact revision. Keep artifacts and manifests together.

## Evaluator semantics

| Task | Expected fields | Scoring |
| --- | --- | --- |
| extraction | Mapping of required field/value pairs | Fraction of fields matching; invalid JSON object scores zero |
| schema | `required`, `properties` with `type` / `enum`, `additionalProperties` | Binary validation of this subset; nested/general JSON Schema is not implemented |
| summary | `keywords`, optional `max_words`, `forbidden` | Case-insensitive word coverage; length or forbidden-phrase violation scores zero |
| tool | `tool`, optional `arguments` mapping | Correct name and all required argument values |

Keyword coverage is a diagnostic, not semantic faithfulness. Cases should include task-specific failure slices and reviewer judgment where a rule can be gamed. The optional `adapters.import_evals` accepts a limited chat-input/string-ideal JSONL shape and converts ideal words into summary coverage assertions; it does not run the upstream Evals registry or reproduce its grading semantics.

## Python provider integration

```python
from regression_workbench.dataset import load
from regression_workbench.providers import Response
from regression_workbench.runner import run
from regression_workbench.store import Store

class ApplicationProvider:
    name = "my-application"
    revision = "application-build-42"

    def generate(self, prompt, case, config):
        # Call the system under test here. Return measured tokens if available.
        return Response('{"tool":"lookup_order","arguments":{"id":"42"}}',
                        input_tokens=0, output_tokens=0, usage_kind="unknown")

with Store(".local/runs.db", secrets=["value-to-redact"]) as store:
    run_id = run(load("fixtures/tasks-v1.json"),
                 {"model": "my-application", "prompt": "{input}"},
                 ApplicationProvider(), store)
```

Raise `RetryableError` only for transient failures. Attempts count across restarts. Other exceptions fail the run and propagate; the caller decides how to remedy them. Results are immutable per `(run_id, case_id)`. A run already complete can be resumed without provider calls. The local model adapter uses deterministic greedy decoding, temperature zero, a 512-token input cap and at most 256 new tokens; seed identifies repeated experiments rather than changing greedy decoding.

## Release policy

```json
{
  "max_overall_regression": 0.02,
  "critical": {"critical": {
    "minimum": 0.8,
    "max_regression": 0.05,
    "min_cases": 4,
    "lower_delta_bound": -0.1
  }},
  "budgets": {"max_errors": 0, "max_p95_ms": 5000}
}
```

The optional lower bound compares the 95% paired bootstrap interval with a tolerated delta. Bootstrap samples fixed observed case deltas; it does not establish population representativeness. Insufficient or missing required slices block release. A token budget also blocks when usage is estimated or unknown. Unknown policy fields fail validation, so a typo cannot silently disable a gate.

## HTTP surface

- `GET /api/runs`: persisted run catalogue.
- `GET /api/runs/{id}`: metadata and redacted case results.
- `GET /api/compare?baseline=...&candidate=...`: full report and server-configured policy decision.
- `GET /api/review?baseline=...&candidate=...&reviewer=...`: stable A/B presentation and label revisions.
- `POST /api/reviews`: `{baseline,candidate,case_id,reviewer,choice,note,revision}`; choice is `A`, `B`, `tie` or `skip`.
- `GET /api/review-analysis?baseline=...&candidate=...`: agreement, disagreement, reviewer consistency and optional calibration-set threshold analysis.

Comparison and raw run endpoints remain available to local operators. Blinding removes model labels from review presentation; it is not an authorization boundary against an operator inspecting other endpoints.
