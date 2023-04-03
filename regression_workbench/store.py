"""Store contracts."""

import json
import sqlite3
import time
from .redaction import sanitize

class Store:
    def __init__(self,path,secrets=()):
        self.secrets=tuple(secrets)
        self.connection=sqlite3.connect(str(path),timeout=10)
        self.connection.row_factory=sqlite3.Row
        self.connection.execute('PRAGMA journal_mode=WAL')
        self.connection.execute('PRAGMA foreign_keys=ON')
        self.connection.executescript("CREATE TABLE IF NOT EXISTS runs (\n          id TEXT PRIMARY KEY,dataset_hash TEXT NOT NULL,config TEXT NOT NULL,seed INTEGER NOT NULL,\n          expected_count INTEGER NOT NULL,status TEXT NOT NULL DEFAULT 'pending',created REAL NOT NULL,\n          owner TEXT,lease_until REAL NOT NULL DEFAULT 0);\n        CREATE TABLE IF NOT EXISTS results (\n          run_id TEXT NOT NULL REFERENCES runs(id),case_id TEXT NOT NULL,payload TEXT NOT NULL,\n          PRIMARY KEY(run_id,case_id));\n        CREATE TABLE IF NOT EXISTS attempts (\n          id INTEGER PRIMARY KEY,run_id TEXT NOT NULL REFERENCES runs(id),case_id TEXT NOT NULL,payload TEXT NOT NULL);\n        PRAGMA user_version=1;\n")
    def close(self): self.connection.close()
    def __enter__(self): return self
    def __exit__(self,*exc): self.close()

    def register(self,run_id,dataset_hash,config,seed,expected_count):
        encoded=json.dumps(sanitize(config,self.secrets),sort_keys=True,allow_nan=False)
        with self.connection:
            row=self.connection.execute('SELECT * FROM runs WHERE id=?',(run_id,)).fetchone()
            if row:
                if (row['dataset_hash'],row['config'],row['seed'],row['expected_count'])!=(dataset_hash,encoded,seed,expected_count):
                    raise ValueError('run identity collision')
                return
            self.connection.execute('INSERT INTO runs(id,dataset_hash,config,seed,expected_count,created) VALUES (?,?,?,?,?,?)',(run_id,dataset_hash,encoded,seed,expected_count,time.time()))

    def save_result(self,run_id,case_id,payload):
        encoded=json.dumps(sanitize(payload,self.secrets),sort_keys=True,allow_nan=False)
        with self.connection:
            existing=self.connection.execute('SELECT payload FROM results WHERE run_id=? AND case_id=?',(run_id,case_id)).fetchone()
            if existing:
                if existing['payload']!=encoded: raise ValueError('case result is immutable')
                return
            self.connection.execute('INSERT INTO results VALUES (?,?,?)',(run_id,case_id,encoded))

    def results(self,run_id):
        return [dict(json.loads(row['payload']),case_id=row['case_id']) for row in self.connection.execute('SELECT * FROM results WHERE run_id=? ORDER BY case_id',(run_id,))]
    def get_run(self,run_id):
        row=self.connection.execute('SELECT * FROM runs WHERE id=?',(run_id,)).fetchone()
        if not row: raise KeyError('run not found')
        value=dict(row);value['config']=json.loads(value['config'])
        value['completed']=self.connection.execute('SELECT count(*) FROM results WHERE run_id=?',(run_id,)).fetchone()[0]
        return value
    def list_runs(self):
        return [self.get_run(row['id']) for row in self.connection.execute('SELECT id FROM runs ORDER BY created DESC,id')]

    def record_attempt(self,run_id,case_id,payload):
        with self.connection:
            self.connection.execute('INSERT INTO attempts(run_id,case_id,payload) VALUES (?,?,?)',(run_id,case_id,json.dumps(sanitize(payload,self.secrets),allow_nan=False)))
    def attempts(self,run_id):
        return [dict(json.loads(row['payload']),case_id=row['case_id']) for row in self.connection.execute('SELECT * FROM attempts WHERE run_id=? ORDER BY id',(run_id,))]

    def claim(self,run_id,owner,lease_seconds=300,now=None):
        if lease_seconds<=0: raise ValueError('lease must be positive')
        now=time.time() if now is None else now
        with self.connection:
            cursor=self.connection.execute("UPDATE runs SET owner=?,lease_until=?,status='running' WHERE id=? AND (owner IS NULL OR owner=? OR lease_until<=?)",(owner,now+lease_seconds,run_id,owner,now))
            if cursor.rowcount!=1: raise RuntimeError('run leased by another worker or missing')
