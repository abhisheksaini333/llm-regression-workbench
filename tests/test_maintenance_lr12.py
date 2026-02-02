import pytest
from regression_workbench.store import Store

def test_backup_refuses_existing_destinations(tmp_path):
    target=tmp_path/"backup.db";target.write_bytes(b"preserve")
    with Store(tmp_path/"live.db") as store:
        with pytest.raises(ValueError): store.backup(target)
    assert target.read_bytes() == b"preserve"

def test_backup_is_private(tmp_path):
    target=tmp_path/"backup.db"
    with Store(tmp_path/"live.db") as store: store.backup(target)
    assert target.stat().st_mode & 0o777 == 0o600
