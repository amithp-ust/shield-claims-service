import unittest
from unittest.mock import Mock

from src.claims.service import ClaimsService


class ClaimsTests(unittest.TestCase):
    def setUp(self):
        self.policy = Mock(return_value={
            "status": "active", "coverage_cents": 100000,
            "deductible_cents": 10000,
        })
        self.fraud = Mock(return_value={"score": 10})
        self.payout = Mock(side_effect=lambda claim_id, amount: {
            "claim_id": claim_id, "amount_cents": amount,
        })
        self.service = ClaimsService(self.policy, self.fraud, self.payout)

    def test_partial_payment_and_retry(self):
        result = self.service.adjudicate("CL-1", "P-1", 50000)
        self.assertEqual(result["paid_cents"], 40000)
        self.assertEqual(result["status"], "partially_paid")
        self.assertEqual(result, self.service.adjudicate("CL-1", "P-1", 50000))
        self.payout.assert_called_once_with("CL-1", 40000)

    def test_coverage_cap(self):
        self.assertEqual(
            self.service.adjudicate("CL-1", "P-1", 200000)["paid_cents"], 100000
        )

    def test_manual_review(self):
        self.fraud.return_value = {"score": 80}
        self.assertEqual(
            self.service.adjudicate("CL-1", "P-1", 50000)["status"], "manual_review"
        )
        self.payout.assert_not_called()

    def test_denied(self):
        self.assertEqual(
            self.service.adjudicate("CL-1", "P-1", 10000)["status"], "denied"
        )
        self.payout.assert_not_called()

    def test_conflict(self):
        self.service.adjudicate("CL-1", "P-1", 50000)
        with self.assertRaises(ValueError):
            self.service.adjudicate("CL-1", "P-1", 60000)

    def test_dependency_error_propagates(self):
        self.policy.side_effect = LookupError("Policy unavailable")
        with self.assertRaises(LookupError):
            self.service.adjudicate("CL-1", "P-1", 50000)
        self.payout.assert_not_called()

    def test_missing_claim(self):
        with self.assertRaises(LookupError):
            self.service.get_claim("unknown")
