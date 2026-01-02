import sqlite3
import pytest
from regression_workbench.store import Store

def test_unknown_schema_is_not_relabelled(tmp_path):
    path=tmp_path/"future.db"
    with sqlite3.connect(path) as db: db.execute("PRAGMA user_version=2")
    with pytest.raises(ValueError): Store(path)
    with sqlite3.connect(path) as db:
        assert db.execute("PRAGMA user_version").fetchone()[0] == 2
        assert db.execute("SELECT count(*) FROM sqlite_master").fetchone()[0] == 0
