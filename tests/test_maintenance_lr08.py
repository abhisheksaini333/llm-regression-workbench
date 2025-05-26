import pytest
from regression_workbench.review import calibrate

def test_orphan_reviews_do_not_qualify_calibration():
    pairs=[{"case_id":"a","delta":.1}]
    labels=[{"case_id":"x","preference":"tie"},{"case_id":"y","preference":"tie"}]
    with pytest.raises(ValueError): calibrate(pairs,labels)

def test_duplicate_reviewers_do_not_multiply_evidence():
    pairs=[{"case_id":"a","delta":.1}]
    label={"case_id":"a","reviewer":"u","preference":"tie"}
    with pytest.raises(ValueError): calibrate(pairs,[label,label])
