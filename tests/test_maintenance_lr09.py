import pytest
from regression_workbench.store import Store
from regression_workbench.review import save, list_reviews

@pytest.mark.parametrize("bad", [False,0.0,-1])
def test_review_revision_is_a_nonnegative_integer(bad):
    with Store(":memory:") as store:
        for run in ("a","b"):
            store.register(run,"d",{},0,1);store.save_result(run,"c",{"score":1})
        with pytest.raises(ValueError): save(store,"a","b","c","u","tie",expected_revision=bad)
        assert list_reviews(store,"a","b") == []
