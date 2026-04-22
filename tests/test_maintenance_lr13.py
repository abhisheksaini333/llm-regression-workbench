from regression_workbench.redaction import sanitize

def test_url_userinfo_and_encoded_secrets_are_redacted():
    assert "user:password" not in sanitize("https://user:password@example.org/a")
    assert "s%20ecret" not in sanitize("https://example.org/a?v=s%20ecret",["s ecret"])
    assert sanitize("https://example.org/docs") == "https://example.org/docs"
