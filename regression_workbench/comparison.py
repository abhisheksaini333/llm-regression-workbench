"""Comparison contracts."""

import math
import random

def pair(baseline,candidate):
    a={r['case_id']:r for r in baseline};b={r['case_id']:r for r in candidate}
    if len(a)!=len(baseline) or len(b)!=len(candidate): raise ValueError('duplicate case identity')
    if not a or a.keys()!=b.keys(): raise ValueError('comparison requires identical nonempty case sets')
    return [{'case_id':key,'baseline':a[key],'candidate':b[key],'delta':b[key]['score']-a[key]['score']} for key in sorted(a)]

_pair_identity=pair

def pair(baseline,candidate):
    pairs=_pair_identity(baseline,candidate)
    for p in pairs:
        a,b=p['baseline'],p['candidate']
        if a.get('task')!=b.get('task') or set(a.get('slices',[]))!=set(b.get('slices',[])):
            raise ValueError('task or slice membership differs')
        for row in (a,b):
            score=row['score']
            if not isinstance(score,(int,float)) or not math.isfinite(score) or not 0<=score<=1: raise ValueError('invalid score')
    return pairs

def bootstrap(values,seed=0,resamples=2000,confidence=0.95):
    if not values or any(not math.isfinite(v) for v in values): raise ValueError('finite observations required')
    if resamples<100 or not 0<confidence<1: raise ValueError('invalid bootstrap settings')
    rng=random.Random(seed)
    means=sorted(sum(rng.choice(values) for _ in values)/len(values) for _ in range(resamples))
    tail=(1-confidence)/2
    return {'mean':sum(values)/len(values),'low':means[int(tail*(resamples-1))],'high':means[int((1-tail)*(resamples-1))],'confidence':confidence,'resamples':resamples,'seed':seed,'n':len(values)}

def _summary(pairs):
    return {'count':len(pairs),'baseline':sum(p['baseline']['score'] for p in pairs)/len(pairs),'candidate':sum(p['candidate']['score'] for p in pairs)/len(pairs),'delta':sum(p['delta'] for p in pairs)/len(pairs),'interval':bootstrap([p['delta'] for p in pairs])}

def compare(baseline,candidate):
    pairs=pair(baseline,candidate)
    tasks=sorted({p['baseline']['task'] for p in pairs})
    slices=sorted({s for p in pairs for s in p['baseline'].get('slices',[])})
    return {'overall':_summary(pairs),'tasks':{t:_summary([p for p in pairs if p['baseline']['task']==t]) for t in tasks},'slices':{s:_summary([p for p in pairs if s in p['baseline'].get('slices',[])]) for s in slices},'cases':pairs}

def gate(comparison,critical=None,max_overall_regression=0.02):
    failures=[]
    if comparison['overall']['delta'] < -max_overall_regression:
        failures.append({'scope':'overall','reason':'quality regression','observed':comparison['overall']['delta'],'threshold':-max_overall_regression})
    for name,rule in (critical or {}).items():
        observed=comparison['slices'].get(name)
        if observed is None:
            failures.append({'scope':'slice','slice':name,'reason':'required slice missing'});continue
        if observed['candidate']<rule.get('minimum',0):
            failures.append({'scope':'slice','slice':name,'reason':'below minimum quality','observed':observed['candidate'],'threshold':rule['minimum']})
        if observed['delta'] < -rule.get('max_regression',0):
            failures.append({'scope':'slice','slice':name,'reason':'quality regression','observed':observed['delta'],'threshold':-rule.get('max_regression',0)})
    return {'passed':not failures,'failures':failures}
