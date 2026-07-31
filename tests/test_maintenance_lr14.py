import hashlib,io
import pytest
from regression_workbench.artifacts import download

def test_cached_artifact_cannot_be_a_symlink(tmp_path):
    outside=tmp_path/"outside";outside.write_bytes(b"model")
    cache=tmp_path/"cache";cache.mkdir();(cache/"model.bin").symlink_to(outside)
    row={"file":"model.bin","url":"https://example.org/model","bytes":5,"sha256":hashlib.sha256(b"model").hexdigest()}
    with pytest.raises(ValueError): download([row],cache,lambda *a,**k:io.BytesIO(b"model"))
    assert outside.read_bytes() == b"model"

def test_racing_artifact_is_not_overwritten(tmp_path):
    row={"file":"model.bin","url":"https://example.org/model","bytes":5,"sha256":hashlib.sha256(b"model").hexdigest()}
    def fetch(*a,**k):
        (tmp_path/"model.bin").write_bytes(b"racing")
        return io.BytesIO(b"model")
    with pytest.raises((ValueError,FileExistsError)): download([row],tmp_path,fetch)
    assert (tmp_path/"model.bin").read_bytes() == b"racing"
