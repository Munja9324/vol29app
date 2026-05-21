import kbrbot.app as app
from kbrbot.messages_ru import msg


def test_root_summary_payload_counts_basic_totals():
    records = [
        {
            "user_id": "100",
            "username": "alpha",
            "registration_date": "2026-05-01",
            "user_text": "Баланс: 50\nВсего пополнено: 150",
            "parsed_profile": {"balance_rub": 50.0, "total_topped_up_rub": 150.0},
            "subscriptions": [
                {
                    "subscription_id": "sub-1",
                    "location": "Финляндия",
                    "button_text": "sub-1",
                    "detail_text": "Истекает: 2099-01-01",
                }
            ],
        },
        {
            "user_id": "101",
            "username": "beta",
            "registration_date": "2026-05-02",
            "user_text": "",
            "parsed_profile": {"balance_rub": 0.0, "total_topped_up_rub": 0.0},
            "subscriptions": [],
        },
    ]

    summary = app.dashboard_root_summary_payload(records)

    assert summary["users_total"] == 2
    assert summary["paid_users_total"] == 1
    assert summary["subscriptions_total"] == 1
    assert summary["without_subscriptions_total"] == 1
    assert summary["total_balance_rub"] == 50.0
    assert summary["total_topped_up_rub"] == 150.0


def test_dashboard_user_recommendations_highlight_priority_cases():
    record = {
        "parsed_profile": {"balance_rub": 25.0},
        "subscriptions": [{}, {}],
    }
    row = {
        "status": "expiring_7",
        "subscriptions": 2,
        "open_requests_count": 1,
        "wizard_count": 3,
        "days_left": 2,
    }

    recommendations = app.dashboard_user_recommendations(record, row)
    text = "\n".join(recommendations)

    assert "открытые обращения" in text.lower()
    assert "несколько подписок" in text.lower()
    assert "приоритет" in text.lower()


def test_messages_ru_are_readable():
    assert msg("wizard.sent") == "Карточка отправлена"
