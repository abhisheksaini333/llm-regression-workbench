"""Comparison contracts."""

import math
import random

def pair(baseline,candidate):
    a={r['case_id']:r for r in baseline};b={r['case_id']:r for r in candidate}
    if len(a)!=len(baseline) or len(b)!=len(candidate): raise ValueError('duplicate case identity')
    if not a or a.keys()!=b.keys(): raise ValueError('comparison requires identical nonempty case sets')
    return [{'case_id':key,'baseline':a[key],'candidate':b[key],'delta':b[key]['score']-a[key]['score']} for key in sorted(a)]
