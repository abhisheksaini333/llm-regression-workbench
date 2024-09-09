from regression_workbench.evaluators import extraction,schema,tool

def test_nested_boolean_number_values_never_compare_equal():
    assert extraction('{"a":[true]}',{"a":[1]})["score"] == 0
    assert schema('{"a":true}',{"properties":{"a":{"enum":[1]}}})["score"] == 0
    assert tool('{"tool":"x","arguments":{"a":{"b":true}}}',{"tool":"x","arguments":{"a":{"b":1}}})["score"] == 0
    assert extraction('{"a":1.0}',{"a":1})["score"] == 1
