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
