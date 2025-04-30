"""Comparison contracts."""
import math
import random


def pair(baseline, candidate):
    a = {r["case_id"]: r for r in baseline}
    b = {r["case_id"]: r for r in candidate}
    if len(a) != len(baseline) or len(b) != len(candidate):
        raise ValueError("duplicate case identity")
    if not a or a.keys() != b.keys():
        raise ValueError("comparison requires identical nonempty case sets")
    for row in [*baseline, *candidate]:
        score = row.get("score")
        if type(score) not in (int, float) or not math.isfinite(score) or not 0 <= score <= 1:
            raise ValueError("invalid score")
    pairs = [
        {
            "case_id": key,
            "baseline": a[key],
            "candidate": b[key],
            "delta": b[key]["score"] - a[key]["score"],
        }
        for key in sorted(a)
    ]
    for p in pairs:
        a, b = (p["baseline"], p["candidate"])
        if a.get("task") != b.get("task") or set(a.get("slices", [])) != set(
            b.get("slices", [])
        ):
            raise ValueError("task or slice membership differs")
        for row in (a, b):
            score = row["score"]
            if (
                not isinstance(score, (int, float))
                or not math.isfinite(score)
                or (not 0 <= score <= 1)
            ):
                raise ValueError("invalid score")
    return pairs


def bootstrap(values, seed=0, resamples=2000, confidence=0.95):
    if not values or any(type(v) not in (int, float) or not math.isfinite(v) for v in values):
        raise ValueError("finite observations required")
    if type(resamples) is not int or not 100 <= resamples <= 100000 or type(confidence) not in (int, float) or not 0 < confidence < 1:
        raise ValueError("invalid bootstrap settings")
    rng = random.Random(seed)
    means = sorted(
        (
            sum((rng.choice(values) for _ in values)) / len(values)
            for _ in range(resamples)
        )
    )
    tail = (1 - confidence) / 2
    return {
        "mean": sum(values) / len(values),
        "low": means[int(tail * (resamples - 1))],
        "high": means[int((1 - tail) * (resamples - 1))],
        "confidence": confidence,
        "resamples": resamples,
        "seed": seed,
        "n": len(values),
    }


def _summary(pairs):
    return {
        "count": len(pairs),
        "baseline": sum((p["baseline"]["score"] for p in pairs)) / len(pairs),
        "candidate": sum((p["candidate"]["score"] for p in pairs)) / len(pairs),
        "delta": sum((p["delta"] for p in pairs)) / len(pairs),
        "interval": bootstrap([p["delta"] for p in pairs]),
    }


def compare(baseline, candidate):
    pairs = pair(baseline, candidate)
    tasks = sorted({p["baseline"]["task"] for p in pairs})
    slices = sorted({s for p in pairs for s in p["baseline"].get("slices", [])})
    return {
        "overall": _summary(pairs),
        "tasks": {
            t: _summary([p for p in pairs if p["baseline"]["task"] == t]) for t in tasks
        },
        "slices": {
            s: _summary([p for p in pairs if s in p["baseline"].get("slices", [])])
            for s in slices
        },
        "cases": pairs,
    }


def gate(comparison, critical=None, max_overall_regression=0.02):
    failures = []
    if comparison["overall"]["delta"] < -max_overall_regression:
        failures.append(
            {
                "scope": "overall",
                "reason": "quality regression",
                "observed": comparison["overall"]["delta"],
                "threshold": -max_overall_regression,
            }
        )
    for name, rule in (critical or {}).items():
        observed = comparison["slices"].get(name)
        if observed is None:
            failures.append(
                {"scope": "slice", "slice": name, "reason": "required slice missing"}
            )
            continue
        if observed["candidate"] < rule.get("minimum", 0):
            failures.append(
                {
                    "scope": "slice",
                    "slice": name,
                    "reason": "below minimum quality",
                    "observed": observed["candidate"],
                    "threshold": rule["minimum"],
                }
            )
        if observed["delta"] < -rule.get("max_regression", 0):
            failures.append(
                {
                    "scope": "slice",
                    "slice": name,
                    "reason": "quality regression",
                    "observed": observed["delta"],
                    "threshold": -rule.get("max_regression", 0),
                }
            )
    decision = {"passed": not failures, "failures": failures}
    for name, rule in (critical or {}).items():
        observed = comparison["slices"].get(name)
        if observed is None:
            continue
        if observed["count"] < rule.get("min_cases", 1):
            decision["failures"].append(
                {
                    "scope": "slice",
                    "slice": name,
                    "reason": "insufficient cases",
                    "observed": observed["count"],
                    "threshold": rule["min_cases"],
                }
            )
        if (
            "lower_delta_bound" in rule
            and observed["interval"]["low"] < rule["lower_delta_bound"]
        ):
            decision["failures"].append(
                {
                    "scope": "slice",
                    "slice": name,
                    "reason": "uncertainty exceeds tolerance",
                    "observed": observed["interval"]["low"],
                    "threshold": rule["lower_delta_bound"],
                }
            )
    decision["passed"] = not decision["failures"]
    return decision


def operational(results):
    for row in results:
        latency = row.get("latency_ms", 0)
        if type(latency) not in (int, float) or not math.isfinite(latency) or latency < 0:
            raise ValueError("valid latency observations required")
        if any(type(row.get(k, 0)) is not int or row.get(k, 0) < 0 for k in ("input_tokens", "output_tokens")):
            raise ValueError("nonnegative integer token observations required")
        if row.get("usage_kind", "unknown") not in {"unknown", "tokens", "estimated_words"}:
            raise ValueError("invalid usage kind")
    latencies = sorted((float(r.get("latency_ms", 0)) for r in results))
    if not latencies or any((not math.isfinite(v) or v < 0 for v in latencies)):
        raise ValueError("valid latency observations required")
    kinds = sorted({r.get("usage_kind", "unknown") for r in results})
    return {
        "count": len(results),
        "p50_ms": latencies[math.ceil(len(latencies) * 0.5) - 1],
        "p95_ms": latencies[math.ceil(len(latencies) * 0.95) - 1],
        "total_tokens": sum(
            (r.get("input_tokens", 0) + r.get("output_tokens", 0) for r in results)
        ),
        "usage_kinds": kinds,
        "errors": sum((r.get("status") == "error" for r in results)),
    }


def operational_gate(metrics, budgets):
    failures = []
    for budget, metric in [
        ("max_p95_ms", "p95_ms"),
        ("max_tokens", "total_tokens"),
        ("max_errors", "errors"),
    ]:
        if budget in budgets and metrics[metric] > budgets[budget]:
            failures.append(
                {
                    "scope": "operations",
                    "reason": metric + " budget exceeded",
                    "observed": metrics[metric],
                    "threshold": budgets[budget],
                }
            )
    if "max_tokens" in budgets and metrics["usage_kinds"] != ["tokens"]:
        failures.append(
            {"scope": "operations", "reason": "exact token usage unavailable"}
        )
    return {"passed": not failures, "failures": failures}


def compare_runs(store, baseline_id, candidate_id, policy=None):
    baseline = store.get_run(baseline_id)
    candidate = store.get_run(candidate_id)
    if baseline["dataset_hash"] != candidate["dataset_hash"]:
        raise ValueError("dataset fingerprints differ")
    if baseline["status"] != "complete" or candidate["status"] != "complete":
        raise ValueError("both runs must be complete")
    a = store.results(baseline_id)
    b = store.results(candidate_id)
    comparison = compare(a, b)
    policy = validate_policy(policy or {})
    decision = gate(
        comparison,
        policy.get("critical", {}),
        policy.get("max_overall_regression", 0.02),
    )
    operations = {"baseline": operational(a), "candidate": operational(b)}
    extra = operational_gate(
        operations["candidate"], policy.get("budgets", {"max_errors": 0})
    )
    decision["failures"].extend(extra["failures"])
    decision["passed"] = not decision["failures"]
    return dict(
        comparison,
        baseline_id=baseline_id,
        candidate_id=candidate_id,
        operations=operations,
        gate=decision,
        policy=policy,
    )


def validate_policy(policy):
    if not isinstance(policy, dict):
        raise ValueError("policy must be an object")
    if set(policy) - {"critical", "budgets", "max_overall_regression"}:
        raise ValueError("unknown policy field")

    def number(value, lower, upper):
        if (
            type(value) not in (int, float)
            or not math.isfinite(value)
            or (not lower <= value <= upper)
        ):
            raise ValueError("invalid policy threshold")

    number(policy.get("max_overall_regression", 0.02), 0, 1)
    critical = policy.get("critical", {})
    if not isinstance(critical, dict):
        raise ValueError("critical policy must be an object")
    for name, rule in critical.items():
        if not isinstance(name, str) or not name or (not isinstance(rule, dict)):
            raise ValueError("invalid critical slice policy")
        if set(rule) - {"minimum", "max_regression", "min_cases", "lower_delta_bound"}:
            raise ValueError("unknown critical rule field")
        for key in ("minimum", "max_regression"):
            if key in rule:
                number(rule[key], 0, 1)
        if "lower_delta_bound" in rule:
            number(rule["lower_delta_bound"], -1, 1)
        if "min_cases" in rule and (
            type(rule["min_cases"]) is not int or rule["min_cases"] < 1
        ):
            raise ValueError("min_cases must be positive")
    budgets = policy.get("budgets", {})
    if not isinstance(budgets, dict):
        raise ValueError("budgets must be an object")
    if set(budgets) - {"max_p95_ms", "max_tokens", "max_errors"}:
        raise ValueError("unknown budget field")
    for value in budgets.values():
        number(value, 0, 1000000000000.0)
    return policy
