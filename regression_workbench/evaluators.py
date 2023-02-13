"""Evaluators contracts."""

import json
import math
import re

def result(score, reason, details=None):
    return {'score':float(score),'reason':reason,'details':details or {}}

def parse_object(output):
    try:
        value=json.loads(output)
        return value if isinstance(value,dict) else None
    except (ValueError,TypeError): return None

def extraction(output, expected):
    value=parse_object(output)
    if value is None: return result(0,'invalid JSON object')
    matches={key:key in value and value[key]==item for key,item in expected.items()}
    return result(sum(matches.values())/len(matches) if matches else 1,'field accuracy',{'fields':matches})

def schema(output, expected):
    value=parse_object(output)
    if value is None: return result(0,'invalid JSON object')
    missing=[key for key in expected.get('required',[]) if key not in value]
    return result(not missing,'schema requirements',{'errors':['missing '+key for key in missing]})

_schema_required=schema

def schema(output, expected):
    checked=_schema_required(output,expected)
    value=parse_object(output)
    if value is None: return checked
    errors=list(checked['details']['errors'])
    types={'string':lambda v:isinstance(v,str),'integer':lambda v:type(v) is int,'number':lambda v:type(v) in (int,float) and math.isfinite(v),'boolean':lambda v:type(v) is bool,'object':lambda v:isinstance(v,dict),'array':lambda v:isinstance(v,list),'null':lambda v:v is None}
    for key,spec in expected.get('properties',{}).items():
        if key in value and 'type' in spec:
            if spec['type'] not in types: raise ValueError('unsupported schema type')
            if not types[spec['type']](value[key]): errors.append('wrong type '+key)
    return result(not errors,'schema validation',{'errors':errors})
