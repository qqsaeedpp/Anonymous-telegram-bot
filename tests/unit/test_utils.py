from app.utils.id_generator import generate_anonymous_id
from app.utils.text_sanitizer import is_blank, sanitize_text
from app.utils.token_generator import generate_public_token


def test_tokens_are_unique_and_urlsafe():
    tokens = {generate_public_token() for _ in range(1000)}
    assert len(tokens) == 1000
    for t in tokens:
        assert all(c.isalnum() or c in "-_" for c in t)
        assert len(t) <= 64


def test_anonymous_id_has_prefix():
    assert generate_anonymous_id().startswith("anon-")


def test_sanitize_escapes_and_clamps():
    out = sanitize_text("  <b>hi</b>  ", max_length=100)
    assert out == "&lt;b&gt;hi&lt;/b&gt;"
    assert len(sanitize_text("x" * 50, max_length=10)) == 10


def test_is_blank():
    assert is_blank("") and is_blank("   ") and is_blank(None)
    assert not is_blank("a")
