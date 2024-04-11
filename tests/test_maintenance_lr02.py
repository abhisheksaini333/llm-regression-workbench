import pytest
from regression_workbench.config import validate

@pytest.mark.parametrize("bad", [True, float("nan"),float("inf"),"0"])
def test_temperature_is_a_finite_number(bad):
    with pytest.raises(ValueError): validate({"model":"m","prompt":"{input}","parameters":{"temperature":bad}})
