"""Evaluators contracts."""
import json
import math
import re


def result(score, reason, details=None):
    return {"score": float(score), "reason": reason, "details": details or {}}


def _unique_object(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise ValueError("duplicate JSON field")
        value[key] = item
    return value


def parse_object(output):
    try:
        value = json.loads(
            output,
            object_pairs_hook=_unique_object,
            parse_constant=lambda value: (_ for _ in ()).throw(
                ValueError("nonfinite JSON")
            ),
        )
        return value if isinstance(value, dict) else None
    except (ValueError, TypeError):
        return None


def extraction(output, expected):
    value = parse_object(output)
    if value is None:
        return result(0, "invalid JSON object")
    matches = {
        key: key in value
        and value[key] == item
        and (
            type(value[key]) is type(item)
            if type(value[key]) is bool or type(item) is bool
            else True
        )
        for key, item in expected.items()
    }
    return result(
        sum(matches.values()) / len(matches) if matches else 1,
        "field accuracy",
        {"fields": matches},
    )


def schema(output, expected):
    value = parse_object(output)
    if value is None:
        return result(0, "invalid JSON object")
    missing = [key for key in expected.get("required", []) if key not in value]
    checked = result(
        not missing,
        "schema requirements",
        {"errors": ["missing " + key for key in missing]},
    )
    value = parse_object(output)
    if value is None:
        return checked
    errors = list(checked["details"]["errors"])
    types = {
        "string": lambda v: isinstance(v, str),
        "integer": lambda v: type(v) is int,
        "number": lambda v: type(v) in (int, float) and math.isfinite(v),
        "boolean": lambda v: type(v) is bool,
        "object": lambda v: isinstance(v, dict),
        "array": lambda v: isinstance(v, list),
        "null": lambda v: v is None,
    }
    for key, spec in expected.get("properties", {}).items():
        if key in value and "type" in spec:
            if spec["type"] not in types:
                raise ValueError("unsupported schema type")
            if not types[spec["type"]](value[key]):
                errors.append("wrong type " + key)
    checked = result(not errors, "schema validation", {"errors": errors})
    value = parse_object(output)
    if value is None:
        return checked
    errors = list(checked["details"]["errors"])
    for key, spec in expected.get("properties", {}).items():
        if key in value and "enum" in spec and (value[key] not in spec["enum"]):
            errors.append("invalid enum " + key)
    if expected.get("additionalProperties") is False:
        errors.extend(
            (
                "unexpected " + key
                for key in value.keys() - expected.get("properties", {}).keys()
            )
        )
    return result(not errors, "schema validation", {"errors": errors})


def summary(output, expected):
    words = set(re.findall("[\\w'-]+", output.casefold()))
    keywords = expected.get("keywords", [])
    matched = [word for word in keywords if word.casefold() in words]
    checked = result(
        len(matched) / len(keywords) if keywords else 1,
        "keyword coverage",
        {"matched": matched, "word_count": len(output.split())},
    )
    violations = []
    if len(output.split()) > expected.get("max_words", 100000):
        violations.append("length limit")
    for claim in expected.get("forbidden", []):
        if claim.casefold() in output.casefold():
            violations.append("forbidden claim: " + claim)
    return result(
        0 if violations else checked["score"],
        "summary constraints" if violations else checked["reason"],
        dict(checked["details"], violations=violations),
    )


def tool(output, expected):
    value = parse_object(output)
    if value is None:
        return result(0, "invalid tool JSON")
    correct = value.get("tool") == expected.get("tool")
    checked = result(correct, "tool selection", {"name_correct": correct})
    value = parse_object(output)
    if not checked["score"]:
        return checked
    args = value.get("arguments", {})
    correct = isinstance(args, dict) and all(
        (k in args and args[k] == v for k, v in expected.get("arguments", {}).items())
    )
    return result(
        correct, "tool arguments", dict(checked["details"], arguments_correct=correct)
    )


def evaluate(case, output):
    functions = {
        "extraction": extraction,
        "schema": schema,
        "summary": summary,
        "tool": tool,
    }
    if case["task"] not in functions:
        raise ValueError("unsupported task")
    scored = functions[case["task"]](output, case["expected"])
    return dict(scored, version=1, task=case["task"])


def aggregate(results):
    grouped = {}
    for item in results:
        grouped.setdefault(item["task"], []).append(item["score"])
    return {
        task: {"count": len(scores), "mean": sum(scores) / len(scores)}
        for task, scores in sorted(grouped.items())
    }
