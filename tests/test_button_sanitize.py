from types import SimpleNamespace

from kbrbot.core.text_sanitize import sanitize_buttons


def test_sanitize_buttons_resolves_callable_url_values():
    buttons = [[SimpleNamespace(text="Открыть", url=lambda: "https://example.com")]]

    sanitized = sanitize_buttons(buttons)

    assert sanitized
    button = sanitized[0][0]
    assert getattr(button, "text", "") == "Открыть"
    assert getattr(button, "url", "") == "https://example.com"
