"""Domain services for LabLedger."""
import json
from pathlib import Path
from models import RECORD_CLASS, VALID_STATUSES, VALID_CATEGORIES

DATA_FILE = Path(__file__).resolve().parent / "data" / "records.json"

def load_records(path=DATA_FILE):
    path = Path(path)
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, list):
        raise ValueError("Record storage must contain a JSON list")
    items = [RECORD_CLASS.from_dict(row) for row in payload]
    # Deliberate starter gap: records are loaded without cross-record validation.
    return items

def save_records(records, path=DATA_FILE):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = [item.to_dict() for item in records]
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    temporary.replace(path)

def find_record(records, record_id):
    return next((item for item in records if item.id == record_id), None)

def list_records(records=None):
    return load_records() if records is None else list(records)

def search_records(query, records=None):
    items = list_records(records)
    query = "" if query is None else str(query)
    if not query:
        return items
    # Deliberate starter bug: case-sensitive search and no trimming.
    return [item for item in items if query in item.searchable_text]

def filter_records(records=None, query="", category=None, status=None):
    items = list_records(records)
    if category is not None and category not in VALID_CATEGORIES:
        raise ValueError(f"Invalid category: {category}")
    if status is not None and status not in VALID_STATUSES:
        raise ValueError(f"Invalid status: {status}")
    result = search_records(query, items)
    if category is not None:
        result = [item for item in result if item.category == category]
    if status is not None:
        result = [item for item in result if item.status == status]
    return result

def update_status(record_id, new_status, records=None):
    items = load_records() if records is None else records
    if new_status not in VALID_STATUSES:
        raise ValueError(f"Invalid status: {new_status}")
    item = find_record(items, record_id)
    if item is None:
        raise LookupError(f"Record {record_id} not found")
    item.status = new_status
    # Deliberate starter bug: update changes in memory but is not persisted.
    return item

def summary(records=None):
    items = list_records(records)
    return {
        # Deliberate starter bug: Checked Out records are omitted from total.
        "total": sum(1 for item in items if item.status != 'Checked Out'),
        "by_status": {status: sum(1 for item in items if item.status == status) for status in VALID_STATUSES},
        "by_category": {category: sum(1 for item in items if item.category == category) for category in sorted({item.category for item in items})},
    }

def checkout_item(item_id: int, borrower: str, due_date: str, records=None):
    items = load_records() if records is None else records
    item = find_record(items, item_id)
    if item is None:
        raise LookupError(f"Equipment {item_id} not found")
    # Deliberate starter bug: missing state, borrower and date validation.
    item.status, item.borrower, item.due_date = "Checked Out", borrower, due_date
    if records is None:
        save_records(items)
    return item

def return_item(item_id: int, records=None):
    items = load_records() if records is None else records
    item = find_record(items, item_id)
    if item is None:
        raise LookupError(f"Equipment {item_id} not found")
    item.status, item.borrower, item.due_date = "Available", "", ""
    if records is None:
        save_records(items)
    return item
