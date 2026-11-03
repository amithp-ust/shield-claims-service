"""Coverage, fraud, and payout orchestration (CM-CLAIMS)."""

from collections.abc import Callable


class ClaimsService:
    def __init__(self, get_policy: Callable, score_fraud: Callable,
                 create_payout: Callable):
        self.get_policy = get_policy
        self.score_fraud = score_fraud
        self.create_payout = create_payout
        self._claims: dict[str, dict] = {}

    def adjudicate(self, claim_id: str, policy_id: str,
                   requested_cents: int) -> dict:
        if not claim_id or not policy_id:
            raise ValueError("claim_id and policy_id are required")
        if type(requested_cents) is not int or requested_cents <= 0:
            raise ValueError("requested_cents must be a positive integer")
        if claim_id in self._claims:
            existing = self._claims[claim_id]
            if (existing["policy_id"] != policy_id
                    or existing["requested_cents"] != requested_cents):
                raise ValueError("Conflicting claim retry")
            return dict(existing)
        policy = self.get_policy(policy_id)
        if policy["status"] != "active":
            raise ValueError("Policy is not active")
        risk = self.score_fraud(policy_id, requested_cents)
        paid_cents = 0
        if risk["score"] >= 80:
            status = "manual_review"
        else:
            payable = min(
                max(0, requested_cents - policy["deductible_cents"]),
                policy["coverage_cents"],
            )
            if payable:
                payout = self.create_payout(claim_id, payable)
                paid_cents = payout["amount_cents"]
                if payout["claim_id"] != claim_id or paid_cents != payable:
                    raise ValueError("Payout response does not match claim")
                status = "partially_paid" if paid_cents < requested_cents else "paid"
            else:
                status = "denied"
        claim = {
            "claim_id": claim_id,
            "policy_id": policy_id,
            "requested_cents": requested_cents,
            "paid_cents": paid_cents,
            "status": status,
        }
        self._claims[claim_id] = claim
        return dict(claim)

    def get_claim(self, claim_id: str) -> dict:
        if claim_id not in self._claims:
            raise LookupError(f"Claim not found: {claim_id}")
        return dict(self._claims[claim_id])
