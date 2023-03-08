"""Redaction contracts."""

import re
SENSITIVE = re.compile(r'(authorization|api.?key|password|secret|access.?token|refresh.?token|cookie)',re.I)

def redact(value):
    if isinstance(value,dict): return {str(k):'[REDACTED]' if SENSITIVE.search(str(k)) else redact(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)): return [redact(v) for v in value]
    return value

_redact_structure=redact

def redact(value):
    if isinstance(value,str):
        value=re.sub(r'(?i)\bBearer\s+[A-Za-z0-9._~+/=-]+','Bearer [REDACTED]',value)
        value=re.sub(r'\bsk-[A-Za-z0-9_-]{8,}','[REDACTED]',value)
        return value
    return _redact_structure(value)
