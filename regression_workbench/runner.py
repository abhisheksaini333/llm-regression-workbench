"""Durable sequential runner with bounded retry and fenced ownership."""
import time
import uuid
from . import dataset as datasets, config as configs, evaluators
from .providers import RetryableError


def bound_config(config, provider):
    identity = {"adapter": getattr(provider, "name", type(provider).__name__)}
    if hasattr(provider, "outputs"):
        identity["outputs_hash"] = datasets.digest(provider.outputs)
    if hasattr(provider, "revision"):
        identity["model_revision"] = provider.revision
    return dict(config, provider_identity=identity)


def run_key(dataset, config, provider, seed=0):
    return configs.run_identity(
        datasets.fingerprint(dataset), bound_config(config, provider), seed
    )


def run(
    dataset,
    config,
    provider,
    store,
    seed=0,
    stop_after=None,
    max_attempts=3,
    lease_seconds=300,
    sleep=time.sleep,
):
    from .store import validate_lease
    validate_lease(lease_seconds)
    datasets.validate(dataset)
    configs.validate(config)
    if type(max_attempts) is not int or not 1 <= max_attempts <= 10:
        raise ValueError("max_attempts must be 1..10")
    if stop_after is not None and (type(stop_after) is not int or stop_after < 1):
        raise ValueError("stop_after must be positive")
    if not dataset["cases"]:
        raise ValueError("cannot run an empty dataset")
    config = bound_config(config, provider)
    fingerprint = datasets.fingerprint(dataset)
    identity = configs.run_identity(fingerprint, config, seed)
    store.register(identity, fingerprint, config, seed, len(dataset["cases"]))
    owner = uuid.uuid4().hex
    store.claim(identity, owner, lease_seconds)
    completed = 0
    try:
        done = {row["case_id"] for row in store.results(identity)}
        for case in sorted(dataset["cases"], key=lambda case: case["id"]):
            if case["id"] in done:
                continue
            store.claim(identity, owner, lease_seconds)
            prompt = configs.render(config, case["input"])
            started = time.perf_counter()
            response = None
            failure = "provider retry budget exhausted before resume"
            prior = [
                attempt
                for attempt in store.attempts(identity)
                if attempt["case_id"] == case["id"]
            ]
            used = max((a["attempt"] for a in prior), default=0)
            for attempt in range(used + 1, max_attempts + 1):
                try:
                    response = provider.generate(prompt, case, config)
                    break
                except RetryableError as error:
                    failure = str(error)
                    store.record_owned_attempt(
                        identity,
                        case["id"],
                        {"attempt": attempt, "error": failure, "retryable": True},
                        owner,
                    )
                    if attempt < max_attempts:
                        sleep(min(0.05 * 2 ** (attempt - 1), 1.0))
            elapsed = (time.perf_counter() - started) * 1000
            if response is None:
                payload = {
                    "task": case["task"],
                    "slices": case.get("slices", []),
                    "score": 0.0,
                    "reason": "provider retry budget exhausted",
                    "status": "error",
                    "error": failure,
                    "output": "",
                    "latency_ms": elapsed,
                    "input_tokens": 0,
                    "output_tokens": 0,
                    "usage_kind": "unknown",
                }
            else:
                scored = evaluators.evaluate(case, response.output)
                payload = dict(
                    scored,
                    slices=case.get("slices", []),
                    output=response.output,
                    prompt=prompt,
                    trace=response.trace,
                    latency_ms=elapsed,
                    input_tokens=response.input_tokens,
                    output_tokens=response.output_tokens,
                    usage_kind=response.usage_kind,
                    status="ok",
                )
            store.save_owned_result(identity, case["id"], payload, owner)
            completed += 1
            if stop_after is not None and completed >= stop_after:
                status = (
                    "complete"
                    if store.get_run(identity)["completed"] == len(dataset["cases"])
                    else "paused"
                )
                store.finish(identity, owner, status)
                return identity
        store.finish(identity, owner, "complete")
        return identity
    except BaseException:
        try:
            store.finish(identity, owner, "failed")
        except RuntimeError:
            pass  # Another owner or an expired lease must not hide the original error.
        raise
