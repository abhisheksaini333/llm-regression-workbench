"""Store contracts."""

import json
import sqlite3
import time
import math


def validate_lease(seconds):
    if type(seconds) not in (int, float) or not math.isfinite(seconds) or not 0 < seconds <= 86400:
        raise ValueError("lease must be finite and within one day")
from .redaction import sanitize


class Store:
    def __init__(self, path, secrets=()):
        self.secrets = tuple(secrets)
        self.path = str(path)
        self.connection = sqlite3.connect(str(path), timeout=10)
        if self.connection.execute("PRAGMA user_version").fetchone()[0] not in {0, 1}:
            self.connection.close()
            raise ValueError("unsupported workspace schema version")
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA journal_mode=WAL")
        self.connection.execute("PRAGMA foreign_keys=ON")
        self.connection.executescript(
            "CREATE TABLE IF NOT EXISTS runs (\n          id TEXT PRIMARY KEY,dataset_hash TEXT NOT NULL,config TEXT NOT NULL,seed INTEGER NOT NULL,\n          expected_count INTEGER NOT NULL,status TEXT NOT NULL DEFAULT 'pending',created REAL NOT NULL,\n          owner TEXT,lease_until REAL NOT NULL DEFAULT 0);\n        CREATE TABLE IF NOT EXISTS results (\n          run_id TEXT NOT NULL REFERENCES runs(id),case_id TEXT NOT NULL,payload TEXT NOT NULL,\n          PRIMARY KEY(run_id,case_id));\n        CREATE TABLE IF NOT EXISTS attempts (\n          id INTEGER PRIMARY KEY,run_id TEXT NOT NULL REFERENCES runs(id),case_id TEXT NOT NULL,payload TEXT NOT NULL);\n        PRAGMA user_version=1;\n"
        )

    def close(self):
        self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()

    def register(self, run_id, dataset_hash, config, seed, expected_count):
        encoded = json.dumps(
            sanitize(config, self.secrets), sort_keys=True, allow_nan=False
        )
        with self.connection:
            row = self.connection.execute(
                "SELECT * FROM runs WHERE id=?", (run_id,)
            ).fetchone()
            if row:
                if (
                    row["dataset_hash"],
                    row["config"],
                    row["seed"],
                    row["expected_count"],
                ) != (dataset_hash, encoded, seed, expected_count):
                    raise ValueError("run identity collision")
                return
            self.connection.execute(
                "INSERT INTO runs(id,dataset_hash,config,seed,expected_count,created) VALUES (?,?,?,?,?,?)",
                (run_id, dataset_hash, encoded, seed, expected_count, time.time()),
            )

    def save_result(self, run_id, case_id, payload):
        encoded = json.dumps(
            sanitize(payload, self.secrets), sort_keys=True, allow_nan=False
        )
        with self.connection:
            existing = self.connection.execute(
                "SELECT payload FROM results WHERE run_id=? AND case_id=?",
                (run_id, case_id),
            ).fetchone()
            if existing:
                if existing["payload"] != encoded:
                    raise ValueError("case result is immutable")
                return
            self.connection.execute(
                "INSERT INTO results VALUES (?,?,?)", (run_id, case_id, encoded)
            )

    def results(self, run_id):
        return [
            dict(json.loads(row["payload"]), case_id=row["case_id"])
            for row in self.connection.execute(
                "SELECT * FROM results WHERE run_id=? ORDER BY case_id", (run_id,)
            )
        ]

    def get_run(self, run_id):
        row = self.connection.execute(
            "SELECT * FROM runs WHERE id=?", (run_id,)
        ).fetchone()
        if not row:
            raise KeyError("run not found")
        value = dict(row)
        value["config"] = json.loads(value["config"])
        value["completed"] = self.connection.execute(
            "SELECT count(*) FROM results WHERE run_id=?", (run_id,)
        ).fetchone()[0]
        return value

    def list_runs(self):
        return [
            self.get_run(row["id"])
            for row in self.connection.execute(
                "SELECT id FROM runs ORDER BY created DESC,id"
            )
        ]

    def record_attempt(self, run_id, case_id, payload):
        """Trusted fixture/import helper; workers use record_owned_attempt instead."""
        with self.connection:
            self.connection.execute(
                "INSERT INTO attempts(run_id,case_id,payload) VALUES (?,?,?)",
                (
                    run_id,
                    case_id,
                    json.dumps(sanitize(payload, self.secrets), allow_nan=False),
                ),
            )

    def attempts(self, run_id):
        return [
            dict(json.loads(row["payload"]), case_id=row["case_id"])
            for row in self.connection.execute(
                "SELECT * FROM attempts WHERE run_id=? ORDER BY id", (run_id,)
            )
        ]

    def claim(self, run_id, owner, lease_seconds=300, now=None):
        validate_lease(lease_seconds)
        if not isinstance(owner, str) or not owner.strip():
            raise ValueError("worker owner required")
        now = time.time() if now is None else now
        if type(now) not in (int, float) or not math.isfinite(now):
            raise ValueError("finite lease timestamp required")
        with self.connection:
            cursor = self.connection.execute(
                "UPDATE runs SET owner=?,lease_until=?,status='running' WHERE id=? AND (owner IS NULL OR owner=? OR lease_until<=?)",
                (owner, now + lease_seconds, run_id, owner, now),
            )
            if cursor.rowcount != 1:
                raise RuntimeError("run leased by another worker or missing")

    def save_owned_result(self, run_id, case_id, payload, owner):
        # IMMEDIATE serializes ownership validation with immutable result insertion.
        self.connection.execute("BEGIN IMMEDIATE")
        try:
            row = self.connection.execute(
                "SELECT owner,lease_until FROM runs WHERE id=?", (run_id,)
            ).fetchone()
            if not row or row["owner"] != owner or row["lease_until"] <= time.time():
                raise RuntimeError("worker lease lost")
            self.save_result(run_id, case_id, payload)
            self.connection.commit()
        except BaseException:
            self.connection.rollback()
            raise

    def finish(self, run_id, owner, status):
        if status not in {"complete", "paused", "failed"}:
            raise ValueError("invalid terminal status")
        run = self.get_run(run_id)
        if status == "complete" and run["completed"] != run["expected_count"]:
            raise ValueError("run incomplete")
        with self.connection:
            cursor = self.connection.execute(
                "UPDATE runs SET status=?,owner=NULL,lease_until=0 WHERE id=? AND owner=? AND lease_until>?",
                (status, run_id, owner, time.time()),
            )
            if cursor.rowcount != 1:
                raise RuntimeError("worker lease lost")

    def backup(self, path):
        from pathlib import Path

        if (
            self.path != ":memory:"
            and Path(path).resolve() == Path(self.path).resolve()
        ):
            raise ValueError("backup destination must differ from source")
        import os
        destination = Path(path)
        try:
            descriptor = os.open(destination, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        except FileExistsError as exc:
            raise ValueError("backup destination must not exist") from exc
        os.close(descriptor)
        try:
            target = sqlite3.connect(str(destination))
            try:
                self.connection.backup(target)
            finally:
                target.close()
        except BaseException:
            destination.unlink(missing_ok=True)
            raise

    def record_owned_attempt(self, run_id, case_id, payload, owner):
        """Fence durable retry accounting with the same lease as result writes."""
        self.connection.execute("BEGIN IMMEDIATE")
        try:
            row = self.connection.execute(
                "SELECT owner,lease_until FROM runs WHERE id=?", (run_id,)
            ).fetchone()
            if not row or row["owner"] != owner or row["lease_until"] <= time.time():
                raise RuntimeError("worker lease lost")
            self.record_attempt(run_id, case_id, payload)
            self.connection.commit()
        except BaseException:
            self.connection.rollback()
            raise
