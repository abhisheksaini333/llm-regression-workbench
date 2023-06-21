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
        store.connection.execute('INSERT INTO reviews VALUES (?,?,?,?,?,?,1,?) ON CONFLICT(baseline,candidate,case_id,reviewer) DO UPDATE SET preference=excluded.preference,note=excluded.note,revision=reviews.revision+1,updated=excluded.updated',(baseline,candidate,case_id,reviewer,preference,sanitize(note,store.secrets),time.time()))
    return next(r for r in list_reviews(store,baseline,candidate) if r['case_id']==case_id and r['reviewer']==reviewer)

def list_reviews(store,baseline,candidate):
    _schema(store)
    return [dict(row) for row in store.connection.execute('SELECT * FROM reviews WHERE baseline=? AND candidate=? ORDER BY case_id,reviewer',(baseline,candidate))]
