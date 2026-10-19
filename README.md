# LabLedger — Student Starter

**Zenith School of AI | Individual Open-Source Evaluation**

LabLedger is a Python application for managing lab equipment, checkouts and returns.

## Start here
1. Read [the student problem statement](STUDENT_PROBLEM_STATEMENT.md) before coding.
2. Use Python 3.10+ and Git.
3. Install dependencies and run the tests from the repository root:

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
python -m main
```

The starter includes 110 visible contract tests. Some are expected to fail on the untouched starter: investigate and fix the defects rather than deleting, skipping, weakening or bypassing tests. The final evaluation also includes additional private checks that are not included in this public repository.

## Project map
- `models.py` — domain models and validation.
- `service.py` — storage, search/filtering, status changes and domain operations.
- `data/records.json` — sample records.
- `tests/test_contract.py` — visible contract tests.
- `.github/workflows/tests.yml` — runs checks on pushes and pull requests and reports test counts.
- `CONTRIBUTING.md` and templates — submission workflow and documentation.

## Required work
- Understand the code and create `ARCHITECTURE.md` from the supplied template.
- Fix the three organiser issue tickets announced at kick-off.
- Implement equipment search and combined filters.
- Complete one optional feature from the problem statement.
- Add relevant tests, document at least five test cases, and prepare a two-minute demo.
- Use focused branches and pull requests, and declare AI assistance if used.

Start only when the organiser announces the evaluation. See `CONTRIBUTING.md` for the expected workflow.
