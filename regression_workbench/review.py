"""Review contracts."""

import hashlib
import json
import time
from .redaction import sanitize

def _schema(store):
    store.connection.execute('CREATE TABLE IF NOT EXISTS reviews (baseline TEXT NOT NULL,candidate TEXT NOT NULL,case_id TEXT NOT NULL,reviewer TEXT NOT NULL,preference TEXT NOT NULL,note TEXT NOT NULL,revision INTEGER NOT NULL,updated REAL NOT NULL,PRIMARY KEY(baseline,candidate,case_id,reviewer),FOREIGN KEY(baseline,case_id) REFERENCES results(run_id,case_id),FOREIGN KEY(candidate,case_id) REFERENCES results(run_id,case_id))')

def save(store,baseline,candidate,case_id,reviewer,preference,note='',expected_revision=None):
    _schema(store)
    if baseline==candidate: raise ValueError('distinct runs required')
    if preference not in {'baseline','candidate','tie','skip'}: raise ValueError('invalid preference')
    if not isinstance(reviewer,str) or not reviewer.strip() or len(reviewer)>100: raise ValueError('reviewer required')
    if not isinstance(note,str) or len(note)>4000: raise ValueError('note too long')
    with store.connection:
        current=store.connection.execute('SELECT revision FROM reviews WHERE baseline=? AND candidate=? AND case_id=? AND reviewer=?',(baseline,candidate,case_id,reviewer)).fetchone()
        if expected_revision is not None and expected_revision!=(current['revision'] if current else 0): raise ValueError('review revision conflict')
        store.connection.execute('INSERT INTO reviews VALUES (?,?,?,?,?,?,1,?) ON CONFLICT(baseline,candidate,case_id,reviewer) DO UPDATE SET preference=excluded.preference,note=excluded.note,revision=reviews.revision+1,updated=excluded.updated',(baseline,candidate,case_id,reviewer,preference,sanitize(note,store.secrets),time.time()))
    return next(r for r in list_reviews(store,baseline,candidate) if r['case_id']==case_id and r['reviewer']==reviewer)

def list_reviews(store,baseline,candidate):
    _schema(store)
    return [dict(row) for row in store.connection.execute('SELECT * FROM reviews WHERE baseline=? AND candidate=? ORDER BY case_id,reviewer',(baseline,candidate))]

def _order(case_id,reviewer):
    return int(hashlib.sha256((case_id+'\0'+reviewer).encode()).hexdigest()[:8],16)%2

def blind_pair(pair,reviewer):
    names=['baseline','candidate'] if _order(pair['case_id'],reviewer)==0 else ['candidate','baseline']
    return {'case_id':pair['case_id'],'A':pair[names[0]].get('output',''),'B':pair[names[1]].get('output',''),'prompt':pair['baseline'].get('prompt','')}

def unblind(case_id,reviewer,choice):
    if choice in {'tie','skip'}: return choice
    if choice not in {'A','B'}: raise ValueError('invalid blinded choice')
    names=['baseline','candidate'] if _order(case_id,reviewer)==0 else ['candidate','baseline']
    return names[0 if choice=='A' else 1]

def judge_preference(delta,tie_threshold=0.05):
    return 'tie' if abs(delta)<=tie_threshold else ('candidate' if delta>0 else 'baseline')

def agreement(pairs,reviews,tie_threshold=0.05):
    deltas={p['case_id']:p['delta'] for p in pairs}
    observations=[]
    for label in reviews:
        if label['preference']=='skip' or label['case_id'] not in deltas: continue
        judge=judge_preference(deltas[label['case_id']],tie_threshold)
        observations.append({'case_id':label['case_id'],'human':label['preference'],'judge':judge,'agrees':judge==label['preference']})
    return {'reviewed':len(observations),'agreement':sum(o['agrees'] for o in observations)/len(observations) if observations else None,'disagreements':[o for o in observations if not o['agrees']],'tie_threshold':tie_threshold}
