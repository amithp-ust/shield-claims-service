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

Shared context: `amithp-ust/shield-context` (`AGENTS.md`, glossary, scope,
standards, component map). `specs/` is empty. For the future
`001-claim-payment-reason` intent, this repository would host the full spec,
interview, plan, and tasks; the portal would receive only its requirements with
a link back to the primary spec. No such spec has been published yet.

Python 3.12+, standard library only. Run `python -m unittest discover -s tests`.
These callable stubs are not production claims processing or HTTP servers.
