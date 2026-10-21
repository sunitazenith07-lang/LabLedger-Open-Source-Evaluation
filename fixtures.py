"""Synthetic demo records; no real customer or payment data is used."""
from models import new_transaction


def sample_transactions() -> list[dict]:
    return [
        new_transaction("TX-1001", 159900, "SUCCEEDED"),
        new_transaction("TX-1002", 49900, "PENDING"),
        new_transaction("TX-1003", 25000, "FAILED"),
    ]


def sample_provider_records() -> list[dict]:
    return [
        {"transaction_id": "TX-1001", "amount_paise": 159900, "status": "SUCCEEDED"},
        {"transaction_id": "TX-1002", "amount_paise": 49900, "status": "SUCCEEDED"},
        {"transaction_id": "TX-1004", "amount_paise": 8900, "status": "SUCCEEDED"},
    ]
