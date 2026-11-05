# Shield claims service

**Application:** Claims (`claims`)

**Component:** `CM-CLAIMS`

**Owner:** Claims platform

`src/claims/service.py` adjudicates synthetic claims using callbacks to:

- `shield-policy-service` for coverage and deductible checks;
- `shield-fraud-scoring` for a risk score;
- `shield-billing-service` for a payout.

A score of 80 or more requires manual review. Otherwise, a payout is the
requested loss less the deductible, capped by coverage. A zero payout is denied.
The response exposes status and amounts, but no payment-reason explanation.
Claims and idempotent results are held in memory for the service instance.
`contracts/claims-api.yaml` describes the intended API.

## Specification consumer

Canonical specs, authoring, gates, and requirement metrics live only in
[`amithp-ust/Intent-to-spec`](https://github.com/amithp-ust/Intent-to-spec).
Shared glossary, map, standards, and policy remain in
[`amithp-ust/shield-context`](https://github.com/amithp-ust/shield-context).
This repo owns `CM-CLAIMS` implementation, not spec authoring. See
[AGENTS.md](AGENTS.md) for immutable approved spec references, issue/PR traceability,
human review, and fixture-contract checks. Do not install authoring here or copy
specs; empty `specs/.gitkeep` is a legacy placeholder.

Python 3.11+, standard library only. Run `python -m unittest discover -s tests`
from this repository root; the unit-test CI runs the same command on Python 3.11.
These callable stubs are not production claims processing or HTTP servers.
