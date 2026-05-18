from kbrbot.app import is_explicit_requester_command_input, parse_scan_menu_action


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
