import pytest
from regression_workbench.comparison import operational

@pytest.mark.parametrize("field,bad", [("input_tokens",-1),("output_tokens",True),("output_tokens",1.5),("latency_ms",True),("latency_ms","2"),("usage_kind","bogus")])
def test_operational_measurements_reject_corruption(field,bad):
    row={"latency_ms":1,"input_tokens":2,"output_tokens":3,"usage_kind":"tokens"}
    row[field]=bad
    with pytest.raises(ValueError): operational([row])
