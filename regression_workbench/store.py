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
