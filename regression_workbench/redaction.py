"""Redaction contracts."""

import re
SENSITIVE = re.compile(r'(authorization|api.?key|password|secret|access.?token|refresh.?token|cookie)',re.I)

def redact(value):
    if isinstance(value,dict): return {str(k):'[REDACTED]' if SENSITIVE.search(str(k)) else redact(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)): return [redact(v) for v in value]
    return value
