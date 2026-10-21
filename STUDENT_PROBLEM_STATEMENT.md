# LabLedger: Payment Ledger & Reconciliation Engine

**Track:** Fintech reliability | **Language:** Python 3.10+ | **Time:** 24-hour evaluation

## Scenario
A fintech product receives payment events from a payment provider. Events can arrive late, more than once, or in a different order. Internal transaction records can also disagree with the provider's settlement report. Incorrect handling can show a failed payment as successful, credit the same payment twice, or mark a transaction refunded for more money than was paid.

You are joining an existing small Python service. Improve the existing code; do not replace the project with a new framework or an external API integration. All data is synthetic and the challenge runs offline.

## Required behaviour
1. **Process payment events.** Support payment_succeeded, payment_failed and refund_succeeded events. Keep transaction status consistent with the event and the rules below.
2. **Idempotency.** Each event has an event_id. Processing the same event more than once must not change the result after its first successful processing.
3. **Money safety.** Amounts are integer paise. Do not accept zero or negative refund amounts. The total refunded amount must never exceed the original transaction amount.
4. **Valid transitions.** A refund can only be applied to a transaction whose payment succeeded. A failed or pending transaction must not become refunded because of a refund event.
5. **Reconciliation.** Compare internal and provider records by transaction_id. Report records missing from either side, amount mismatches, and status mismatches. Results must be deterministic.
6. **Explainability.** Keep functions small and add comments where a non-obvious financial rule is enforced.

## Record format
An internal transaction is a dictionary with transaction_id, amount_paise, status, refunded_paise and processed_event_ids. Status is PENDING, SUCCEEDED, FAILED or REFUNDED. An event is a dictionary with event_id, transaction_id, type and, for refunds, amount_paise. Provider records contain transaction_id, amount_paise and status.

## Mandatory work
- Read the source and run the existing tests before editing.
- Reproduce and fix the defects described in the issue tickets announced at the evaluation kick-off. Organisers will release the ticket text at kick-off.
- Make the required behaviour above correct and robust to missing fields, unknown transaction IDs, duplicate events, invalid amounts, empty lists and out-of-order events.
- Add regression tests for the defects you fix.
- Add a concise RECONCILIATION_NOTES.md with one example input/output, your key assumptions, and three edge cases you tested.
- Submit a pull request containing your changes, tests run, root-cause explanation and limitations.

## Optional stretch work
Choose at most one: (A) export a reconciliation report as CSV; (B) add a summary with counts by mismatch type; or (C) detect repeated provider references and report possible duplicate transactions. Stretch work is not required for a strong core score.

## Test and CI instructions
Run python -m pytest -q locally. The initial starter intentionally has failing tests. GitHub Actions runs on every push and pull-request update and reports the test outcome. Do not delete or weaken tests, edit the CI workflow to avoid failures, or hard-code the sample results. A failed check is not a submission blocker by itself; it is feedback about unfinished behaviour.

## Integrity rules
AI chatbots, AI code completion, generated patches and asking another person to write or debug the solution are not allowed. Work must be your own. You may use Python documentation and ordinary non-AI reference documentation. You will be asked to explain your changes and make a small live modification. A submission you cannot explain may receive no credit under the event rules.

## Evaluation — 100 marks
- Understanding the code and data flow: 15
- Root-cause analysis and correctness: 30
- Safe event processing and reconciliation edge cases: 25
- Regression testing: 15
- Code quality and maintainability: 5
- Pull request, notes and live explanation: 10

The goal is reliable financial behaviour, not the number of lines written.
