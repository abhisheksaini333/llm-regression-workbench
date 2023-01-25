"""Dataset contracts."""

import hashlib
import json
import re

def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':'), allow_nan=False)

def digest(value):
    return hashlib.sha256(canonical(value).encode('utf-8')).hexdigest()

def validate(dataset):
    if not isinstance(dataset, dict) or dataset.get('version') != 1:
        raise ValueError('dataset.version must be 1')
    if not isinstance(dataset.get('name'), str) or not dataset['name'].strip():
        raise ValueError('dataset.name is required')
    if not isinstance(dataset.get('cases'), list):
        raise ValueError('dataset.cases must be a list')
    return dataset

_validate_envelope = validate
TASKS = {'extraction', 'schema', 'summary', 'tool'}

def validate(dataset):
    _validate_envelope(dataset)
    for case in dataset['cases']:
        if not isinstance(case, dict) or not isinstance(case.get('id'), str) or not case['id'].strip():
            raise ValueError('case.id is required')
        if case.get('task') not in TASKS:
            raise ValueError('unsupported case.task')
        if not isinstance(case.get('input'), str):
            raise ValueError('case.input must be text')
        if not isinstance(case.get('expected'), dict):
            raise ValueError('case.expected must be an object')
    return dataset

_validate_cases = validate

def validate(dataset):
    _validate_cases(dataset)
    ids = [c['id'] for c in dataset['cases']]
    if len(ids) != len(set(ids)):
        raise ValueError('case identifiers must be unique')
    return dataset

_validate_unique = validate

def validate(dataset):
    _validate_unique(dataset)
    for case in dataset['cases']:
        slices = case.get('slices', [])
        if not isinstance(slices, list) or not all(isinstance(s,str) and s.strip() for s in slices) or len(slices)!=len(set(slices)):
            raise ValueError('slices must be unique nonempty strings')
    return dataset

def fingerprint(dataset):
    validate(dataset)
    return digest(dict(dataset, cases=sorted(dataset['cases'], key=lambda c:c['id'])))

def load(path):
    from pathlib import Path
    return validate(json.loads(Path(path).read_text(encoding='utf-8')))
