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
