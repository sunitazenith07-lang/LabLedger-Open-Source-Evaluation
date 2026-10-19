# LabLedger: Lab Equipment Inventory and Checkout

**Zenith School of AI | Individual Open-Source Evaluation | Python + JSON + GitHub**

## 1. The challenge
University labs lend equipment such as microcontroller kits, sensors, laptops, cables and tools. The team needs to track what exists, what is available, who has borrowed each item and when it should be returned. LabLedger is an existing small Python application that maintains an equipment catalogue and checkout records using JSON files.

Your task is to understand the supplied code, fix issues announced by organisers, improve equipment search and filtering, add one lab-operations feature, test your changes and explain your decisions. Improve the existing application rather than rebuilding it from scratch.

## 2. Setup
Use Python 3.10+ and Git. From the repository root, run:

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
python -m main
```

Read `README.md`, `CONTRIBUTING.md` and this problem statement before coding.

## 3. Understand the existing project — mandatory
Inspect the files before making changes. Be able to explain how information flows from JSON storage through domain logic to command-line output.

- `models.py` — equipment model and field definitions.
- `service.py` — JSON storage, catalogue search/filtering, status updates, checkout/return and summary logic.
- `main.py` — command-line preview.
- `data/` — sample equipment and checkout records.
- `tests/test_contract.py` — visible automated behaviour checks.
- `fixtures.py` — deterministic test/sample records.

Create `ARCHITECTURE.md` using `ARCHITECTURE_TEMPLATE.md`. Include the project map, data model, a numbered data flow, storage design, a simple diagram and three improvements grounded in the code you inspected.

## 4. Fix reported issues — mandatory
At kick-off, organisers will announce three issue tickets with observed and expected behaviour. For each one: reproduce the issue, identify its root cause, make a focused fix and add or update a regression test. The provided tickets and acceptance examples are authoritative; do not guess at unannounced behaviour.

## 5. Core feature — equipment search and filtering
Implement and test all of the following:
- Search by equipment name or asset tag without case sensitivity. Leading/trailing spaces should not produce confusing results.
- Filter by category and state: `Available`, `Checked Out` or `Maintenance`.
- Allow text search and multiple filters to work together.
- Show a clear result when no items match.
- Validate unsupported filter values and handle an empty catalogue safely.
- Never show an item as available if it is checked out or under maintenance.

## 6. Add at least one lab-operations feature
Choose at least one option below. Integrate it into the existing application and include relevant tests.

**Option A — Overdue checkout view:** List items whose due date is before a supplied reference date and which have not been returned. Show equipment, borrower and due date. Handle the case where nothing is overdue.

**Option B — Availability summary:** Report total equipment and counts for available, checked-out and maintenance states. Show counts by category and handle an empty catalogue safely.

**Option C — Checkout history:** Show checkout/return history for one item or borrower. Keep history in date order and do not silently discard previous records.

## 7. Code quality and testing
Use clear names, sensible functions/modules and existing project conventions. Handle empty collections, missing fields, invalid values and unexpected input safely. Add or update tests for your fixes and feature.

The starter's **110 visible tests** intentionally include failures. The untouched project is expected to begin with **86 passing and 24 failing tests**. Make the behaviour correct; do not remove, skip, weaken or bypass tests/checks. The final evaluation also includes **90 additional private checks**, for 200 automated cases in total. These private tests are not included in this public repository; passing the visible suite alone does not guarantee full credit.

Document at least five test scenarios in `TESTING.md`, with expected and actual results. Useful scenarios include checkout/return state transitions, maintenance restrictions, whitespace/case-insensitive search, combined filters, impossible search combinations, unknown IDs, malformed records and empty catalogues.

## 8. GitHub workflow
- Use a focused branch for each unrelated issue: `fix/issue-<number>-<short-description>`.
- Use `feature/<short-feature-name>` for features.
- Use commit messages such as `fix(storage): persist checkout return` or `feat(summary): add availability counts`.
- Open pull requests with a summary, root cause, issue reference, tests run and known limitations.
- Keep `PROJECT_NOTES.md` current with completed requirements, files changed, decisions, tests, assumptions and next steps.
- Check the GitHub Actions result on each pull request.

## 9. Schedule
Follow the schedule and announcements issued by organisers. Current planning slots are:
- **30 October, 5:00 PM:** event starts.
- **30 October, 6:00 PM:** problem statement and issue tickets shared.
- **30 October, 8:00 PM:** dinner break.
- **30 October, 9:00 PM:** work resumes.
- **30 October, 10:00 PM:** Round 1 check.
- **31 October, 3:00 AM:** Round 2 mentor evaluation.
- **31 October, 8:00–9:00 AM:** breakfast window.

Organisers will confirm the code-freeze, submission and demo/viva timings. Treat the latest official announcement as authoritative.

## 10. Submission requirements
Submit:
- Your fork/repository URL and pull-request links.
- `README.md` with setup, run and usage instructions.
- `ARCHITECTURE.md`, `TESTING.md` and `PROJECT_NOTES.md`.
- A summary of bugs fixed and features completed.
- An `AI_USAGE.md` declaration if AI assistance is used.
- A two-minute demo; include a live demo URL if deployment is feasible, otherwise provide reliable local run instructions.

## 11. AI tools and academic integrity
AI tools and online resources are permitted, but you are responsible for understanding and verifying every change. In `AI_USAGE.md`, record the tool/model or source, its purpose, what you verified or changed yourself, and any displayed credit/token count (otherwise write “not available”). State one suggestion you accepted, modified or rejected and why. Do not include secrets or private personal data. Copying another student's code or submitting a solution you cannot explain is prohibited; mentors may give an unseen input or ask you to modify a small function during the viva.

## 12. Evaluation rubric — 100 marks

| Parameter | Marks | What mentors assess |
|---|---:|---|
| Codebase understanding | 15 | Explains the project structure, domain model, data flow and where changes belong. |
| Problem solving | 25 | Finds root causes, selects appropriate logic/data structures and handles edge cases. |
| Working prototype | 20 | Required bug fixes, search/filter capability and one additional feature work. |
| Code quality | 10 | Readable, maintainable code that follows project conventions. |
| Testing | 10 | Runs checks, adds relevant tests and explains results/limitations. |
| Demo and communication | 20 | Clear demo, explains decisions/trade-offs, answers questions and acknowledges limitations. |
| **Total** | **100** | |

All 300 students will be assessed using the same six-parameter rubric. The top 270 students will be shortlisted by final score, subject to any minimum competency criteria announced before the event. Ties at the cutoff will be resolved by Problem Solving, Demo & Communication, Working Prototype, Codebase Understanding, then Testing.

## 13. Demo and viva
Be prepared to explain how records are represented and move through the program, demonstrate a bug fix and its root cause, show search/filtering and your chosen additional feature, explain one algorithm or validation decision and one limitation, show your branch/commit/pull-request history and automated test results, and make or describe a small change to a function you wrote.
