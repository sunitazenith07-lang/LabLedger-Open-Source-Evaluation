"""Deterministic fixtures for LabLedger."""
from copy import deepcopy
from models import RECORD_CLASS

_SAMPLE = [
    {'id': 1, 'name': 'Arduino Kit Alpha', 'asset_tag': 'LAB-001', 'category': 'Electronics', 'condition': 'Good', 'status': 'Available', 'location': 'Room A', 'description': 'Controller kit for practicals', 'borrower': '', 'due_date': ''},
    {'id': 2, 'name': 'Oscilloscope Probe', 'asset_tag': 'LAB-002', 'category': 'Tools', 'condition': 'Good', 'status': 'Checked Out', 'location': 'Room A', 'description': 'Probe set', 'borrower': 'student02', 'due_date': '2026-10-25'},
    {'id': 3, 'name': '3D Printer', 'asset_tag': 'LAB-003', 'category': 'Fabrication', 'condition': 'Fair', 'status': 'Maintenance', 'location': 'Makerspace', 'description': 'Printer awaiting nozzle repair', 'borrower': '', 'due_date': ''},
    {'id': 4, 'name': 'Laptop 14', 'asset_tag': 'LAB-004', 'category': 'Computing', 'condition': 'Good', 'status': 'Available', 'location': 'Room B', 'description': 'Lab laptop', 'borrower': '', 'due_date': ''},
    {'id': 5, 'name': 'Digital Sensor', 'asset_tag': 'LAB-005', 'category': 'Electronics', 'condition': 'Good', 'status': 'Checked Out', 'location': 'Room C', 'description': 'Sensor kit', 'borrower': 'student05', 'due_date': '2026-10-24'},
    {'id': 6, 'name': 'Soldering Station', 'asset_tag': 'LAB-006', 'category': 'Tools', 'condition': 'Good', 'status': 'Available', 'location': 'Room C', 'description': 'Bench station', 'borrower': '', 'due_date': ''}
]

def make_records():
    return [RECORD_CLASS.from_dict(row) for row in deepcopy(_SAMPLE)]
