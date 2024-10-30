import pytest
from regression_workbench.comparison import bootstrap

@pytest.mark.parametrize("settings", [{"resamples":100.5},{"resamples":100001},{"confidence":True}])
def test_bootstrap_settings_are_bounded(settings):
    with pytest.raises(ValueError): bootstrap([.1,.2],**settings)

@pytest.mark.parametrize("bad", [True,"1",None])
def test_bootstrap_observations_are_numeric(bad):
    with pytest.raises(ValueError): bootstrap([bad])
