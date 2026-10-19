"""110-case contract for the LabLedger starter."""
import json
from copy import deepcopy
import pytest

from models import RECORD_CLASS, FIELD_NAMES, VALID_STATUSES, VALID_CATEGORIES
import service as service
from service import (
    load_records, save_records, find_record, list_records, search_records,
    filter_records, update_status, summary, checkout_item
)
from fixtures import make_records

STATUS_CHECKS = ['Available', 'Checked Out', 'Maintenance']
STATUS_VALUES = ['Available', 'Checked Out', 'Maintenance']
CATEGORY_CHECKS = ['Electronics', 'Tools', 'Fabrication', 'Computing']
CLOSED_STATUS = 'Checked Out'
SEARCH_CASES = [('Arduino', [1]), ('LAB-001', [1]), ('Oscilloscope', [2]), ('3D Printer', [3]), ('Laptop', [4]), ('Digital Sensor', [5]), ('Soldering', [6]), ('MISSING-ASSET', [])]
NORMALIZATION_CASES = [('arduino', [1]), ('ARDUINO', [1]), (' Arduino Kit Alpha ', [1]), ('aRdUiNo', [1]), ('lab-001', [1]), (' lab-001 ', [1]), ('oscilloscope', [2]), (' OSCILLOSCOPE ', [2])]

@pytest.mark.parametrize("field", FIELD_NAMES)
def test_model_serialisation_preserves_each_field(field):
    item = make_records()[0]
    row = item.to_dict()
    assert field in row
    assert row[field] == getattr(item, field)

@pytest.mark.parametrize("status", STATUS_CHECKS)
def test_sample_status_values_are_supported(status):
    assert status in VALID_STATUSES

@pytest.mark.parametrize("size", [1, 2, 4, 6])
def test_storage_round_trip(tmp_path, size):
    path = tmp_path / "nested" / "records.json"
    expected = make_records()[:size]
    save_records(expected, path)
    assert [x.to_dict() for x in load_records(path)] == [x.to_dict() for x in expected]

def test_missing_storage_returns_empty_list(tmp_path):
    assert load_records(tmp_path / "missing.json") == []

def test_storage_creates_parent_directories(tmp_path):
    path = tmp_path / "nested" / "child" / "data.json"
    save_records(make_records()[:1], path)
    assert path.exists() and len(load_records(path)) == 1

def test_storage_preserves_unicode(tmp_path):
    items = make_records()
    items[0].name = "Café — test record"
    path = tmp_path / "unicode.json"
    save_records(items[:1], path)
    assert load_records(path)[0].name == "Café — test record"

def test_malformed_json_is_reported(tmp_path):
    path = tmp_path / "broken.json"
    path.write_text("[broken", encoding="utf-8")
    with pytest.raises(json.JSONDecodeError): load_records(path)

def test_non_list_json_is_rejected(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text('{"not": "a list"}', encoding="utf-8")
    with pytest.raises(ValueError): load_records(path)

def test_missing_required_model_field_is_rejected():
    payload = make_records()[0].to_dict()
    payload.pop(FIELD_NAMES[0])
    with pytest.raises(ValueError): RECORD_CLASS.from_dict(payload)

@pytest.mark.parametrize("record_id,expected", [(1,1),(2,2),(3,3),(6,6),(999,None)])
def test_find_record_by_id(record_id, expected):
    found = find_record(make_records(), record_id)
    assert (found.id if found else None) == expected

@pytest.mark.parametrize("category", CATEGORY_CHECKS)
def test_filter_by_each_category_returns_only_that_category(category):
    result = filter_records(make_records(), category=category)
    assert all(item.category == category for item in result)
    assert [item.id for item in result] == [item.id for item in make_records() if item.category == category]

@pytest.mark.parametrize("status", STATUS_CHECKS)
def test_filter_by_each_status_returns_only_that_status(status):
    result = filter_records(make_records(), status=status)
    assert all(item.status == status for item in result)
    assert [item.id for item in result] == [item.id for item in make_records() if item.status == status]

@pytest.mark.parametrize("category,status", [(CATEGORY_CHECKS[0],STATUS_CHECKS[0]),(CATEGORY_CHECKS[1],STATUS_CHECKS[1]),(CATEGORY_CHECKS[2],STATUS_CHECKS[2]),(CATEGORY_CHECKS[3],STATUS_CHECKS[0]),(CATEGORY_CHECKS[0],STATUS_CHECKS[2]),(CATEGORY_CHECKS[1],STATUS_CHECKS[0])])
def test_combined_category_and_status_filters(category, status):
    result = filter_records(make_records(), category=category, status=status)
    expected = [item.id for item in make_records() if item.category == category and item.status == status]
    assert [item.id for item in result] == expected

@pytest.mark.parametrize("kwargs", [{"status":"NOT-VALID"},{"category":"NOT-VALID"},{"status":""},{"category":""}])
def test_invalid_filter_values_raise(kwargs):
    with pytest.raises(ValueError): filter_records(make_records(), **kwargs)

@pytest.mark.parametrize("query,expected", SEARCH_CASES)
def test_exact_case_search_contract(query, expected):
    assert [item.id for item in search_records(query, make_records())] == expected

def test_empty_search_returns_every_record():
    assert len(search_records("", make_records())) == 6

def test_missing_search_query_is_safe():
    assert len(search_records(None, make_records())) == 6

def test_search_with_no_matches_returns_empty_list():
    assert search_records("NO-SUCH-RECORD-991", make_records()) == []

@pytest.mark.parametrize("status", STATUS_CHECKS)
def test_update_status_mutates_an_explicit_list(status):
    items = make_records()
    result = update_status(1, status, items)
    assert result.status == status and items[0].status == status

@pytest.mark.parametrize("status", ["invalid", "", "RESOLVED-ISH"])
def test_update_status_rejects_unsupported_state(status):
    with pytest.raises(ValueError): update_status(1, status, make_records())

def test_update_status_rejects_unknown_record():
    with pytest.raises(LookupError): update_status(999, STATUS_CHECKS[0], make_records())

@pytest.mark.parametrize("status", STATUS_CHECKS)
def test_summary_counts_each_status_bucket(status):
    items = make_records()
    assert summary(items)["by_status"][status] == sum(1 for item in items if item.status == status)

@pytest.mark.parametrize("category", CATEGORY_CHECKS)
def test_summary_counts_each_category(category):
    items = make_records()
    assert summary(items)["by_category"][category] == sum(1 for item in items if item.category == category)

def test_summary_handles_empty_catalogue():
    result = summary([])
    assert result["total"] == 0 and result["by_status"] == {status: 0 for status in STATUS_VALUES} and result["by_category"] == {}

def test_summary_does_not_mutate_input():
    items = make_records(); before = [item.to_dict() for item in items]
    summary(items)
    assert [item.to_dict() for item in items] == before

@pytest.mark.parametrize("repeat", [1,2,3,4])
def test_domain_operation_happy_path(repeat):
    items = make_records()
    checkout_item(1, "student-new", "2026-12-01", items)
    if 'LabLedger' == "LabLedger":
        assert items[0].status == "Checked Out" and items[0].borrower == "student-new"
    elif 'LabLedger' == "EventHive":
        assert items[0].registered_count == 11 and "new@example.org" in items[0].attendees
    elif 'LabLedger' == "ClubBudget":
        assert items[0].status == "Approved"
    else:
        assert items[0].passengers == 13

@pytest.mark.parametrize("case", [0,1,2,3])
def test_filtering_does_not_mutate_input(case):
    items = make_records(); before = [item.to_dict() for item in items]
    if case == 0: filter_records(items, category=CATEGORY_CHECKS[0])
    elif case == 1: filter_records(items, status=STATUS_CHECKS[0])
    elif case == 2: filter_records(items, query=SEARCH_CASES[0][0])
    else: filter_records(items, category=CATEGORY_CHECKS[2], status=STATUS_CHECKS[1])
    assert [item.to_dict() for item in items] == before

@pytest.mark.parametrize("size", [2,4,6])
def test_sample_subsets_have_unique_ids(size):
    ids = [item.id for item in make_records()[:size]]
    assert len(ids) == len(set(ids))

def test_separate_loads_return_separate_objects(tmp_path):
    path = tmp_path / "records.json"; save_records(make_records(), path)
    one, two = load_records(path), load_records(path)
    assert one[0] == two[0] and one[0] is not two[0]

@pytest.mark.parametrize("case", [0,1])
def test_searching_and_filtering_are_repeatable(case):
    items = make_records(); before = [x.to_dict() for x in items]
    query = SEARCH_CASES[case][0]
    filter_records(items, query=query)
    filter_records(items, query=query)
    assert [x.to_dict() for x in items] == before

# Required defects students must correct: 24 cases, four groups of six/eight/four.
@pytest.mark.parametrize("query,expected", NORMALIZATION_CASES)
def test_search_normalises_case_and_surrounding_whitespace(query, expected):
    assert [item.id for item in search_records(query, make_records())] == expected

@pytest.mark.parametrize("new_status", STATUS_VALUES[:3] + [STATUS_VALUES[0]])
def test_status_update_is_persisted_for_default_storage(monkeypatch, new_status):
    items = make_records(); saved = []
    monkeypatch.setattr(service, "load_records", lambda: items)
    monkeypatch.setattr(service, "save_records", lambda rows, path=service.DATA_FILE: saved.append([x.to_dict() for x in rows]))
    service.update_status(1, new_status)
    assert len(saved) == 1 and saved[0][0]["status"] == new_status

@pytest.mark.parametrize("case", [0,1,2,3])
def test_summary_total_includes_terminal_records(case):
    items = make_records()
    terminal = next(item for item in items if item.status == CLOSED_STATUS)
    other = [item for item in items if item.status != CLOSED_STATUS]
    selected = [terminal] + other[:case]
    assert summary(selected)["total"] == len(selected)

@pytest.mark.parametrize("invalid_case", ["duplicate-id", "invalid-status", "invalid-category", "negative-id"])
def test_storage_rejects_invalid_records(tmp_path, invalid_case):
    row = make_records()[0].to_dict()
    if invalid_case == "duplicate-id": payload = [row, deepcopy(row)]
    else:
        bad = deepcopy(row)
        if invalid_case == "invalid-status": bad["status"] = "Not A Status"
        elif invalid_case == "invalid-category": bad["category"] = "Not A Category"
        else: bad["id"] = -1
        payload = [bad]
    path = tmp_path / "invalid.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(ValueError): load_records(path)

@pytest.mark.parametrize("case", [0,1,2,3])
def test_domain_operations_reject_unsafe_edge_cases(case):
    items = make_records()
    if 'LabLedger' == "LabLedger":
        if case == 0: items[2].status = "Maintenance"; args=(3,"borrower","2026-12-01")
        elif case == 1: args=(2,"different-borrower","2026-12-01")
        elif case == 2: args=(1,"   ","2026-12-01")
        else: args=(1,"borrower","not-a-date")
        with pytest.raises(ValueError): checkout_item(*args, records=items)
    elif 'LabLedger' == "EventHive":
        if case == 0: items[0].registered_count=items[0].capacity
        elif case == 1: items[0].status="Cancelled"
        elif case == 2: items[0].attendees.append("duplicate@example.org")
        else: pass
        email = "duplicate@example.org" if case == 2 else ("   " if case == 3 else "new@example.org")
        with pytest.raises(ValueError): register_attendee(1,email,items)
    elif 'LabLedger' == "ClubBudget":
        if case == 0: items[0].budget_limit=50; items[1].category=items[0].category; items[1].status="Approved"; items[1].amount=60; items[0].amount=20
        elif case == 1: items[0].amount=-1
        elif case == 2: items[0].status="Rejected"
        else: items[0].budget_limit=0; items[0].amount=1
        with pytest.raises(ValueError): approve_expense(1,items)
    else:
        if case == 0: items[0].passengers=items[0].capacity
        elif case == 1: items[0].status="Cancelled"
        elif case == 2: items[0].capacity=0
        else: items[0].passengers=items[0].capacity+1
        with pytest.raises(ValueError): book_seat(1,items)
