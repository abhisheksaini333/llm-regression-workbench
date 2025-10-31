import pytest
from regression_workbench.store import Store
from regression_workbench.runner import run
from regression_workbench.providers import FixtureProvider

@pytest.mark.parametrize("bad", [True,float("nan"),float("inf"),-1])
def test_invalid_lease_never_registers_a_run(bad):
    data={"version":1,"name":"d","cases":[{"id":"c","task":"summary","input":"x","expected":{"keywords":["x"]}}]}
    with Store(":memory:") as store:
        with pytest.raises(ValueError): run(data,{"model":"m","prompt":"{input}"},FixtureProvider({"c":"x"}),store,lease_seconds=bad)
        assert store.list_runs() == []

def test_invalid_claim_identity_and_clock():
    with Store(":memory:") as store:
        store.register("r","d",{},0,1)
        with pytest.raises(ValueError): store.claim("r","",10,now=0)
        with pytest.raises(ValueError): store.claim("r","u",10,now=float("nan"))
