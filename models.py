"""Domain model for LabLedger."""
from dataclasses import asdict, dataclass

VALID_STATUSES = ['Available', 'Checked Out', 'Maintenance']
VALID_CATEGORIES = ['Electronics', 'Tools', 'Fabrication', 'Computing']
FIELD_NAMES = ['id', 'name', 'asset_tag', 'category', 'condition', 'status', 'location', 'description', 'borrower', 'due_date']

@dataclass
class Equipment:
    id: int
    name: str
    asset_tag: str
    category: str
    condition: str
    status: str
    location: str
    description: str
    borrower: str
    due_date: str

    @property
    def searchable_text(self) -> str:
        return " ".join(str(getattr(self, field, "")) for field in ("name", "asset_tag", "category", "location", "description"))

    def to_dict(self) -> dict:
        """Return a JSON-serialisable dictionary."""
        return asdict(self)

    def validate(self) -> None:
        # Intentionally incomplete validation for the evaluation starter.
        return None

    @classmethod
    def from_dict(cls, row: dict) -> "Equipment":
        """Build a model from a JSON object, checking required fields."""
        if not isinstance(row, dict):
            raise ValueError("Each record must be a JSON object")
        missing = set(FIELD_NAMES).difference(row)
        if missing:
            raise ValueError(f"Missing fields: {', '.join(sorted(missing))}")
        # Deliberately skip domain validation at starter stage.
        return cls(**{key: row[key] for key in FIELD_NAMES})

RECORD_CLASS = Equipment
