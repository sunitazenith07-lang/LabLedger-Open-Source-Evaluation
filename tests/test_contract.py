import pytest

from models import new_transaction
from service import apply_event, reconcile_transactions


def test_successful_payment_changes_pending_to_succeeded():
    tx = new_transaction("TX-1", 1000)
    result = apply_event(tx, {"event_id": "EV-1", "type": "payment_succeeded"})
    assert result["status"] == "SUCCEEDED"
    assert result["processed_event_ids"] == ["EV-1"]
    assert tx["status"] == "PENDING"  # input is not mutated


def test_failed_payment_changes_pending_to_failed():
    tx = new_transaction("TX-1", 1000)
    result = apply_event(tx, {"event_id": "EV-2", "type": "payment_failed"})
    assert result["status"] == "FAILED"


def test_duplicate_event_is_idempotent():
    tx = new_transaction("TX-1", 1000)
    event = {"event_id": "EV-1", "type": "payment_succeeded"}
    once = apply_event(tx, event)
    twice = apply_event(once, event)
    assert twice["processed_event_ids"] == ["EV-1"]


def test_refund_requires_successful_payment():
    tx = new_transaction("TX-1", 1000)
    result = apply_event(tx, {
        "event_id": "EV-R1", "type": "refund_succeeded", "amount_paise": 1000
    })
    assert result["status"] == "PENDING"
    assert result["refunded_paise"] == 0


def test_refund_cannot_exceed_original_amount():
    tx = new_transaction("TX-1", 1000, "SUCCEEDED")
    result = apply_event(tx, {
        "event_id": "EV-R2", "type": "refund_succeeded", "amount_paise": 1200
    })
    assert result["refunded_paise"] == 0
    assert result["status"] == "SUCCEEDED"


def test_zero_or_negative_refund_is_ignored():
    for amount in (0, -1):
        tx = new_transaction("TX-1", 1000, "SUCCEEDED")
        result = apply_event(tx, {
            "event_id": "EV-R3", "type": "refund_succeeded", "amount_paise": amount
        })
        assert result["refunded_paise"] == 0
        assert result["status"] == "SUCCEEDED"


def test_partial_refund_does_not_mark_transaction_fully_refunded():
    tx = new_transaction("TX-1", 1000, "SUCCEEDED")
    result = apply_event(tx, {
        "event_id": "EV-R4", "type": "refund_succeeded", "amount_paise": 400
    })
    assert result["refunded_paise"] == 400
    assert result["status"] == "SUCCEEDED"


def test_matching_records_are_reported_as_matched():
    tx = {"transaction_id": "TX-1", "amount_paise": 1000, "status": "SUCCEEDED"}
    report = reconcile_transactions([tx], [dict(tx)])
    assert report["matched"] == ["TX-1"]
    assert report["amount_mismatches"] == []
    assert report["status_mismatches"] == []


def test_amount_mismatch_is_reported():
    internal = [{"transaction_id": "TX-1", "amount_paise": 1000, "status": "SUCCEEDED"}]
    provider = [{"transaction_id": "TX-1", "amount_paise": 900, "status": "SUCCEEDED"}]
    report = reconcile_transactions(internal, provider)
    assert report["amount_mismatches"] == ["TX-1"]
    assert report["matched"] == []


def test_status_mismatch_is_not_mislabelled_as_matched():
    internal = [{"transaction_id": "TX-1", "amount_paise": 1000, "status": "PENDING"}]
    provider = [{"transaction_id": "TX-1", "amount_paise": 1000, "status": "SUCCEEDED"}]
    report = reconcile_transactions(internal, provider)
    assert report["status_mismatches"] == ["TX-1"]
    assert report["matched"] == []


def test_missing_records_are_reported_on_correct_side():
    internal = [
        {"transaction_id": "TX-A", "amount_paise": 100, "status": "SUCCEEDED"},
    ]
    provider = [
        {"transaction_id": "TX-B", "amount_paise": 200, "status": "FAILED"},
    ]
    report = reconcile_transactions(internal, provider)
    assert report["missing_from_provider"] == ["TX-A"]
    assert report["missing_from_internal"] == ["TX-B"]


def test_empty_reconciliation_returns_empty_lists():
    report = reconcile_transactions([], [])
    assert all(value == [] for value in report.values())


def test_unknown_event_does_not_change_payment_status():
    tx = new_transaction("TX-1", 1000)
    result = apply_event(tx, {"event_id": "EV-X", "type": "unrecognised"})
    assert result["status"] == "PENDING"
