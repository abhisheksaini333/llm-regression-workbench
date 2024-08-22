from regression_workbench.evaluators import parse_object, extraction, tool

def test_duplicate_json_fields_are_invalid():
    assert parse_object('{"a":0,"a":1}') is None
    assert parse_object('{"a":{"b":0,"b":1}}') is None
    assert extraction('{"a":0,"a":1}', {"a":1})["score"] == 0
    assert parse_object('{"a":1}') == {"a":1}
