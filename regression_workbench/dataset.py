"""Dataset contracts."""
import hashlib
import json
import re


def canonical(value):
    return json.dumps(
        value,
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
        allow_nan=False,
    )


def digest(value):
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def validate(dataset):
    if not isinstance(dataset, dict) or type(dataset.get("version")) is not int or dataset["version"] != 1:
        raise ValueError("dataset.version must be 1")
    if not isinstance(dataset.get("name"), str) or not dataset["name"].strip():
        raise ValueError("dataset.name is required")
    if not isinstance(dataset.get("cases"), list):
        raise ValueError("dataset.cases must be a list")
    for case in dataset["cases"]:
        if (
            not isinstance(case, dict)
            or not isinstance(case.get("id"), str)
            or (not case["id"].strip())
        ):
            raise ValueError("case.id is required")
        if case.get("task") not in TASKS:
            raise ValueError("unsupported case.task")
        if not isinstance(case.get("input"), str):
            raise ValueError("case.input must be text")
        if not isinstance(case.get("expected"), dict):
            raise ValueError("case.expected must be an object")
    ids = [c["id"] for c in dataset["cases"]]
    if len(ids) != len(set(ids)):
        raise ValueError("case identifiers must be unique")
    for case in dataset["cases"]:
        slices = case.get("slices", [])
        if (
            not isinstance(slices, list)
            or not all((isinstance(s, str) and s.strip() for s in slices))
            or len(slices) != len(set(slices))
        ):
            raise ValueError("slices must be unique nonempty strings")
    canonical(dataset)
    return dataset


TASKS = {"extraction", "schema", "summary", "tool"}


def fingerprint(dataset):
    validate(dataset)
    return digest(dict(dataset, cases=sorted(dataset["cases"], key=lambda c: c["id"])))


def load(path):
    from pathlib import Path

    return validate(json.loads(Path(path).read_text(encoding="utf-8")))


def select(dataset, task=None, slice_name=None):
    validate(dataset)
    return dict(
        dataset,
        cases=[
            c
            for c in dataset["cases"]
            if (task is None or c["task"] == task)
            and (slice_name is None or slice_name in c.get("slices", []))
        ],
    )


def diff(before, after):
    validate(before)
    validate(after)
    a = {c["id"]: c for c in before["cases"]}
    b = {c["id"]: c for c in after["cases"]}
    return {
        "added": sorted(b.keys() - a.keys()),
        "removed": sorted(a.keys() - b.keys()),
        "changed": sorted((k for k in a.keys() & b.keys() if a[k] != b[k])),
    }
