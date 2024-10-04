import pytest
from regression_workbench.comparison import pair

@pytest.mark.parametrize("bad", [True,"0.5",None])
def test_scores_validated_before_delta(bad):
    a={"case_id":"x","score":.5,"task":"summary"}
    with pytest.raises(ValueError): pair([a],[dict(a,score=bad)])
