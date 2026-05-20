import asyncio

import kbrbot.app as app
from kbrbot.app import (
    cancel_pending_requester_workflows,
    dashboard_api_cache_get,
    dashboard_api_cache_set,
    is_explicit_requester_command_input,
    parse_scan_menu_action,
)


def test_scan_slash_variants_are_recognized():
    assert parse_scan_menu_action("/scan", allow_numeric=False) == "menu"
    assert parse_scan_menu_action("/scan new", allow_numeric=False) == "new"
    assert parse_scan_menu_action("/scan continue", allow_numeric=False) == "continue"
    assert parse_scan_menu_action("/scan results", allow_numeric=False) == "results"
    assert parse_scan_menu_action("/scan pause", allow_numeric=False) == "pause_results"
    assert parse_scan_menu_action("/scan reset", allow_numeric=False) == "reset"
    assert parse_scan_menu_action("/scan scan", allow_numeric=False) == "new"


def test_requester_commands_stay_explicit_in_public_mode():
    sender_id = 123
    assert is_explicit_requester_command_input("menu", sender_id) is True
    assert is_explicit_requester_command_input("/dashboard", sender_id) is True
    assert is_explicit_requester_command_input("/adminsite", sender_id) is True
    assert is_explicit_requester_command_input("/root", sender_id) is True
    assert is_explicit_requester_command_input("/diag", sender_id) is True
    assert is_explicit_requester_command_input("/processes", sender_id) is True
    assert is_explicit_requester_command_input("/version", sender_id) is True
    assert is_explicit_requester_command_input("/tail 20", sender_id) is True
    assert is_explicit_requester_command_input("/unresolved", sender_id) is True
    assert is_explicit_requester_command_input("/user 1232", sender_id) is True
    assert is_explicit_requester_command_input("/user test_user -b", sender_id) is True
    assert is_explicit_requester_command_input("/subs 1232", sender_id) is True
    assert is_explicit_requester_command_input("/subs test_user -b", sender_id) is True
    assert is_explicit_requester_command_input("/wizard 1232", sender_id) is True
    assert is_explicit_requester_command_input("/send 1232 привет", sender_id) is True
    assert is_explicit_requester_command_input("/broadcast текст", sender_id) is True
    assert is_explicit_requester_command_input("/coupon 1232", sender_id) is True
    assert is_explicit_requester_command_input("/tpl key", sender_id) is True
    assert is_explicit_requester_command_input("/scan new", sender_id) is True
    assert is_explicit_requester_command_input("/roots add me", sender_id) is True


def test_explicit_command_can_clear_pending_requester_workflows():
    sender_id = 777
    app.pending_wizard_requests[sender_id] = {"stage": "await_choice"}
    app.pending_mail2_requests[sender_id] = {"stage": "await_text"}
    app.pending_direct_mail_requests[sender_id] = {"user_id": "123"}

    cleared = set(cancel_pending_requester_workflows(sender_id))

    assert cleared == {"wizard", "mail2", "mail"}
    assert sender_id not in app.pending_wizard_requests
    assert sender_id not in app.pending_mail2_requests
    assert sender_id not in app.pending_direct_mail_requests


def test_dashboard_overview_cache_bypassed_while_scan_is_active():
    key = "admin-api::overview::"
    original_scan_event = app.active_scan_cancel_event
    try:
        dashboard_api_cache_set(key, {"ok": True, "value": 1})
        assert dashboard_api_cache_get(key) == {"ok": True, "value": 1}

        app.active_scan_cancel_event = asyncio.Event()
        assert dashboard_api_cache_get(key) is None
    finally:
        app.active_scan_cancel_event = original_scan_event
