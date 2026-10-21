"""Run a small offline demonstration of LabLedger."""
from fixtures import sample_provider_records, sample_transactions
from service import reconcile_transactions


if __name__ == "__main__":
    report = reconcile_transactions(sample_transactions(), sample_provider_records())
    for category, transaction_ids in report.items():
        print(f"{category}: {transaction_ids}")
