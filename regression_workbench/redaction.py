"""Redaction contracts."""

import re
from urllib.parse import quote, quote_plus

SENSITIVE = re.compile(
    r"(authorization|api.?key|password|secret|access.?token|refresh.?token|cookie)",
    re.I,
)


def redact(value):
    if isinstance(value, dict):
        return {
            str(k): "[REDACTED]" if SENSITIVE.search(str(k)) else redact(v)
            for k, v in value.items()
        }
    if isinstance(value, (list, tuple)):
        return [redact(v) for v in value]
    return value


_redact_structure = redact


def redact(value):
    if isinstance(value, str):
        value = re.sub(
            r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]+", "Bearer [REDACTED]", value
        )
        value = re.sub(r"\bsk-[A-Za-z0-9_-]{8,}", "[REDACTED]", value)
        return value
    return _redact_structure(value)


def sanitize(value, secrets=()):
    value = redact(value)
    if isinstance(value, str):
        value = re.sub(
            r"(?i)((?:api[_-]?key|token|password|secret)=)[^&\s]+",
            r"\1[REDACTED]",
            value,
        )
        value = re.sub(r"(?i)(https?://)[^/\s@]+@", r"\1[REDACTED]@", value)
        variants = {variant for secret in secrets if secret for variant in (secret, quote(secret, safe=""), quote_plus(secret, safe=""))}
        for secret in sorted(variants, key=len, reverse=True):
            value = value.replace(secret, "[REDACTED]")
        return value
    if isinstance(value, dict):
        return {k: sanitize(v, secrets) for k, v in value.items()}
    if isinstance(value, list):
        return [sanitize(v, secrets) for v in value]
    return value
