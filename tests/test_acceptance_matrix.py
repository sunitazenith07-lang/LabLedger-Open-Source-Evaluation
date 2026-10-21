import pytest
from models import new_transaction
from service import apply_event, reconcile_transactions


SUCCESS_STATES = ["PENDING", "FAILED", "SUCCEEDED", "REFUNDED"]
FAIL_STATES = ["PENDING", "FAILED", "SUCCEEDED", "REFUNDED"]


@pytest.mark.parametrize("status,expected", [
    ("PENDING", "SUCCEEDED"), ("FAILED", "FAILED"),
    ("SUCCEEDED", "SUCCEEDED"), ("REFUNDED", "REFUNDED"),
])
def test_payment_success_transition_matrix(status, expected):
    tx = new_transaction("TX", 5000, status)
    out = apply_event(tx, {"event_id": "EV", "type": "payment_succeeded"})
    assert out["status"] == expected


@pytest.mark.parametrize("status,expected", [
    ("PENDING", "FAILED"), ("FAILED", "FAILED"),
    ("SUCCEEDED", "SUCCEEDED"), ("REFUNDED", "REFUNDED"),
])
def test_payment_failure_transition_matrix(status, expected):
    tx = new_transaction("TX", 5000, status)
    out = apply_event(tx, {"event_id": "EV", "type": "payment_failed"})
    assert out["status"] == expected


@pytest.mark.parametrize("event_id", [f"SUCCESS-{i:02}" for i in range(20)])
def test_success_event_replay_is_idempotent_for_many_ids(event_id):
    tx = new_transaction("TX", 5000)
    event = {"event_id": event_id, "type": "payment_succeeded"}
    once = apply_event(tx, event)
    twice = apply_event(once, event)
    assert twice["status"] == "SUCCEEDED"
    assert twice["processed_event_ids"] == [event_id]


@pytest.mark.parametrize("amount", [1, 2, 10, 50, 99, 100, 250, 499, 500, 750, 999, 1000, 1250, 2500, 4999, 5000])
def test_valid_refund_amounts_are_applied_exactly(amount):
    tx = new_transaction("TX", 5000, "SUCCEEDED")
    out = apply_event(tx, {"event_id": "R1", "type": "refund_succeeded", "amount_paise": amount})
    assert out["refunded_paise"] == amount
    assert out["status"] == ("REFUNDED" if amount == 5000 else "SUCCEEDED")


@pytest.mark.parametrize("amount", [0, -1, -5, -100, -999, 5001, 6000, 10000, None, 1.5, True, "100", [], {}])
def test_invalid_refund_values_do_not_change_ledger(amount):
    tx = new_transaction("TX", 5000, "SUCCEEDED")
    out = apply_event(tx, {"event_id": "R1", "type": "refund_succeeded", "amount_paise": amount})
    assert out["refunded_paise"] == 0
    assert out["status"] == "SUCCEEDED"


@pytest.mark.parametrize("status", ["PENDING", "FAILED", "REFUNDED"])
@pytest.mark.parametrize("amount", [1, 2500, 5000])
def test_refunds_require_successful_payment(status, amount):
    tx = new_transaction("TX", 5000, status)
    out = apply_event(tx, {"event_id": "R1", "type": "refund_succeeded", "amount_paise": amount})
    assert out["refunded_paise"] == 0
    assert out["status"] == status


@pytest.mark.parametrize("first,second", [
    (100, 200), (100, 900), (200, 800), (250, 750), (499, 501),
    (500, 500), (700, 300), (999, 1), (800, 201), (400, 601),
    (1, 999), (333, 667), (600, 400), (1200, 3800), (4500, 500),
    (3000, 2000), (2000, 3001), (5000, 1), (4500, 600), (2500, 2500),
])
def test_cumulative_refunds_never_exceed_original_amount(first, second):
    tx = new_transaction("TX", 5000, "SUCCEEDED")
    once = apply_event(tx, {"event_id": "R1", "type": "refund_succeeded", "amount_paise": first})
    twice = apply_event(once, {"event_id": "R2", "type": "refund_succeeded", "amount_paise": second})
    if first + second <= 5000:
        assert twice["refunded_paise"] == first + second
    else:
        assert twice["refunded_paise"] == first
    assert 0 <= twice["refunded_paise"] <= 5000


@pytest.mark.parametrize("left,right", [
    ("PENDING","PENDING"), ("PENDING","SUCCEEDED"), ("PENDING","FAILED"),
    ("SUCCEEDED","PENDING"), ("SUCCEEDED","SUCCEEDED"), ("SUCCEEDED","FAILED"),
    ("FAILED","PENDING"), ("FAILED","FAILED"), ("REFUNDED","REFUNDED"),
    ("REFUNDED","SUCCEEDED"), ("FAILED","REFUNDED"), ("SUCCEEDED","REFUNDED"),
])
def test_reconciliation_status_matrix(left, right):
    internal = [{"transaction_id":"TX", "amount_paise":5000, "status":left}]
    provider = [{"transaction_id":"TX", "amount_paise":5000, "status":right}]
    report = reconcile_transactions(internal, provider)
    if left == right:
        assert report["matched"] == ["TX"]
        assert report["status_mismatches"] == []
    else:
        assert report["matched"] == []
        assert report["status_mismatches"] == ["TX"]


@pytest.mark.parametrize("internal_amount,provider_amount", [
    (0,1),(1,0),(1,2),(2,1),(99,100),(100,99),(499,500),(500,499),
    (999,1000),(1000,999),(10000,9999),(9999,10000),(12345,12346),
    (159900,159901),(5000,0),(5000,10000),(10,5000),(5000,10),
    (888,777),(777,888),
])
def test_reconciliation_amount_mismatch_matrix(internal_amount, provider_amount):
    report = reconcile_transactions(
        [{"transaction_id":"TX","amount_paise":internal_amount,"status":"SUCCEEDED"}],
        [{"transaction_id":"TX","amount_paise":provider_amount,"status":"SUCCEEDED"}],
    )
    assert report["amount_mismatches"] == ["TX"]
    assert report["matched"] == []


@pytest.mark.parametrize("txid", [f"IN-{i:02}" for i in range(20)])
def test_internal_only_records_are_reported(txid):
    report = reconcile_transactions(
        [{"transaction_id":txid,"amount_paise":1,"status":"PENDING"}], []
    )
    assert report["missing_from_provider"] == [txid]
    assert report["missing_from_internal"] == []


@pytest.mark.parametrize("txid", [f"PROV-{i:02}" for i in range(20)])
def test_provider_only_records_are_reported(txid):
    report = reconcile_transactions(
        [], [{"transaction_id":txid,"amount_paise":1,"status":"PENDING"}]
    )
    assert report["missing_from_internal"] == [txid]
    assert report["missing_from_provider"] == []


@pytest.mark.parametrize("count", list(range(1, 16)))
def test_reconciliation_sorting_is_deterministic(count):
    ids = [f"TX-{i:02}" for i in range(count)]
    internal = [{"transaction_id":x,"amount_paise":100,"status":"OK"} for x in reversed(ids)]
    provider = [{"transaction_id":x,"amount_paise":100,"status":"OK"} for x in ids[::2]]
    report = reconcile_transactions(internal, provider)
    assert report["matched"] == sorted(ids[::2], key=str)
    assert report["missing_from_provider"] == sorted(ids[1::2], key=str)


@pytest.mark.parametrize("kind", ["", "unknown", "refund", "payment_succeeded_v2", None, 1, "PAYMENT_FAILED", "chargeback", "settled", "retry"])
def test_unknown_event_does_not_change_transaction_status(kind):
    tx = new_transaction("TX", 5000, "PENDING")
    out = apply_event(tx, {"event_id":"EV-X","type":kind,"amount_paise":3000})
    assert out["status"] == "PENDING"
    assert out["refunded_paise"] == 0


@pytest.mark.parametrize("amount", [1, 100, 999, 1000, 5000])
def test_apply_event_does_not_mutate_input(amount):
    tx = new_transaction("TX", 5000, "SUCCEEDED")
    before = dict(tx)
    apply_event(tx, {"event_id":"EV","type":"refund_succeeded","amount_paise":amount})
    assert tx == before


@pytest.mark.parametrize("amount", [1, 100, 499, 500, 1000, 2000, 4999, 5000])
def test_full_refund_status_changes_only_at_exact_total(amount):
    tx = new_transaction("TX", 5000, "SUCCEEDED")
    out = apply_event(tx, {"event_id":"R","type":"refund_succeeded","amount_paise":amount})
    assert out["status"] == ("REFUNDED" if amount == 5000 else "SUCCEEDED")


@pytest.mark.parametrize("amount", [1, 25, 100, 1000, 2500, 4999, 5000, 5001, -100, 0])
def test_refund_against_already_failed_payment_never_changes_amount(amount):
    tx = new_transaction("TX", 5000, "FAILED")
    out = apply_event(tx, {"event_id":"R","type":"refund_succeeded","amount_paise":amount})
    assert out["refunded_paise"] == 0
    assert out["status"] == "FAILED"
