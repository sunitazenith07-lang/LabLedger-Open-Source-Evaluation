# LabLedger: Payment Ledger & Reconciliation Engine

**Track:** Fintech reliability | **Language:** Python 3.10+ | **Time:** 24-hour evaluation

## Scenario
A fintech product receives payment events from a payment provider. Events can arrive late, more than once, or in a different order. Internal transaction records may also disagree with a provider's settlement report. Incorrect handling can show a failed payment as successful, credit the same payment twice, or refund more than was paid.

You are joining an existing small Python service. Improve the supplied code; do not replace it with a new framework or connect to external APIs. All data is synthetic and the challenge runs offline.

## Required behaviour
1. Process payment events: payment_succeeded, payment_failed and refund_succeeded.
   Payment state transitions are terminal: payment_succeeded and payment_failed only change a PENDING transaction. Later conflicting payment events must not silently reverse a terminal status; use reconciliation to surface disagreement.
2. Process each event_id at most once. Replaying the same event must not change the result a second time.
3. Store money in integer paise. Refunds must be positive and cumulative refunds must never exceed the original transaction amount.
4. A refund may only be applied to a transaction whose payment succeeded. A failed or pending transaction must not become refunded because of a refund event.
5. A partial refund must keep the transaction partially refunded. Mark it REFUNDED only when the full amount is refunded.
6. Reconcile internal and provider records by transaction_id. Report records missing from either side, amount mismatches, and status mismatches separately. Sort report items deterministically.
7. Handle unknown transaction IDs, invalid events, empty input and missing fields without corrupting state.
8. Keep changes focused, with clear names and comments for non-obvious financial rules.

## Setup
Run: `python -m pip install -r requirements-dev.txt`, then `python -m pytest -q`, then `python -m main`.

## Work to submit
- Read the source and run the starter tests before editing.
- Use the required behaviour above as the acceptance contract. Investigate test failures, trace their root causes, and fix the underlying behaviour rather than hard-coding fixture results.
- Add regression tests for defects you fix and document at least five edge cases in `TESTING.md`.
- Submit one pull request against the original repository containing your changes and tests. Do not merge it.
- Include `RECONCILIATION_NOTES.md` with one example input/output, key assumptions and three edge cases.

## Optional stretch work
Choose at most one after the required behaviour is correct: export a CSV report; add counts by mismatch type; or flag possible duplicate provider references for human review.

## Testing and GitHub Actions
Some visible tests are expected to fail on the untouched starter because key behaviours are incomplete. The test suite's exact initial counts can change as the repository is updated; no fixed count is promised. GitHub Actions runs on pushes and pull-request updates and publishes test counts. A red check before your fixes is expected; the goal is to make the visible tests pass without deleting, skipping, weakening or bypassing them. Do not edit the workflow to evade failures.

## Individual-work policy
AI chatbots, AI coding assistants, generated patches/tests and asking another person to write or debug the solution are prohibited. Ordinary non-AI Python documentation is allowed. Do not upload challenge code or data to external services. You must explain your changes and make a small live modification if asked. Organisers may use a short code walkthrough; no automated detector can prove AI use.

## Evaluation — 100 marks
- Understanding the code and data flow: 15
- Root-cause analysis and correctness: 30
- Safe event processing and reconciliation edge cases: 25
- Regression testing: 15
- Code quality and maintainability: 5
- Pull request, notes and live explanation: 10

The goal is reliable financial behaviour, not the number of lines written.
