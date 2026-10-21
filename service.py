"""Starter service for a simulated payment ledger and reconciliation engine."""
from copy import deepcopy


def apply_event(transaction: dict, event: dict) -> dict:
    """Return a new transaction after applying one provider event.

    Expected transaction keys: transaction_id, amount_paise, status,
    refunded_paise, processed_event_ids.
    """
    updated = deepcopy(transaction)
    updated.setdefault("refunded_paise", 0)
    updated.setdefault("processed_event_ids", [])
    event_id = event.get("event_id")
    event_type = event.get("type")
    amount = event.get("amount_paise", 0)

    # Deliberate starter defects: duplicate events and invalid refunds are not
    # yet handled safely. Identify and fix them without changing the function
    # contract used by the visible tests.
    if event_type == "payment_succeeded":
        updated["status"] = "SUCCEEDED"
    elif event_type == "payment_failed":
        if updated.get("status") == "PENDING":
            updated["status"] = "FAILED"
    elif event_type == "refund_succeeded":
        updated["refunded_paise"] += amount
        if updated["refunded_paise"] >= updated.get("amount_paise", 0):
            updated["status"] = "REFUNDED"

    updated["processed_event_ids"].append(event_id)
    return updated


def reconcile_transactions(internal_records: list[dict], provider_records: list[dict]) -> dict:
    """Compare internal records with a provider export.

    Returns lists named matched, missing_from_provider, missing_from_internal,
    amount_mismatches and status_mismatches. Each list contains transaction IDs.
    """
    internal = {row.get("transaction_id"): row for row in internal_records}
    provider = {row.get("transaction_id"): row for row in provider_records}
    result = {
        "matched": [],
        "missing_from_provider": [],
        "missing_from_internal": [],
        "amount_mismatches": [],
        "status_mismatches": [],
    }
    for transaction_id in sorted(set(internal) | set(provider), key=lambda item: str(item)):
        if transaction_id not in provider:
            result["missing_from_provider"].append(transaction_id)
        elif transaction_id not in internal:
            result["missing_from_internal"].append(transaction_id)
        else:
            left, right = internal[transaction_id], provider[transaction_id]
            if left.get("amount_paise") != right.get("amount_paise"):
                result["amount_mismatches"].append(transaction_id)
            # Deliberate starter defect: status differences are not reported.
            else:
                result["matched"].append(transaction_id)
    return result
