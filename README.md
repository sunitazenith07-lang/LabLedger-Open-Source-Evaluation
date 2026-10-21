# LabLedger — Payment Ledger & Reconciliation

Zenith School of AI | Individual Open-Source Evaluation | Python 3.10+

This is a startup-style fintech engineering challenge inspired by the payment reconciliation problems financial products face. It is a simulated project; it does not connect to real banks, payment processors or customer data.

## Start here
1. Read STUDENT_PROBLEM_STATEMENT.md.
2. Install Python 3.10+ and Git.
3. Install dependencies: python -m pip install -r requirements-dev.txt
4. Run the tests: python -m pytest -q
5. Run the demo: python -m main

The starter intentionally contains several defects. Some tests will fail before you fix them. That is expected. A lower failure count means your changes fixed some behaviours; a green test check means every visible test passed. Never delete, skip, weaken or bypass a test to make the check green.

## Files
- service.py — event processing and reconciliation logic.
- models.py — transaction states and starter data helpers.
- fixtures.py and data/records.json — synthetic examples only.
- tests/test_contract.py — visible behavioural tests.
- .github/workflows/tests.yml — runs when code is pushed or a pull request is opened/updated.

## Submission
Fork this repository, work in focused branches, and open a pull request against this original repository. Do not merge your pull request. GitHub Actions should run against the pull-request code and display the test result. Submit the PR URL and be ready for a live code walkthrough.

AI coding assistants and generated solutions are prohibited during this evaluation. Read CONTRIBUTING.md and the integrity declaration before coding.
