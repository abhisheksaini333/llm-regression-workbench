import pytest
from regression_workbench.dataset import validate

@pytest.mark.parametrize("version", [True, 1.0])
def test_strict_dataset_version(version):
    with pytest.raises(ValueError): validate({"version":version,"name":"d","cases":[]})

def test_nonfinite_dataset_content():
    with pytest.raises(ValueError): validate({"version":1,"name":"d","cases":[],"metadata":{"score":float("nan")}})
