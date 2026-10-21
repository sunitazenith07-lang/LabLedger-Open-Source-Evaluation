"""Small data helpers for the simulated payment ledger."""


def new_transaction(transaction_id: str, amount_paise: int, status: str = "PENDING") -> dict:
    return {
        "transaction_id": transaction_id,
        "amount_paise": amount_paise,
        "status": status,
        "refunded_paise": 0,
        "processed_event_ids": [],
    }
